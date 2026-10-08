"""Regression tests for the existing routing probe's selection evidence."""

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


def load_runner():
    spec = importlib.util.spec_from_file_location(
        "routing_runner", ROOT / "tests/run_superpowers_routing_forward_tests.py"
    )
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    return runner


class SuperpowersSelectionEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.runner = load_runner()
        self.schema = json.loads(
            (ROOT / "tests/fixtures/superpowers-routing-output.schema.json").read_text()
        )
        self.schema["required"].append("selection_evidence")
        self.schema["properties"]["selection_evidence"] = {
            "type": "object", "additionalProperties": False,
            "required": ["record_kind", "reason"],
            "properties": {
                "record_kind": {"enum": ["gate-0", "bypass"]},
                "reason": {"enum": [
                    "ordinary-answer-no-workflow",
                    "fully-specified-proposal-no-implementation-phase",
                    "compact-restoration-existing-cause-and-regression",
                    "explicit-method-request-no-authority",
                ]},
            },
        }
        self.proposal = {
            "route": "openspec-proposal", "result": "stop-for-approval",
            "selected_superpowers": [], "state_change_allowed": False,
            "git_authorized": False, "completion_owner": "router",
            "selection_evidence": {
                "record_kind": "gate-0",
                "reason": "fully-specified-proposal-no-implementation-phase",
            },
        }

    def test_accepts_auditable_nonselection_without_changing_route(self):
        try:
            actual = self.runner.validate_observed(self.proposal, self.schema)
        except self.runner.ProbeFailure as exc:
            self.fail(f"Selection evidence was rejected: {exc}")
        self.assertEqual(actual["selected_superpowers"], [])
        self.assertEqual(actual["selection_evidence"], {
            "record_kind": "gate-0",
            "reason": "fully-specified-proposal-no-implementation-phase",
        })

    def test_missing_or_malformed_selection_reason_fails_closed(self):
        mutations = [None, {}, {"record_kind": "gate-0", "reason": ""},
                     {"record_kind": "gate-0", "reason": True},
                     {"record_kind": "gate-0", "reason": "unknown"},
                     {"record_kind": "bypass", "reason": "ordinary-answer-no-workflow"},
                     {**self.proposal["selection_evidence"], "authority_granted": True}]
        for evidence in mutations:
            with self.subTest(evidence=evidence):
                observed = copy.deepcopy(self.proposal)
                if evidence is None:
                    observed.pop("selection_evidence")
                else:
                    observed["selection_evidence"] = evidence
                with self.assertRaisesRegex(self.runner.ProbeFailure, "selection evidence"):
                    self.runner.validate_observed(observed, self.schema)

    def test_route_match_without_matching_reason_is_not_pass(self):
        observed = copy.deepcopy(self.proposal)
        self.assertEqual(self.runner.compare_expected(self.proposal, observed), [])
        observed["selection_evidence"]["reason"] = "explicit-method-request-no-authority"
        self.assertIn("selection_evidence mismatch", self.runner.compare_expected(self.proposal, observed))

    def test_case_selection_preserves_order_and_rejects_unknown_or_duplicate_ids(self):
        select = getattr(self.runner, "select_cases", None)
        self.assertTrue(callable(select), "Existing runner must support a bounded case selection")
        cases = [{"id": "ordinary_question"}, {"id": "proposal_only"}, {"id": "direct_change"}]
        self.assertEqual([c["id"] for c in select(cases, ["direct_change", "ordinary_question"])],
                         ["ordinary_question", "direct_change"])
        for ids in (["unknown"], ["proposal_only", "proposal_only"]):
            with self.assertRaises(self.runner.ProbeFailure):
                select(cases, ids)

    def test_native_probe_uses_requested_model_and_high_reasoning(self):
        captured = []
        trace = "\n".join(json.dumps(event) for event in [
            {"type": "thread.started"}, {"type": "turn.started"},
            {"type": "item.completed", "item": {"type": "agent_message"}},
            {"type": "turn.completed"},
        ])

        class ProbeProcess:
            pid = 424242
            returncode = 0

            def __init__(self, command, **kwargs):
                captured.append(command)
                output = Path(command[command.index("--output-last-message") + 1])
                output.write_text("A set holds unique values. A list preserves order.")

            def communicate(self, timeout):
                return trace, ""

        case = {
            "id": "ordinary_question", "prompt": "What is a set versus a list?",
            "fixture": {"router": False, "superpowers": []},
            "expected": {"route": "direct", "result": "answer", "selected_superpowers": [],
                         "state_change_allowed": False, "git_authorized": False, "completion_owner": "none"},
        }
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(
            self.runner.subprocess, "Popen", ProbeProcess
        ):
            root = Path(tmp)
            schema = copy.deepcopy(self.schema)
            schema["required"].remove("selection_evidence")
            schema["properties"].pop("selection_evidence")
            result = self.runner.run_case(case, root, root / "rule.md", root,
                                          root / "schema.json", schema, root / "account", root)
        self.assertEqual(result["status"], "PASS")
        command = captured[0]
        self.assertIn("--model", command)
        self.assertEqual(command[command.index("--model") + 1], "gpt-6.1-sol")
        self.assertIn('model_reasoning_effort="high"', command)
        self.assertNotIn('model_reasoning_effort="low"', command)


if __name__ == "__main__":
    unittest.main()
