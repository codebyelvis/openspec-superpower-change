## ADDED Requirements

### Requirement: Project document destination ownership

Before creating or relocating an ordinary project document, the Change Gate
SHALL resolve its purpose/domain against scoped project instructions and relevant
existing navigation/documents. Explicit user/project path contracts SHALL take
precedence, followed by established purpose/domain conventions. Only when neither
exists SHALL a suitable purpose subdirectory be selected. A universal project
layout SHALL NOT be imposed, and directory existence alone SHALL NOT establish
a convention. Applicable conflicting contracts or equally plausible destinations
SHALL be resolved before writes. The docs root SHALL be reserved for index entry
points and explicitly contracted paths.

#### Scenario: Existing domain directory is reused
- **WHEN** a project uses an established `docs/ops/` deployment convention and
  requests a new deployment note without specifying a different contracted path
- **THEN** the note follows that convention, with no forced `docs/deployment/`
  structure or ordinary docs-root addition

#### Scenario: No convention uses a purpose directory
- **WHEN** a new project has no applicable destination contract or convention
  and requests an ordinary deployment or engineering document
- **THEN** its destination is a suitable purpose subdirectory rather than the
  docs root, with only the authorized document/navigation additions

#### Scenario: Ambiguous ownership does not default silently
- **WHEN** scoped inspection leaves conflicting applicable contracts or two
  equally plausible destinations
- **THEN** the unresolved ownership is reported and no destination is selected
  by file recency or by the generic fallback before resolution

### Requirement: Protected project artifact location contracts

Ordinary document organization SHALL preserve the existing locations of AGENTS,
CONTEXT and its map, OpenSpec artifacts, collaboration status and iteration-state
files. Explicit user/project root-path contracts SHALL override generic directory
defaults. Bound approval/evidence references SHALL remain subject to their existing
owner, authorization, hash and transition rules; document organization SHALL NOT
grant migration, re-signing, state-transition or completion authority over them.

#### Scenario: Explicit root engineering guidance is retained
- **WHEN** AGENTS explicitly points to `docs/engineering-invariants.md`
- **THEN** that guidance path is reused and neither it nor AGENTS is moved merely
  because an unconstrained project's fallback uses an engineering subdirectory

#### Scenario: Special artifacts are excluded from ordinary relocation
- **WHEN** ordinary project-document organization occurs alongside CONTEXT,
  OpenSpec and `docs/agent-collab/<change-id>/status.md` or iteration-state files
- **THEN** their locations and contents remain under their existing contracts,
  without generic-directory migration or fabricated new approval/evidence

### Requirement: Authorized document relocation reference closure

Document relocation SHALL be limited to explicitly authorized documents and the
authorized reference closure identified before mutation. It SHALL preserve content
except necessary link edits and repair relative inbound/outbound links, anchors,
agent navigation and applicable active references in that closure. Unrelated
historical files SHALL remain unchanged. An unauthorized required referring file,
conflicting destination, bound-project escape or unresolved link SHALL block
relocation until resolved through the existing Change Gate. Creation authority
SHALL NOT imply blanket migration authority.

#### Scenario: Scoped move preserves content and effective links
- **WHEN** a document and all required referring files/navigation are authorized
  for relocation to an agreed project-purpose directory
- **THEN** the actual moved document retains its substantive content, relative
  links/anchors and authorized AGENTS navigation resolve, and unrelated snapshots
  remain unchanged

#### Scenario: Missing reference authorization stops before the move
- **WHEN** an intended move requires editing a referring file outside the
  current authorization or a protected bound artifact
- **THEN** the gate records the unresolved reference closure and stops before
  relocation rather than leaving a broken link or silently expanding write scope

### Requirement: Single owned placement policy and learning fallback

The Project Document Ownership subsection of
`references/project-learning-closeout.md` SHALL own the ordinary-document rule.
SKILL SHALL provide minimal conditional navigation and the Candidate Card template
SHALL reference the canonical resolver instead of maintaining a copied fallback.
Reading the ownership subsection alone SHALL NOT activate learning promotion.
The engineering Target resolver SHALL respect existing contracted/conventional
guidance and otherwise default to `docs/engineering/engineering-invariants.md`.
Existing learning triggers, enforcement and completion gates SHALL remain intact.

#### Scenario: Unconstrained learning target uses an engineering subdirectory
- **WHEN** engineering knowledge qualifies under the existing learning gate and
  the project has no explicit or established guidance destination
- **THEN** the engineering target uses `docs/engineering/engineering-invariants.md`
  through the canonical resolver and existing promotion/Review requirements

#### Scenario: Navigation does not duplicate or activate promotion
- **WHEN** an ordinary document-creation request reads the ownership subsection
- **THEN** the entrance/template supply navigation rather than copied policy,
  and reading that subsection does not itself trigger a learning-closeout bundle

### Requirement: Actual document behavior and link evidence

S8 acceptance SHALL include isolated actual file operations with assertions on
destinations, content, relative links/anchors, navigation and unaffected paths.
Native evidence SHALL demonstrate real authorized tool behavior and fail closed
on absent outputs or off-scope writes. Rule-text presence or an answer-only
routing probe SHALL NOT substitute for behavior evidence. Artifact-bound negative
validation SHALL reject moving owned policy/default obligations into other files.
Major approval, RED/GREEN, applicable independent Reviews, required parser-mode
checks and authorized required runtime synchronization SHALL remain mandatory.

#### Scenario: Actual files determine acceptance
- **WHEN** the approved slice is verified using existing-convention, no-convention
  and authorized-migration/incomplete-closure isolated scenarios
- **THEN** real file/link/scope results decide acceptance, while missing tool
  evidence, broken links, unauthorized changes or unresolved gates block closure

#### Scenario: Misplaced rule text cannot satisfy ownership validation
- **WHEN** the canonical ownership subsection or resolver is replaced by a
  placeholder and its required text is copied into a template
- **THEN** artifact-bound validation fails despite the text existing elsewhere
