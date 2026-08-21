#!/usr/bin/env python3
"""Regression tests for source-bootstrap parent-link phase accounting."""

import ast
import importlib.util
import json
import pathlib
import unittest


HELPER_PATH = pathlib.Path(__file__).with_name("source-bootstrap-v2-helper.py")
PRESTATE_PATH = pathlib.Path(__file__).with_name("source-bootstrap-v2-prestate.json")
SPEC = importlib.util.spec_from_file_location("source_bootstrap_v2_helper", HELPER_PATH)
HELPER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HELPER)

EXPECTED_DELTAS = {
    "approval-recorded": {
        HELPER.APPROVAL_DIR: 1,
    },
    "journal-ready": {
        HELPER.APPROVAL_DIR: 2,
        HELPER.SOURCE_BOOTSTRAP_DIR: 1,
    },
    "post-bootstrap": {
        HELPER.APPROVAL_DIR: 2,
        HELPER.SOURCE_BOOTSTRAP_DIR: 1,
        HELPER.GIT_DIR + "/refs/heads": 1,
        HELPER.GIT_DIR + "/logs/refs/heads": 1,
        HELPER.GIT_DIR + "/worktrees": 1,
        HELPER.TARGET_PARENT: 1,
    },
}


class ParentLinkPhaseTests(unittest.TestCase):
    def test_phase_table_is_an_exact_closed_map(self):
        self.assertEqual(HELPER.PARENT_NLINK_DELTAS, EXPECTED_DELTAS)

    def test_current_prestate_baseline_and_every_phase_delta(self):
        raw = PRESTATE_PATH.read_bytes()
        self.assertTrue(raw.endswith(b"\n"))
        prestate = json.loads(raw[:-1])
        baseline = {entry["path"]: entry["nlink"] for entry in prestate["parent_closure"]}
        self.assertEqual(len(baseline), 23)
        self.assertEqual(baseline[HELPER.APPROVAL_DIR], 8)
        self.assertEqual(baseline[HELPER.SOURCE_BOOTSTRAP_DIR], 3)
        self.assertEqual(
            HELPER.expected_parent_nlink(HELPER.APPROVAL_DIR, 8, "approval-recorded"),
            9,
        )
        self.assertEqual(
            HELPER.expected_parent_nlink(HELPER.APPROVAL_DIR, 8, "journal-ready"),
            10,
        )
        self.assertEqual(
            HELPER.expected_parent_nlink(HELPER.APPROVAL_DIR, 8, "post-bootstrap"),
            10,
        )
        for phase, deltas in EXPECTED_DELTAS.items():
            for path, value in baseline.items():
                with self.subTest(phase=phase, path=path):
                    self.assertEqual(
                        HELPER.expected_parent_nlink(path, value, phase),
                        value + deltas.get(path, 0),
                    )

    def test_all_validation_calls_bind_the_required_phase(self):
        tree = ast.parse(HELPER_PATH.read_text(encoding="utf-8"))
        functions = {
            node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)
        }

        def literal_phases(function_name, callee):
            phases = []
            for node in ast.walk(functions[function_name]):
                if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
                        node.func.id == callee):
                    phases.append(ast.literal_eval(node.args[-1]))
            return phases

        self.assertEqual(
            literal_phases("main", "validate_prestate"),
            ["approval-recorded", "approval-recorded", "journal-ready"],
        )
        self.assertEqual(
            literal_phases("main", "verify_retained_bindings"),
            ["approval-recorded", "journal-ready", "post-bootstrap"],
        )
        self.assertEqual(
            literal_phases("validate_prestate_post_only", "expected_parent_nlink"),
            ["post-bootstrap"],
        )

        validate = functions["validate_prestate"]
        retained = functions["verify_retained_bindings"]
        self.assertEqual(validate.args.args[-1].arg, "phase")
        self.assertEqual(retained.args.args[-1].arg, "phase")
        self.assertFalse(validate.args.defaults)
        self.assertFalse(retained.args.defaults)

    def test_unlisted_parent_has_zero_delta_in_every_phase(self):
        for phase in EXPECTED_DELTAS:
            with self.subTest(phase=phase):
                self.assertEqual(
                    HELPER.expected_parent_nlink(HELPER.ROOT, 20, phase),
                    20,
                )

    def test_unknown_phase_fails_closed(self):
        with self.assertRaises(HELPER.Blocked):
            HELPER.expected_parent_nlink(HELPER.ROOT, 20, "unexpected")


if __name__ == "__main__":
    unittest.main()
