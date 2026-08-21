# Isolated Pi Adversarial Review — add-role-first-review-routing

## Reviewer Assignment

- Review purpose: adversarially decide whether the candidate preserves
  product-neutral role parity, exact reviewer assignment and evidence identity,
  current/legacy isolation, and complete four-target deployment and recovery
  safety; identify any actionable blocker.
- Reviewer product: `pi`.
- Reviewer role: `independent-reviewer`.
- Capability profile: `control-plane-high`.
- Instance-independence requirement: this isolated process is fresh, has no
  inherited context or Skills, and is distinct from every author, executor,
  prior reviewer, Pi target process, and canonical decision owner.
- Result authority: governed adversarial Review evidence only. You cannot
  mutate source/runtime, accept your own result, update canonical state,
  authorize promotion, or claim completion.

## Bound evidence

Change: `add-role-first-review-routing`.

- approved implementation Plan SHA-256:
  `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229`;
- accepted P1 R5 source Review SHA-256:
  `073a367b6fa82e512bcb16df8c4f95152c9f9db76cd3c360201d36cc122dd9b4`;
- accepted P1 R5 runtime Sync-plan Review SHA-256:
  `b0714b11b826de230bea71e909ffaea916953ada136188ad7df11a1c6502c886`;
- runtime Sync-plan Review input SHA-256:
  `213d8166583978c17d87136953385e0756e46d176b0204c326590fad086494c1`;
- reviewed runtime plan SHA-256:
  `6ae0cc4dcca9fbc8de9d1e4c1fc050d0fcc4dc7bde445a6bda85bb6845a51156`;
- corrected sync validator SHA-256:
  `332de6171495faa12b3acd6c7c39e8ee35972a9c87eebe216d9581cc3b520044`;
- corrected cross-CLI tests SHA-256:
  `97d46aec7247ab9e0f93d60b2c017248e22e4b54d2c53f3f01eaa83d0c9b1ed2`;
- verified receipt SHA-256 values:
  - Codex: `7342f5ebab105de531b475592235d7a3179e25ec00e86442196fb3fdbb3de803`;
  - Pi: `670fa2279ae30a90ab1f4f470983fcd493b86a1b24a666735105c1aaff761e05`;
  - Antigravity CLI: `3338354fdd5fa9e0cf2b9d1eb0c8fa0c8d8fdad1e375e20ebd5b6d452b6392bd`;
  - Grok CLI: `76194a63735b869702c858ecee1f100c713b4099df92ba0ca18b504a743779c1`.

The control plane reports fresh `verify-all: pass` in exact order
`codex → pi → antigravity-cli → grok-cli`; all four receipts are state
`verified`, bind the reviewed plan SHA, and contain both content and discovery
verification digests. Legacy inventory reports zero active records.

## Read-only review scope

Read only the two supplied candidate roots. Inspect actual Router/Companion
instructions and Skills, OpenSpec/Plan, source and runtime-plan Reviews,
portable manifest, shared governance, sync contracts, production validators,
tests, fixtures, and public guidance.

Adversarially check:

1. concrete purpose/product/role/profile/independence/authority binding and
   product-neutral eligibility for Codex, Pi, Antigravity CLI, and Grok CLI;
2. evidence identity, self-review prevention, control-plane authority, and
   schema-6 current versus frozen legacy separation;
3. exact four-target order, manifest closure, managed-v6 semantics, portable
   parity, discovery, sensitive exclusions, and later-target gating;
4. destination/preimage identity, parent creation, backup and transaction-root
   containment, durable receipts, rollback, restore, blocked recovery, and
   failure-before-later-target behavior;
5. whether the reported hashes and Review evidence support final progression,
   or whether any concrete P0/P1/P2 issue remains.

Do not attempt writes, network access, native Pi-root access, external process
execution, or reading outside the supplied roots. Do not include private native
paths, confidential values, environment output, raw traces, or source contents
in the result.

## Required output

Return exactly one JSON object and no Markdown or surrounding text:

```json
{
  "verdict": "PASS",
  "findings": []
}
```

The only verdicts are `PASS` and `BLOCKED`. Use `PASS` only when there is no
actionable finding. Otherwise use `BLOCKED` and include every finding as an
object with exactly these non-blank string fields:

```json
{
  "severity": "P1",
  "category": "concise-safe-category",
  "location": "relative-path:line",
  "summary": "concise software-correctness finding",
  "required_action": "exact correction and resume condition"
}
```

Keep the output sanitized and path/category-only. Do not grant authority to
your own verdict.
