## MODIFIED Requirements

### Requirement: Scope-bound cross-CLI synchronization plans

The workflow SHALL verify Grok's native Skill discovery against the active
source paths reported by `grok inspect --json`. Default `user` discovery SHALL
continue to require the planned Grok Skill root. A `configToml` source MAY be
accepted only when all expected Skills resolve beneath one consistent root that
equals a `skills_root` in the same reviewed plan, the corresponding target has
a verified same-plan receipt before Grok discovery is accepted, and the full
portable closure at that source root matches canonical content.

Configured-source evidence SHALL bind the observed source type, root, expected
paths, canonical content, and source-target receipt digest. The verifier SHALL
reject mixed source types or roots, an unplanned root, an unverified or
different-plan source receipt, missing Skills, or content drift. It SHALL NOT
read or mutate Grok configuration to manufacture discovery evidence.

#### Scenario: Grok discovers the verified Codex Skill root

- **GIVEN** native Grok configuration points both expected Skills at the Codex
  Skill root bound by the same sync plan
- **AND** the Codex target receipt is verified under that plan with full parity
- **WHEN** Grok discovery verification consumes native inspect evidence
- **THEN** the configured source paths and source receipt are included in the
  discovery digest
- **AND** Grok discovery may pass without modifying Grok configuration

#### Scenario: Configured discovery is not transaction-bound

- **WHEN** native inspect reports mixed roots/types, a root absent from the
  reviewed plan, an unverified source target, a different-plan receipt, or
  canonical content drift
- **THEN** Grok discovery is `BLOCKED`
- **AND** no configured path is trusted merely because native output reports it
