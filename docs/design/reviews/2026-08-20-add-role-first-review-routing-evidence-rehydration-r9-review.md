# Add Role-First Review Routing — R9 Evidence-Rehydration Preflight Review

Verdict: PASS

Decision scope: exactly R9 Plan Preflight for Task 6 Steps 5A–6.

## Input verification

- Read all six primary inputs completely. The Plan SHA is
  `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229`;
  the R9 input SHA is
  `dcc8658bb014a0e7140a5a4e0eda733f921544c2911422e0bc2d8fef183d2903`.
  Both match the review prompt. The prompt remained SHA
  `bd31f6fe47ac426961b5830b3dde27d45056c7b0f0928e4aecb5b991ce9f76e7`.
- The target R9 Review artifact was absent at review start and end. Step 5A
  recovery, Step 6 compare/delta outputs, and runtime outputs remained absent.
- The private root is a real mode-`0700` directory. Every bound top-level
  artifact is regular mode `0600`; all prompt-specified hashes match, including
  script, manifest, bindings, compatibility receipt, continuity receipt,
  archives, inventories, and allowlist.
- All 36 preimages—22 Router and 14 Companion—match every durable R4 path/SHA
  pair. Their 36 private objects are unique mode-`0600` files. The two archives
  contain exactly those unique, relative, regular members: 22 and 14, with no
  links, traversal, absolute paths, or extra members.
- Provenance is exact: six Router full object IDs and four Companion
  `HEAD:<path>` specifications, expressed as exactly ten
  `git -C … cat-file blob …` commands. Every resulting byte SHA matches the
  durable R4 value. All 26 non-Git sources remain regular, non-symlink files
  with matching SHA.
- The earlier diagnostic `git fsck`, `git show`, and `git cat-file` deviation
  is explicitly disclosed in the R9 input and Plan; it is not rewritten as
  compliant history. The reviewer ran no Git command.
- The original pre-R9 and fresh pre-r2 current-tree archives are regular mode
  `0600`, match their recorded hashes, contain only relative regular/directory
  members, exclude `.git`, and were listed without extraction. Member counts
  are Router `344/345` and Companion `30/30`.
- Reconstructed baselines contain Router `341` and Companion `29` records.
  They differ from Preflight exactly by the 36 durable preimage projections,
  the three documented absent Router paths, and the old generated-cache record;
  all other records are unchanged.
- Preflight inventories contain Router `344` records with exactly two
  exclusions and Companion `29` records with none. The only live non-directory
  delta from the preparation snapshot is the R9 input's pre-dispatch
  finalization from SHA
  `e4e44681a4b914528edb798bf747d8e395953cf2a96e59de4481b42074e6893d`
  to the prompt-bound current SHA; that path is explicitly allowlisted. No
  post-dispatch input or prompt drift was observed.
- The exact allowlist has `43` sorted, unique, wildcard-free entries: the 36
  durable paths, three original absent paths, one cache path, and three R9
  input/prompt/Review paths.
- Bindings are schema `1` and correctly bind the Plan, `22/14` archives,
  `344/29` Preflight inventories, their exclusions, and the 43-entry allowlist.
  The compatibility receipt is `pass` against current validator SHA
  `42cb47739b81646eadc303dbdfb59821ed75f21a6a12815600a3b51b7555ed98`;
  its successful archive-check root contains exactly 36 mode-`0600` files and
  no symlinks.
- Continuity was independently recomputed from inventory records and archive
  header metadata without reading archive member contents: Router `341`
  records reach
  `929958fbde3d78ff66282ceb3bdee3b301fae68f400875cf02a8b869d3bb678d`;
  Companion `29` records reach
  `c9e67d141f875877da6d0922281d8a65aa4fcb2a9aa1afab32fa5dc3bb4baecf`.
- The superseded attempt remains under its separate mode-`0700` root. Its
  partial preimages/archives have distinct inodes from revision 2; it contains
  no baseline, bindings, allowlist, continuity, or manifest output. The failed
  compatibility root remains empty. Neither attempt is authorizing evidence.
- The live cache still exactly matches SHA
  `5b7cd72df71d308929c08fb6ae047403b4374e1824a13f479e5034f468dfff49`,
  size `168579`, device/inode `16777233/170846033`, nlink `1`, uid/gid
  `501/20`, mode `0644`. Its parent remains device/inode
  `16777233/163934412`, uid/gid `501/20`, mode `0755`; the transaction root is
  on the same filesystem.
- Residual: none affecting this bounded authorization.

## Findings

None.

## Governance invariants

- Authority: PASS is governed R9 Plan Preflight evidence only. It cannot accept
  itself or mutate canonical state; only the original bound Codex control plane
  may accept it.
- Isolation: reviewer product `codex`, role `independent-reviewer`, capability
  `control-plane-high`, distinct from the Plan/amendment author, evidence
  preparer, failed-attempt investigator, and future executor. No file was
  modified.
- PASS/FAIL/BLOCKED: this PASS applies only while every bound hash, path, mode,
  count, cache identity, and absence guard remains exact. Any drift or nonzero
  Step 5A/Step 6 result is `BLOCKED` and stops progression.
- Completion: no Task 6, source, runtime, OpenSpec, Handoff, archive, or
  whole-change completion is claimed.
- Git: no reviewer Git use; R9 provenance remains limited to the ten disclosed
  read-only preparation commands. No Git-write or publication authority exists.
- Runtime/Pi: no runtime planning, mutation, restore, Pi invocation, or
  cross-runtime synchronization is authorized.
- Archive/publication: no recovery restore, cleanup, canonical transition,
  archive, Envelope, release, push, or publication is authorized.

## Authorized next action

Only the original bound Codex control plane may persist and accept this PASS,
reverify the bound preconditions, and execute Task 6 Step 5A exactly. It may
execute Task 6 Step 6 exactly only after Step 5A exits `0`. Any drift,
ambiguity, or nonzero result stops without cleanup, fallback, restore, scope
expansion, runtime/Pi action, archive, publication, or completion claim.
