# Pre-MR Read-Only Hunt Reference (`review_profile=pre-mr`)

Author: elvis

Use this reference only in `pre-mr` read-only reviews. Keep strict Scope Lock and Anti-Bloat discipline:

1. **Changed-Hunk Attribution Only**: Every `FAIL` finding MUST anchor to an exact `path:line` modified in `git.branch_diff.patch` or `git.working_diff.patch`, and prove a concrete failure path that did not exist on the target baseline before this change.
2. **Conditional Activation (`hunt: n/a`)**: Evaluate each lens below **only** when the diff actually touches that mechanism. When a lens does not apply to the diff, record `hunt: n/a` for that lens. Never fail a change for "missing defensive guards" without a real in-repo caller or reachable runtime trigger, never emit naming/formatting/style nitpicks, and never report untouched pre-existing issues on the target branch.

## Four Conditional Hunt Lenses

1. **Consumer Symmetry (`consumer_symmetry`)**
   - **Activate when**: Diff adds, removes, relaxes, or renames an enum value, schema constraint (`minItems`, nullable, field type), status/error code, event payload, or shared configuration flag.
   - **Check**: Search `{CWD}` for all implementations, producers, serializers, validators, UI/API consumers, and contract tests of that symbol. Verify no sibling path or downstream consumer is left out of sync.

2. **Durable Side-Effect & Re-Entry Safety (`durable_safety`)**
   - **Activate when**: Diff performs database writes, external HTTP/RPC calls, file/checkpoint persistence, queue publishing, or state-machine transitions.
   - **Check**:
     - Crash/failure after an external or durable side effect succeeds but before local row, ack, or checkpoint is recorded -> retry/recovery must not duplicate side effects or corrupt state;
     - Failure after durable commit but before response/watermark advancement -> re-entry must converge idempotently (unique key or conditional `WHERE status = ...` CAS guard);
     - First execution vs retry/recovery must not mix temporary and persistent identities.

3. **Pagination, Query & Bounded-Payload Liveness (`liveness_bounds`)**
   - **Activate when**: Diff writes or alters SQL joins, `IN (...)` batches, `LIMIT`/cursor/offset pagination, queue polling, or size-bounded context/snapshot builders.
   - **Check**:
     - Never apply `LIMIT` first and filter `pending` / `deferred` / `invalid` items only in memory when skipped items can starve subsequent eligible records; filter in the query predicate or advance the cursor;
     - Paginated/cursor `ORDER BY` on non-unique columns (timestamp, score, priority) must include a unique tie-breaker key (e.g., `, id ASC`) to prevent skipped or duplicated rows;
     - `LEFT JOIN` predicates must filter the intended alias without turning unmapped optional rows into whole-batch failures, and dynamic `IN` lists with large upper bounds must be chunked;
     - Size-bounded payloads must reserve mandatory base facts before filling optional display fields.

4. **Target Baseline Counterfactual & Repair Closure (`target_counterfactual`)**
   - **Activate when**: Diff adds conditional branches, fallback paths, or bugfixes.
   - **Check**:
     - Inputs outside the new branch must preserve exact target-branch return values, nullability, and exception behavior (no silent exception swallowing);
     - Regression tests must cover the primary failure case plus applicable retry/recovery or boundary/multi-step cases so a direct one-line patch cannot be immediately bypassed by an adjacent state combination.
