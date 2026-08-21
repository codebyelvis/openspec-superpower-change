# add-codex-skill-update recovery Proposal Review

Date: 2026-08-04

Reviewer: independent Codex reviewer `recovery_proposal_review`

Review class: Major Self-Evolution Proposal / High Review

Verdict: **PASS**

No current High or Blocked actionable finding remains. This verdict reviews the
proposal revision and its source-bootstrap mechanism; it is not task 1.5 exact
user approval and does not authorize snapshot/manifest minting or v2 source
creation.

## Reviewed raw bytes

- `CONTEXT.md`: `ed843cbb8ae275b36cdd5e0a772bc08629a80548521dc7d5147f466de50242b0`
- `proposal.md`: `84451a00853099dd9c1ccc53fa3ca58d6d07e7a77cf8079fb4d7a88ae622b7cd`
- `design.md`: `0e4c571543d813ce8aa04d0041288b802987bbdedd2c9a4b3012621287638e36`
- `tasks.md`: `5739265a71dbe5d2dce1e3bde13905bab8db5d9fb41a0033d6b1f05527d46554`
- governance spec delta: `cb7e4727544e6b5e2cfcdc716c97794443e514b1b1f081780289a70c11c56cfd`
- review draft: `480ed58dc146d5645edf9feb92cc76b543e7cd9744890cc4b1918f2c56830d83`
- v2 helper: `2823d197a8faa73c19766103ca64926dedcc670b1dcc816942075ccaa929ee43`
- schema-2 prestate file: `f7a23253f4d1c5afdb1a2deeb8235721a34143d2c99da620435939c08baf7558`
- schema-2 prestate domain digest: `41c5747beef62fb666200730139a0195e34eab078d97b88ce2128420c522506d`
- sandbox profile: `eb8ddf6e213d3b2388dc7fb681d0f14cf9693335d76c4dc19f2362bc5e5bcce9`
- sandbox exec vector: `983f1ff690bea399c2237f1865c5b9552a3bff1cd7673026a4a595a45de643e8`

The reviewed `tasks.md` still had task 1.4 unchecked. Marking only that completed
review step after this PASS is checklist-only progress and does not change the
checklist-normalized contract projection. The final task raw hash must therefore
be recomputed and displayed at task 1.5 approval.

## Scope conclusions

- Source boundary: PASS. The old branch/worktree/admin attempt is a bound
  preserve-only quarantine. The distinct v2 target remains absent and cannot be
  reused, repaired, deleted, cleaned, or adopted.
- Update authority: PASS. Direction-only scheme approval is not treated as the
  exact Major revision approval. Later bootstrap, schedule, registry, cleanup,
  Git, and publication authorities remain separate.
- Scheduler and registry mutation: PASS. Schedule replacement/removal and
  `registry-replace` remain later exact plan/approval/receipt transactions with
  invalidation rules; no proposal approval performs them.
- Adapters and notifications: PASS. Observation and local notification remain
  closed reviewed adapters, with update/blocker/failure-only notification and
  redaction behavior required by the implementation plan and tests.
- Recovery and rollback: PASS. Journals, leases, no-replace operations, and
  restoration-only recovery are fail-closed; interruption residue is preserved
  and never silently cleaned or force-reused.
- Tests and evidence gates: PASS. The contract requires the seven Skill RED
  scenarios, source/runtime High Reviews, Step Evidence Gates, final evidence,
  Project Learning, and archive validation. The future plan must include the
  four previously missing notification, registry-replace, Bootstrap Control
  Root RED/GREEN, and runtime-bootstrap sequences.
- Git/publication authority: PASS. No staging, commit, reset, clean, remote,
  push, PR, release, or publication is granted. Only the exact local v2 loose
  ref/worktree/admin creation can be approved at task 1.5.

## Source-bootstrap mechanism findings closed

1. The helper now owns the complete task-2.1 transaction. Its read-only
   `--launch` mode validates exact approval material and execs the digest-bound
   inline-profile sandbox vector; `--contained` self-attests active denial.
2. Repository, Git/ref/log/worktree, target-parent, approval, and
   source-bootstrap directories are opened component-by-component no-follow,
   retained, and checked against schema-2 identities before write and after
   registration.
3. The old quarantine is revalidated pre/post using full artifact/manifest/
   missing-evidence bytes plus lstat-to-open-FD inode continuity for both
   worktree and admin directories.
4. Raw base blob OIDs are independently recomputed. A valid Git index v2 is
   generated, fsynced, checked tracked-clean, and proven unchanged by status.
5. Exact file and directory sets, directory owner/mode, raw tracked/untracked
   bytes, ref/reflog/admin bytes, and target/admin inode continuity are checked;
   extra empty or ignored directories cannot pass.
6. Ref/reflog promotion uses descriptor-relative hard-link no-replace plus lock
   unlink, not an overwriting rename. Lock/journal files and parents are
   durably fsynced.
7. The Git object-store claim is capability-scoped: the bootstrap profile has
   no object-store write authority and the helper performs no object mutation;
   unrelated external object creation is not falsely promised as inventoried.

## Evidence observed by reviewer

- strict OpenSpec validation: PASS
- Skill quick validation: PASS
- core-gate validation: PASS
- 142 unit tests: PASS
- helper AST/static checks: PASS
- exact inline sandbox contained path: expected fail-closed exit 70 while no
  current manifest exists
- direct unsandboxed contained path: expected fail-closed exit 70 because
  network denial is not active
- synthetic Git layout/index: 169 blobs, zero porcelain status bytes, index
  SHA-256 unchanged
- temporary real-path sandbox allow probe: descriptor mkdir/write/fchmod/fsync,
  hard-link/unlink, and Python-to-fixed-Git calls PASS
- old quarantine evidence: exact match
- v2 target/admin/ref/reflog and source lock/journal: ABSENT
