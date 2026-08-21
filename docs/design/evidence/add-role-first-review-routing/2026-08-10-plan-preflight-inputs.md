# add-role-first-review-routing Plan Preflight Inputs

## Boundary

- observed_at: 2026-08-10 to 2026-08-11, Asia/Shanghai; revision 4 finalized on 2026-08-11
- mode: approved implementation / planning and recovery preparation only
- file_mutation_before_this_record: implementation source `no`; runtime `no`
- git_command_performed: `no`
- pi_command_performed: `no`
- canonical_state_or_archive_mutation: `no`
- authority: user approved `add-role-first-review-routing` current contract
- result_authority: input binding only; this record is not Plan Preflight PASS,
  source Review, sync-plan Review, runtime authorization, or completion evidence

## Approved OpenSpec binding

| Artifact | SHA-256 |
|---|---|
| `proposal.md` | `970fdbb94fbbc3454db620ef2b2475b4ddb327042ad303c938d268b4710a9330` |
| `design.md` | `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480` |
| `tasks.md` | `764a5401f7f5ec86348f3bfcabb854b196b26793b1b842b236f3731eafa7ffea` |
| spec delta | `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384` |

Independent Proposal Review returned `PASS` with no P0/P1/P2 finding. The user
then supplied the exact authorization phrase `批准实施 add-role-first-review-routing 当前合同`.
The OpenSpec task checkboxes remain byte-frozen at the reviewed revision until
post-Preflight execution tracking; this avoids rewriting the approved input
before its Plan is independently reviewed.

## Plan binding

| Path | SHA-256 |
|---|---|
| `docs/superpowers/plans/2026-08-10-add-role-first-review-routing.md` | `d621b09ad030dfdfd02ad45478ad7156486fc63c392ef0816cb99bc252af6a23` |

The plan contains an exact source file allowlist, current/legacy schema split,
TDD steps, commands and expected results, four-target order, Review assignments,
rollback/stop conditions, no-Git boundary, and Completion Contract handback.

Plan Preflight revision 1 returned `BLOCKED` with `PF-001` and `PF-002`.
Revision 2 also returned `BLOCKED`: `PF-001` identified the wrong compact reason
field plus a duplicated misplaced paragraph; `PF-002A` identified the broken
post-apply verification/restore boundary; `PF-002B` identified incomplete
hidden/Review no-Git coverage and unspecified safe extraction.

Revision 3 returned `BLOCKED` with `PF3-001`: the receipt was first persisted
after destination mutation, leaving a hard-interruption window without an
admissible recovery record.

This revision 4 changes no implementation source. It retains the prior compact,
complete-tree, source-delta, and post-apply restore corrections, and adds a
durable pre-mutation transaction state machine. The verified target-local
backup is fsynced before a mode-`0600` `prepared` receipt; that receipt advances
durably to `mutation-intent` before the first destination write; recovery rules
cover `prepared`, partial mutation, and `applied-uncommitted`; atomic receipt
replacement, fsync ordering, orphan handling, `recovery-blocked`, and four
process-interruption tests are explicit. All prior verdicts remain historical
evidence and authorize nothing; revision 4 requires a fresh full Review.

## Router source preimages

| Path | SHA-256 |
|---|---|
| `SKILL.md` | `011f9f7c6cc02204d2c968ff024b949416ebfcca69aee9d4e3a1196fd40e9a91` |
| `CONTEXT.md` | `bd3d243936fd8e0b33d5f871ec1faf26127968dd369ce9cca8a2084cf10523cd` |
| `README.md` | `8118b8bdb6445f3ac2856cf049e7da8811e21e52ddb77c68fb62ac44dc41fa9e` |
| `README_cn.md` | `1db809c692c8108877e0ebdf173f6426be9e7f8440b6679ab3b06094eb2dc80d` |
| `CHANGELOG.md` | `e41c73eeb630576bfc9182f0bcadba7eada38980b42831781678d93acc87ca74` |
| `references/approved-implementation-workflow.md` | `1e354d5435942cf487b07a8f757a2a2d03f4d0e436c385cb43cf5d5adbc7c32c` |
| `references/agent-capability-routing.md` | `daa8bb5d3d8e468289e520420a23430e0d62c0f2914f9ca5c0ee67e9ced00164` |
| `references/completion-contract.md` | `a8da4f27997acd832abe6d936945ea0b6a5c3c164a920a8ca21fded652920f0b` |
| `references/cross-cli-portable-manifest.json` | `678467379a148aedc66ef164275f1e51c6ca546a5a6dcbf19fe03f07ac542e69` |
| `references/cross-cli-sync.md` | `153bd6b843b4ec965aa53adf3587a75ce73e2fb2c7c92b4a6cce4fb321ca30f9` |
| `references/handoff-contract.md` | `62dfe033d0c6f8b6e0fde79e32f44c97a4da1efca7913def3378bcd16c5e2340` |
| `references/request-modes.md` | `27ae6696e443c165e40646312a0cd6b28f2124d6c52823a5bba886840aa90d99` |
| `references/response-patterns.md` | `488ad07ad9353f862e9a81141ba7323e4718efd52a4f494cbf4e4eb213c63576` |
| `references/self-evolution-rule.md` | `db1aa163103d866edbf593f6781d573a91afcd312b926a30f8620141f495e91a` |
| `references/shared-global-governance.md` | `96158069ce5b7287e628d4f02b2d1f313a62f7cf9c50d9b6ebf068bf9829e537` |
| `references/step-evidence-gate.md` | `4b281f5d53ab675b96a677f96b6049d0e97890a522a6ca8babaf2aa5985e71f4` |
| `references/superpowers-adapter.md` | `bf04ff76f57f8826b6ad68394ffff8010d12a3cf7c8c6cb2d7000836d4268a7a` |
| `references/sync-checklist.md` | `ece284165dee9e923c59ae152b34f39ba2d4980793c0347b6bd1d105582a4d62` |
| `scripts/validate_core_gates.py` | `71839b76491f099c0f178effa90e8d76b95a08f36356286f7000bf600c5e68c8` |
| `scripts/validate_cross_cli_sync.py` | `7c6248b3f34cf94b8ea2930f65a30c768970d0a38b666268d72fe5f6016acdd0` |
| `tests/test_workflow_rules.py` | `c6c120ff5d5237fa54f50bcf28b2c108bde253a246e9bffd60cc334597625916` |
| `tests/test_cross_cli_sync.py` | `4799819c0e1647d4c9b660abf0d75e6e566849cf0a3f9596c670a27518dee2d6` |

Expected absent creation paths at this boundary:

- `tests/fixtures/role-first-review-routing-cases.json`
- `tests/fixtures/role-first-review-routing-output.schema.json`
- `tests/run_role_first_review_forward_tests.py`

## Companion source preimages

| Path | SHA-256 |
|---|---|
| `SKILL.md` | `fb0c3c2157415674df41147ebc415e701d45f6d894d10c763117dc3253d95e00` |
| `README.md` | `36f1acfa26d94734f748c685ac43615eb1455cdcc046a0159c90f0a2cd4f80c3` |
| `README_cn.md` | `6ce70c219e017d9dfecd8b36001fac1143284fd2e82c4edc8cdd510cce8af20d` |
| `CHANGELOG.md` | `b1bef994bcfd43806e2e8a1872f97d4ec29f49e6b7279789f15ec4edae33c663` |
| `agents/openai.yaml` | `dbb8718a64e74c782cde3a1ac0ca19c3f52994adebd5481723fb1fcc2a3b782b` |
| `references/agy-dispatch-template.md` | `8049e8d4b7b806220f74a9e4d79ec303483c0280e9c78768f54bb109fc078956` |
| `references/brief-template.md` | `05222e566e8d436a25b32e0cca1a871469fe5f72ea5511ed878c7a500fb008b0` |
| `references/handed-off-external-execution.md` | `3d4d0b25a0312c6f21d682044af2296a5a9541c8a7bade2bb382b4fcc8b02bf7` |
| `references/handoff-contract.md` | `62dfe033d0c6f8b6e0fde79e32f44c97a4da1efca7913def3378bcd16c5e2340` |
| `references/report-template.md` | `20ea0d2308c5d108901a4e9e3d772d766baf9a9f8e6a6eb1f8d9623afc40b9b5` |
| `references/review-template.md` | `7a6d6dfd9f339edcf722d3d79590ef982c85ca1a08d17195a86d1f652ab1cea5` |
| `references/timeout-audit-template.md` | `84d5b94226a084467d69c605422f687a55cadb653890055c54563788387b11df` |
| `scripts/validate_templates.py` | `0f193805ba5d480443e21b5f1ad4e5c9598f0265cf95d58b6ce2805bb4333aa8` |
| `tests/test_workflow_rules.py` | `2f93a71f2a4532174b10aa29a8705d996b979f11cf9393e8f5e5530c3c4c18be` |

## Structured source backups

| Archive | Mode | Entries | SHA-256 |
|---|---:|---:|---|
| `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/router-source-preflight-r4.tar` | `0600` | `27` | `a0b7a36e0964fe8e6b93bbcb24a2454bab1c3376159f7cd55f710054d464c491` |
| `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/companion-source-preflight.tar` | `0600` | `14` | `3deab7e813efca3de22ff7d583a5ae089eec079c63842239d9adb85191fb4acc` |

The parent root is mode `0700`. Archives retain repository-relative paths and
contain only the approved existing source/contract/plan inputs listed by the
Plan; they contain no Git metadata, credentials, sessions, model settings,
caches, logs, binaries, or runtime global-rule bytes.

The revision-1 through revision-3 Router archives remain present as superseded
recovery history; none is an input to revision 4 or cleanup authorization.

## Non-Git full-tree baselines

These mode-`0600` JSON inventories were generated after the final Plan revision
and before source implementation. Records cover relative path, kind, mode,
size, and non-sensitive SHA-256 without file contents. Both inventories include
hidden files such as `.gitignore` and exclude only the root `.git` entry. All 17
existing Router Review files are present. Companion has no path exclusion.

Router excludes exactly two planning artifacts that must be updated after the
baseline is generated: the Preflight record and its Review prompt. Their fresh
SHA values are bound directly by the Review prompt, and the source-start
inventory captured after accepted Plan Review includes them with no exclusion.

| Inventory | Records | SHA-256 |
|---|---:|---|
| `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/router-tree-preflight-r4.json` | `320` | `f5506db159dd77fe5b9401a20a77d9796183f5515c0e20abb466147f8dc3f859` |
| `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/companion-tree-preflight-r4.json` | `29` | `cf4924df7707cf665d41de48300eb59ce8097f0ee0dd298fd7039e5db625b064` |

They are comparison evidence only, not Git status and not restore inputs. The
Plan gives the exact complete source-start capture and delta commands.

## Machine bindings and exact source-delta allowlist

| Artifact | Mode | Entries | SHA-256 |
|---|---:|---:|---|
| `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/source-delta-allowlist-r4.txt` | `0600` | `45` | `ad6531d92126e6c5e07c2251bff1e535b9f308f382f64541dff2b3e8ebaab3d6` |
| `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/preflight-source-bindings-r4.json` | `0600` | schema `1` | `4fde9680e9d43f8268ef66ea9c31c10f3b92899d6930d5f6bb5d371ccad0c2fe` |

The allowlist has no wildcard and no duplicate; it names each permitted Router
or Companion source/evidence/task path for the source phase. The bindings JSON
contains the exact Plan, backup, baseline, and allowlist paths/hashes/modes/
counts used by `source-delta`. Neither artifact grants implementation or
restore authority.

## Known Handoff inventory

Read-only `rg --files -g 'docs/agent-collab/**/status.md'` was run in:

- Router source repository;
- Companion source repository;
- current `ai_app` project root.

Result: zero canonical `status.md` files in these known roots. This is a
Preflight observation only. The source High Review must be followed by a fresh
all-known-root drain inventory, repeated immediately before runtime apply.

## Runtime observed preimages

The following inventory digest method walks only each governed Skill directory,
does not follow symlinks, and hashes sorted records of relative path, type, mode,
size, and regular-file SHA-256. It does not print file contents.

| Target | Governed path | Files | Symlinks | Inventory SHA-256 |
|---|---|---:|---:|---|
| Codex | `/Users/elvis/.codex/skills/openspec-superpower-change` | 31 | 0 | `bb2533745f0297f52e5ad35e800c7688be7c86c36ed2e234a59c2a9871d7d67e` |
| Codex | `/Users/elvis/.codex/skills/codex-brief-antigravity-review` | 12 | 0 | `e00ef88a7db136d308f470307dbd3a6b4558e5685f4a29781a69cee67c72b898` |
| Pi | `/Users/elvis/.pi/agent/skills/openspec-superpower-change` | 31 | 0 | `5d1722ecce680a9d0f68b034df23199c551ea9b9e5956a85754bf80db0188520` |
| Pi | `/Users/elvis/.pi/agent/skills/codex-brief-antigravity-review` | 12 | 0 | `4ca0637f6da2aaa286d1d4eb44621d77b674cadfa08f6643aad7968beca80e1c` |
| Antigravity | `/Users/elvis/.gemini/antigravity-cli/skills/openspec-superpower-change` | 32 | 0 | `ffe2248d89cf853789549f68f4f41a926ef189626f0762a53eb849a67b25e954` |
| Antigravity | `/Users/elvis/.gemini/antigravity-cli/skills/codex-brief-antigravity-review` | 15 | 0 | `ca2fa37867ffffe128264497149b22f24dc4af5fb71f1c1b166db773d9f84407` |
| Grok | `/Users/elvis/.grok/skills/openspec-superpower-change` | 29 | 0 | `dcb4e28e956630d8a273eaa8e959af226cb9b12febd2fd45db8ae9eba0617adc` |
| Grok | `/Users/elvis/.grok/skills/codex-brief-antigravity-review` | 10 | 0 | `767f9f5ef273af0659830ed3c72409149f26cb85ab917403a76710e726c8dfd5` |

Global-rule preimages (content not printed):

| Target | Path | File SHA-256 | Managed prestate |
|---|---|---|---|
| Codex | `/Users/elvis/.codex/AGENTS.md` | `8985a13981a72a300430ed56368af288526ef4d88e47a43b25e68bdc56be32f1` | v5, 15 IDs, body `1f1eda4a9f93022135e255542594351a0239b5921e0b36e4294268c14628fc8d` |
| Pi | `/Users/elvis/.pi/agent/APPEND_SYSTEM.md` | `5ed58a7632f69298522b9a6871c8854a81d1bfd81f24b8e232a1be0b083ee2a8` | no managed marker pair observed; first governed apply must preserve all existing native bytes and append exactly one reviewed v6 block |
| Antigravity | `/Users/elvis/.gemini/GEMINI.md` | `17835ec162117680aeb700ec548b9bf4a05d8a1ae3427babfbe427242d079a4f` | v5, 15 IDs, same body hash |
| Grok | `/Users/elvis/.grok/AGENTS.md` | `d8cc710655ea2356b6b3a4bd7356950bfe9edc89cc18ce29c3e77e3029f5efe8` | v5, 15 IDs, same body hash |

Codex resolution note: process `CODEX_HOME` is
`/Users/elvis/.codex-account-a`, but that directory has neither governed Skill
nor `AGENTS.md`. The discovered `.agents/skills` entries are symlinks to the
real `/Users/elvis/.codex/skills` directories. The Plan therefore binds the
candidate Codex runtime target to `/Users/elvis/.codex`; `.agents` symlinks are
outside the mutation set and must remain unchanged.

These runtime values are observed preimages, not apply authorization. Candidate
source High Review, fresh destination guards, legacy drain, path/hash sync plan,
and independent Sync-plan Review remain mandatory before any runtime mutation.

## Active OpenSpec isolation

`openspec list` observed:

- `add-role-first-review-routing`: `3/41` tasks;
- `add-codex-skill-update`: `14/40` tasks.

The second active change is unrelated and excluded from modification, cleanup,
reconciliation, archive, or runtime authority in this plan.

## Preflight stop conditions

- Any Plan/approved-artifact/source/backup/full-tree-baseline/bindings/allowlist hash drift.
- Any absent creation path becomes occupied.
- Any non-allowlisted source edit would be required or overwritten.
- Any runtime path resolves through an unreviewed symlink or outside its root.
- Any active schema-4/schema-5 Handoff remains at the runtime deployment gate.
- Any Pi native-root command or sensitive/native-state access would be required.
- Any required validation or independent Review returns `BLOCKED`.
