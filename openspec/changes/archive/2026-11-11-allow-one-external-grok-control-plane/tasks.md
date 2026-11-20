# Tasks

- [x] Record approval of change-id `allow-one-external-grok-control-plane` before any validator edit.
- [x] Add a failing test: an external handoff with a Grok owner is rejected when the external pin is absent.
- [x] Add the external pin parser and the one-field owner transition. Do not create a production pin in the test fixture directory only.
- [x] Prove the accepted transition stays `awaiting-final-verification`, increments revision by one, and rejects `complete`.
- [x] Prove a new owner equal to the bound reviewer is rejected and a new owner equal to the executor is accepted when the pin matches.
- [x] Run `openspec validate allow-one-external-grok-control-plane --strict` and the skill core-gate validator.
- [x] Do not edit canonical status for `migrate-codex-a-session-memory` in this change.
