"""Tests for the deterministic read-only next-action query (scripts/next_action.py).

Author: elvis
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_core_gates.py"
NEXT_ACTION_PATH = ROOT / "scripts" / "next_action.py"
HANDOFF_REF_PATH = ROOT / "references" / "handoff-contract.md"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module {name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def artifact_ref(path: str) -> dict[str, str]:
    return {"path": path, "sha256": "a" * 64}


def render_handoff_status(validator, data: dict) -> str:
    def scalar(value) -> str:
        if value is None:
            return "null"
        if value is True:
            return "true"
        if value is False:
            return "false"
        return str(value)

    def render(value, indent: int = 0) -> list[str]:
        prefix = " " * indent
        lines: list[str] = []
        if isinstance(value, dict):
            for key, item in value.items():
                if isinstance(item, (dict, list)):
                    lines.append(f"{prefix}{key}:")
                    lines.extend(render(item, indent + 2))
                else:
                    lines.append(f"{prefix}{key}: {scalar(item)}")
            return lines
        if isinstance(value, list):
            for item in value:
                lines.append(f"{prefix}- {scalar(item)}")
            return lines
        raise AssertionError("renderer requires dict or list")

    body = "\n".join(render(data))
    return (
        "<!-- COOP_HANDOFF_CONTRACT_START -->\n"
        "```yaml\n"
        f"{body}\n"
        "```\n"
        "<!-- COOP_HANDOFF_CONTRACT_END -->\n"
    )


class NextActionQueryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_module("validate_core_gates", VALIDATOR_PATH)
        cls.handoff_text = HANDOFF_REF_PATH.read_text(encoding="utf-8")
        cls.base_contract = cls.validator.extract_handoff_contract(
            cls.handoff_text, "handoff-contract.md"
        )

    def load_next_action(self):
        self.assertTrue(
            NEXT_ACTION_PATH.is_file(),
            f"missing scripts/next_action.py at {NEXT_ACTION_PATH}",
        )
        return load_module("next_action", NEXT_ACTION_PATH)

    def make_contract(self, **overrides) -> dict:
        data = copy.deepcopy(self.base_contract)
        data.update(copy.deepcopy(overrides))
        return data

    def test_imports_single_source_of_truth_from_validate_core_gates(self) -> None:
        na = self.load_next_action()
        source = NEXT_ACTION_PATH.read_text(encoding="utf-8")
        self.assertIs(na.ALLOWED_TRANSITIONS, self.validator.ALLOWED_TRANSITIONS)
        self.assertIs(na.STATE_TUPLES, self.validator.STATE_TUPLES)
        self.assertIs(na.NEXT_OWNERS, self.validator.NEXT_OWNERS)
        self.assertIs(na.EXPECTED_OWNERS, self.validator.EXPECTED_OWNERS)
        self.assertIs(na.ARTIFACT_FIELDS, self.validator.ARTIFACT_FIELDS)
        self.assertIs(
            na.probe_transition_candidate,
            self.validator.probe_transition_candidate,
        )
        # Ensure transition table literals and condition logic are not duplicated in next_action.py
        self.assertNotIn("ALLOWED_TRANSITIONS = {", source)
        self.assertNotIn("EXPECTED_OWNERS = {", source)
        self.assertNotIn("STATE_TUPLES = {", source)
        self.assertNotIn("_is_transition_applicable", source)
        self.assertNotIn("planned_batches", source)

    def test_transition_decisions_delegate_exclusively_to_validate_transition(self) -> None:
        na = self.load_next_action()
        for batch_num in (1, 2):
            contract = self.make_contract(
                lifecycle_state="ready-for-review",
                current_batch=batch_num,
                planned_batches=2,
                last_review_result="not-run",
                final_verification="pending",
                final_review_result="pending",
                attempt_report_artifact=artifact_ref("docs/review/report.md"),
                last_review_artifact=None,
                final_verification_artifact=None,
                final_review_artifact=None,
                next_owner="codex-brief-antigravity-review",
            )
            text = render_handoff_status(self.validator, contract)
            result = na.query_next_action(text, label=f"batch-{batch_num}")
            reported_next = {
                item["next_state"] for item in result["legal_next_transitions"]
            }
            probed_next = {
                ns
                for ns in self.validator.ALLOWED_TRANSITIONS["ready-for-review"]
                if self.validator.probe_transition_candidate(contract, ns) is not None
            }
            self.assertEqual(reported_next, probed_next)

    def test_every_lifecycle_state_has_valid_query_result(self) -> None:
        na = self.load_next_action()
        state_fixtures = {
            "ready-for-brief": self.make_contract(
                lifecycle_state="ready-for-brief",
                last_review_result="not-run",
                final_verification="pending",
                final_review_result="pending",
                attempt_report_artifact=None,
                last_review_artifact=None,
                final_verification_artifact=None,
                final_review_artifact=None,
                next_owner="codex-brief-antigravity-review",
            ),
            "ready-for-execution": self.make_contract(
                lifecycle_state="ready-for-execution",
                last_review_result="not-run",
                final_verification="pending",
                final_review_result="pending",
                attempt_report_artifact=None,
                last_review_artifact=None,
                final_verification_artifact=None,
                final_review_artifact=None,
                next_owner="external-agent",
            ),
            "ready-for-review": self.make_contract(
                lifecycle_state="ready-for-review",
                last_review_result="not-run",
                final_verification="pending",
                final_review_result="pending",
                attempt_report_artifact=artifact_ref("docs/review/report.md"),
                last_review_artifact=None,
                final_verification_artifact=None,
                final_review_artifact=None,
                next_owner="codex-brief-antigravity-review",
            ),
            "needs-fix": self.make_contract(
                lifecycle_state="needs-fix",
                attempt=2,
                last_review_result="fail",
                final_verification="pending",
                final_review_result="pending",
                attempt_report_artifact=artifact_ref("docs/review/report.md"),
                last_review_artifact=artifact_ref("docs/review/review.md"),
                final_verification_artifact=None,
                final_review_artifact=None,
                next_owner="codex-brief-antigravity-review",
            ),
            "blocked": self.make_contract(
                lifecycle_state="blocked",
                risk_profile="strict",
                last_review_result="blocked",
                final_verification="pending",
                final_review_result="pending",
                attempt_report_artifact=artifact_ref("docs/review/report.md"),
                last_review_artifact=artifact_ref("docs/review/review-blocked.md"),
                blocked_reason="ambiguous migration boundary",
                blocker_owner="openspec-superpower-change",
                resume_condition="clarify migration rollback contract and re-run review",
                next_owner="openspec-superpower-change",
            ),
            "awaiting-final-verification": self.make_contract(
                lifecycle_state="awaiting-final-verification",
                current_batch=2,
                planned_batches=2,
                last_review_result="pass",
                final_verification="pending",
                final_review_result="pending",
                attempt_report_artifact=artifact_ref("docs/review/report.md"),
                last_review_artifact=artifact_ref("docs/review/review.md"),
                final_verification_artifact=None,
                final_review_artifact=None,
                next_owner="openspec-superpower-change",
            ),
            "complete": self.make_contract(
                lifecycle_state="complete",
                current_batch=2,
                planned_batches=2,
                last_review_result="pass",
                final_verification="pass",
                final_review_result="pass",
                attempt_report_artifact=artifact_ref("docs/review/report.md"),
                last_review_artifact=artifact_ref("docs/review/review.md"),
                final_verification_artifact=artifact_ref("docs/review/final-verify.md"),
                final_review_artifact=artifact_ref("docs/review/final-review.md"),
                next_owner="user",
            ),
        }
        self.assertEqual(
            set(state_fixtures),
            self.validator.LIFECYCLE_STATES,
        )
        for state, contract in state_fixtures.items():
            with self.subTest(state=state):
                text = render_handoff_status(self.validator, contract)
                result = na.query_next_action(text, label=state)
                self.assertEqual(result["status"], "OK")
                self.assertTrue(result["advisory"])
                self.assertFalse(result["promotable"])
                self.assertFalse(result["authoritative"])
                self.assertEqual(result["current_state"], state)
                self.assertEqual(
                    result["allowed_next_owners"],
                    sorted(self.validator.EXPECTED_OWNERS[state]),
                )
                self.assertEqual(
                    result["confirmation_lease_status"],
                    contract["confirmation_lease_status"],
                )
                if state == "blocked":
                    self.assertEqual(result["legal_next_transitions"], [])
                    self.assertEqual(result["blocker_owner"], contract["blocker_owner"])
                    self.assertEqual(result["resume_condition"], contract["resume_condition"])
                elif state == "complete":
                    self.assertEqual(result["legal_next_transitions"], [])
                else:
                    next_states = {
                        item["next_state"] for item in result["legal_next_transitions"]
                    }
                    self.assertTrue(
                        next_states.issubset(self.validator.ALLOWED_TRANSITIONS[state])
                    )
                    self.assertGreater(len(next_states), 0)
                    for item in result["legal_next_transitions"]:
                        self.assertEqual(
                            item["allowed_next_owners"],
                            sorted(self.validator.EXPECTED_OWNERS[item["next_state"]]),
                        )
                        for role_binding in item["required_evidence_roles"]:
                            self.assertIn("evidence_role", role_binding)
                            self.assertIn("artifact_field", role_binding)
                            self.assertIn("bound_identity", role_binding)

    def test_awaiting_final_verification_after_verification_pass_shows_complete_with_previous_status(self) -> None:
        na = self.load_next_action()
        contract = self.make_contract(
            lifecycle_state="awaiting-final-verification",
            current_batch=2,
            planned_batches=2,
            last_review_result="pass",
            final_verification="pass",
            final_review_result="pending",
            attempt_report_artifact=artifact_ref("docs/review/report.md"),
            last_review_artifact=artifact_ref("docs/review/review.md"),
            final_verification_artifact=artifact_ref("docs/review/final-verify.md"),
            final_review_artifact=None,
            next_owner="openspec-superpower-change",
        )
        text = render_handoff_status(self.validator, contract)
        result = na.query_next_action(text, label="awaiting-verified")
        self.assertEqual(result["status"], "OK")
        by_state = {
            item["next_state"]: item for item in result["legal_next_transitions"]
        }
        self.assertIn("complete", by_state)
        self.assertNotIn("awaiting-final-verification", by_state)
        complete_entry = by_state["complete"]
        self.assertTrue(complete_entry["requires_previous_status"])
        roles = [r["evidence_role"] for r in complete_entry["required_evidence_roles"]]
        self.assertIn("final-review", roles)

    def test_strict_blocked_status_echoes_resume_context_and_zero_transitions(self) -> None:
        na = self.load_next_action()
        contract = self.make_contract(
            lifecycle_state="blocked",
            risk_profile="strict",
            last_review_result="blocked",
            final_verification="pending",
            final_review_result="pending",
            attempt_report_artifact=artifact_ref("docs/review/report.md"),
            last_review_artifact=artifact_ref("docs/review/review-blocked.md"),
            blocked_reason="strict database boundary requires user sign-off",
            blocker_owner="user",
            resume_condition="user explicitly approves migration window in canonical status",
            next_owner="user",
        )
        text = render_handoff_status(self.validator, contract)
        result = na.query_next_action(text, label="strict-blocked")
        self.assertEqual(result["status"], "OK")
        self.assertEqual(result["current_state"], "blocked")
        self.assertEqual(result["legal_next_transitions"], [])
        self.assertEqual(result["blocker_owner"], "user")
        self.assertEqual(
            result["resume_condition"],
            "user explicitly approves migration window in canonical status",
        )
        self.assertIsNone(result.get("suggested_next_action"))

    def test_invalid_or_unparsable_status_fails_closed_with_blocked(self) -> None:
        na = self.load_next_action()
        invalid_inputs = [
            "plain markdown without handoff markers",
            render_handoff_status(
                self.validator,
                self.make_contract(
                    lifecycle_state="ready-for-execution",
                    next_owner="user",  # invalid owner for ready-for-execution
                ),
            ),
            render_handoff_status(
                self.validator,
                self.make_contract(
                    lifecycle_state="complete",
                    last_review_result="not-run",  # invalid tuple for complete
                ),
            ),
        ]
        for idx, broken_text in enumerate(invalid_inputs):
            with self.subTest(case=idx):
                result = na.query_next_action(broken_text, label=f"broken-{idx}")
                self.assertEqual(result["status"], "BLOCKED")
                self.assertTrue(result["advisory"])
                self.assertFalse(result["promotable"])
                self.assertFalse(result["authoritative"])
                self.assertTrue(isinstance(result.get("reason"), str) and result["reason"].strip())
                self.assertEqual(result["legal_next_transitions"], [])
                self.assertIsNone(result.get("suggested_next_action"))

    def test_cli_is_read_only_and_never_mutates_files_or_emits_evidence_markers(self) -> None:
        self.load_next_action()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            status_file = tmp_dir / "status.md"
            status_file.write_text(self.handoff_text, encoding="utf-8")
            before_sha = hashlib.sha256(status_file.read_bytes()).hexdigest()

            proc = subprocess.run(
                [sys.executable, str(NEXT_ACTION_PATH), "--status", str(status_file)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, msg=proc.stderr)
            after_sha = hashlib.sha256(status_file.read_bytes()).hexdigest()
            self.assertEqual(before_sha, after_sha)
            self.assertEqual(list(tmp_dir.iterdir()), [status_file])

            self.assertNotIn(self.validator.START, proc.stdout)
            self.assertNotIn(self.validator.EVIDENCE_START, proc.stdout)
            payload = json.loads(proc.stdout)
            self.assertEqual(payload["status"], "OK")
            self.assertTrue(payload["advisory"])
            self.assertFalse(payload["promotable"])
            self.assertFalse(payload["authoritative"])

            # Invalid file via CLI exits non-zero and prints BLOCKED JSON
            broken_file = tmp_dir / "broken.md"
            broken_file.write_text("no markers here\n", encoding="utf-8")
            broken_proc = subprocess.run(
                [sys.executable, str(NEXT_ACTION_PATH), "--status", str(broken_file)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(broken_proc.returncode, 0)
            broken_payload = json.loads(broken_proc.stdout)
            self.assertEqual(broken_payload["status"], "BLOCKED")
            self.assertEqual(broken_payload["legal_next_transitions"], [])


if __name__ == "__main__":
    unittest.main()
