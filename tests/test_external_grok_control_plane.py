"""Behavior tests for one external Grok control-plane owner move.

Pins are written only under TemporaryDirectory. The source pin path and the
installed skill pin are never modified by tests.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import validate_core_gates as gates
from tests.test_workflow_rules import (
    artifact,
    render_handoff_contract,
    schema6_contract,
    standard_reviewer_assignment,
)


CHANGE = "fixture-external-owner"
PREV_ID = "codex-fixture-ext-owner"
NEW_ID = "grok-fixture-ext-owner"
EXEC_ID = "grok-fixture-ext-executor"
REVIEW_ID = "pi-fixture-ext-reviewer"
PREVIOUS_SHA = "ab" * 32


def owner(product: str, instance: str) -> dict:
    return {
        "agent_product": product,
        "agent_instance_id": instance,
        "agent_role": "control-plane",
        "capability_profile": "control-plane-high",
    }


class ExternalGrokControlPlaneTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.pin = self.root / "external-pin.json"
        self.real_pin = (
            Path(gates.__file__).resolve().parent.parent
            / "references" / "external-control-plane-rebinds.json"
        )
        self.local_pin = (
            Path(gates.__file__).resolve().parent.parent
            / "references" / "task-scoped-control-plane-rebinds.json"
        )
        self.real_pin_snapshot = (
            (self.real_pin.lstat().st_mode, self.real_pin.read_bytes())
            if os.path.lexists(self.real_pin)
            else None
        )
        self.assertFalse(self.local_pin.exists())
        self.handoff = (
            Path(gates.__file__).resolve().parent.parent / "references" / "handoff-contract.md"
        ).read_text(encoding="utf-8")
        self.patch = mock.patch.object(
            gates, "_external_rebind_pin_path", return_value=self.pin, create=True
        )
        self.patch.start()

    def tearDown(self):
        self.patch.stop()
        self.temporary.cleanup()
        after_snapshot = (
            (self.real_pin.lstat().st_mode, self.real_pin.read_bytes())
            if os.path.lexists(self.real_pin)
            else None
        )
        self.assertEqual(after_snapshot, self.real_pin_snapshot)
        self.assertFalse(self.local_pin.exists())

    def write_pin(self, payload) -> None:
        self.pin.write_text(json.dumps(payload, indent=2) + "\n")
        os.chmod(self.pin, 0o600)

    def assignment(self, product: str, instance: str, role: str, profile: str) -> dict:
        return {
            "agent_product": product,
            "agent_instance_id": instance,
            "agent_role": role,
            "capability_profile": profile,
        }

    def awaiting(self, plane: dict, revision: int = 4) -> dict:
        return schema6_contract(
            gates,
            self.handoff,
            change_id=CHANGE,
            lifecycle_state="awaiting-final-verification",
            current_batch=2,
            contract_revision=revision,
            last_review_result="pass",
            attempt_report_artifact=artifact("docs/agent-collab/fixture-external-owner/report.md"),
            last_review_artifact=artifact("docs/agent-collab/fixture-external-owner/review.md"),
            final_verification="pending",
            final_verification_artifact=None,
            final_review_result="pending",
            final_review_artifact=None,
            next_owner="openspec-superpower-change",
            control_plane_owner=plane,
            executor_assignment=self.assignment(
                "grok-cli", EXEC_ID, "executor", "cohesive-medium"
            ),
            reviewer_assignment=standard_reviewer_assignment("pi", REVIEW_ID),
        )

    def entry(self, new_owner: dict | None = None, previous_sha: str = PREVIOUS_SHA) -> dict:
        return {
            "amendment_kind": "external-control-plane-rebind",
            "scope": "this-change-only",
            "change_id": CHANGE,
            "previous_control_plane_owner": owner("codex", PREV_ID),
            "control_plane_owner": new_owner or owner("grok-cli", NEW_ID),
            "previous_status_sha256": previous_sha,
        }

    def moved(self, new_owner: dict | None = None) -> tuple[dict, dict, dict]:
        before = self.awaiting(owner("codex", PREV_ID), 4)
        after = self.awaiting(new_owner or owner("grok-cli", NEW_ID), 5)
        return before, after, self.entry(new_owner)

    def test_validator_source_has_no_session_or_business_change_id(self):
        source = Path(gates.__file__).read_text(encoding="utf-8")
        for needle in (
            "migrate-codex-a-session-memory",
            "cdfdcb20-8083-4d46-89bd-c73ef3f52fbe",
            "01a1bde9-12af-73c1-aa0b-e57cd905ea0b",
        ):
            self.assertNotIn(needle, source)

    def test_missing_empty_or_multiple_pin_rejects_grok_owner(self):
        _before, after, entry = self.moved()
        self.assertFalse(self.pin.exists())
        with self.assertRaisesRegex(AssertionError, "must use Codex"):
            gates.validate_handoff_contract(after, "missing-pin")
        self.write_pin([])
        with self.assertRaisesRegex(AssertionError, "must use Codex"):
            gates.validate_handoff_contract(after, "empty-pin")
        self.write_pin([entry, dict(entry, change_id="other-fixture-owner")])
        with self.assertRaisesRegex(AssertionError, "must use Codex"):
            gates.validate_handoff_contract(after, "multiple-pin")
        self.pin.unlink()
        gates.validate_handoff_contract(self.awaiting(owner("codex", PREV_ID)), "codex-without-pin")

    def test_matching_pin_allows_one_awaiting_owner_move_without_authority(self):
        before, after, entry = self.moved()
        digest = hashlib.sha256(render_handoff_contract(gates, before).encode()).hexdigest()
        entry["previous_status_sha256"] = digest
        self.write_pin([entry])
        self.assertIsNone(gates.validate_transition(
            before, after, "external-owner", previous_status_sha256=digest
        ))
        self.assertEqual(after["lifecycle_state"], "awaiting-final-verification")
        self.assertEqual(after["contract_revision"], before["contract_revision"] + 1)
        self.assertEqual((after["last_review_result"], after["final_verification"], after["final_review_result"]),
                         ("pass", "pending", "pending"))
        self.assertEqual(gates.validate_capability_action("cohesive-medium", "final-completion"), "BLOCKED")
        for action in ("destructive-git", "production-write", "release"):
            self.assertNotIn(action, json.dumps(after))
        verified = self.awaiting(owner("grok-cli", NEW_ID), 6)
        verified["final_verification"] = "pass"
        verified["final_verification_artifact"] = artifact(
            "docs/agent-collab/fixture-external-owner/final-verification.md"
        )
        gates.validate_transition(after, verified, "later-final-verification")
        with self.assertRaisesRegex(AssertionError, "previous status hash mismatch"):
            gates.validate_transition(
                before, after, "wrong-hash", previous_status_sha256="cd" * 32
            )

    def test_owner_equal_to_executor_or_reviewer_is_rejected(self):
        colliding = owner("grok-cli", REVIEW_ID)
        _before, after, entry = self.moved(colliding)
        self.write_pin([entry])
        with self.assertRaisesRegex(AssertionError, "differ from the reviewer"):
            gates.validate_handoff_contract(after, "reviewer")

        same_executor = owner("grok-cli", EXEC_ID)
        before, after_exec, entry_exec = self.moved(same_executor)
        digest = hashlib.sha256(render_handoff_contract(gates, before).encode()).hexdigest()
        entry_exec["previous_status_sha256"] = digest
        self.write_pin([entry_exec])
        self.assertIsNone(gates.validate_handoff_contract(after_exec, "executor"))
        self.assertIsNone(
            gates.validate_transition(
                before, after_exec, "executor-owner-move", previous_status_sha256=digest
            )
        )
        self.assertEqual(after_exec["lifecycle_state"], "awaiting-final-verification")
        self.assertEqual(after_exec["contract_revision"], before["contract_revision"] + 1)
        self.assertEqual(
            (
                after_exec["last_review_result"],
                after_exec["final_verification"],
                after_exec["final_review_result"],
            ),
            ("pass", "pending", "pending"),
        )

    def test_early_complete_is_rejected(self):
        before, after, entry = self.moved()
        after["lifecycle_state"] = "complete"
        after["final_verification"] = "pass"
        after["final_review_result"] = "pass"
        after["final_verification_artifact"] = artifact(
            "docs/agent-collab/fixture-external-owner/final-verification.md"
        )
        after["final_review_artifact"] = artifact(
            "docs/agent-collab/fixture-external-owner/final-review.md"
        )
        after["next_owner"] = "user"
        self.write_pin([entry])
        with self.assertRaisesRegex(AssertionError, "lifecycle must stay awaiting-final-verification"):
            gates.validate_transition(
                before, after, "early-complete", previous_status_sha256=PREVIOUS_SHA
            )

    def test_section_must_equal_pin_entry(self):
        _before, after, entry = self.moved()
        self.write_pin([entry])
        missing = render_handoff_contract(gates, after)
        with self.assertRaisesRegex(AssertionError, "External Control Plane Rebind"):
            gates.require_external_control_plane_section(missing, after, "missing-section")
        text = missing + (
            "\n## External Control Plane Rebind\n\n```json\n"
            + json.dumps(entry, indent=2)
            + "\n```\n"
        )
        gates.require_external_control_plane_section(text, after, "matching-section")
        wrong = dict(entry, scope="other-scope")
        drifted = missing + (
            "\n## External Control Plane Rebind\n\n```json\n"
            + json.dumps(wrong, indent=2)
            + "\n```\n"
        )
        with self.assertRaisesRegex(AssertionError, "must equal the pin entry"):
            gates.require_external_control_plane_section(drifted, after, "drifted-section")

    def test_lease_may_keep_previous_codex_owner(self):
        _before, after, entry = self.moved()
        self.write_pin([entry])
        lease_path = self.root / "docs" / "agent-collab" / CHANGE / "confirmation-lease.md"

        def write_lease(owner_instance: str) -> None:
            text = (
                "<!-- COOP_CONFIRMATION_LEASE_START -->\n"
                "```yaml\n"
                "decision_id: decision-001\n"
                "artifact_revision: 2\n"
                f"artifact_sha256: {'a' * 64}\n"
                "approved_scope: approved source implementation\n"
                "approved_actions:\n"
                "  - run-safe-tests\n"
                "risk_profile: standard\n"
                "decision_source: ai-proposed/user-approved\n"
                f"owner_instance_id: {owner_instance}\n"
                "status: valid\n"
                "invalidation_conditions:\n"
                "  - scope-change\n"
                "```\n"
                "<!-- COOP_CONFIRMATION_LEASE_END -->\n"
            )
            lease_path.parent.mkdir(parents=True, exist_ok=True)
            lease_path.write_text(text, encoding="utf-8")
            after["confirmation_lease"] = {
                "decision_id": "decision-001",
                "path": f"docs/agent-collab/{CHANGE}/confirmation-lease.md",
                "sha256": hashlib.sha256(lease_path.read_bytes()).hexdigest(),
            }

        write_lease(PREV_ID)
        gates._validate_confirmation_lease_artifact(after, self.root, "previous-owner-lease")
        write_lease("codex-fixture-ext-other")
        with self.assertRaisesRegex(AssertionError, "does not match control plane"):
            gates._validate_confirmation_lease_artifact(after, self.root, "foreign-lease")

    def test_bad_pin_shapes_fail_closed(self):
        before = self.awaiting(owner("codex", PREV_ID))
        entry = self.entry()
        self.write_pin([entry])
        os.chmod(self.pin, 0o644)
        with self.assertRaisesRegex(AssertionError, "0600"):
            gates.validate_handoff_contract(before, "mode")
        self.pin.write_text("{")
        os.chmod(self.pin, 0o600)
        with self.assertRaisesRegex(AssertionError, "invalid JSON"):
            gates.validate_handoff_contract(before, "json")
        self.pin.write_text(
            '[{"amendment_kind":"external-control-plane-rebind","amendment_kind":"x"}]\n'
        )
        os.chmod(self.pin, 0o600)
        with self.assertRaisesRegex(AssertionError, "duplicate JSON key"):
            gates.validate_handoff_contract(before, "duplicate")
        link = self.root / "linked-pin.json"
        link.write_text("[]\n")
        os.chmod(link, 0o600)
        self.pin.unlink()
        self.pin.symlink_to(link)
        with self.assertRaisesRegex(AssertionError, "non-symlink"):
            gates.validate_handoff_contract(before, "symlink")
