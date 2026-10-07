# Migration plan

Status: documentation phase, 2026-10-07. All implementation checkboxes below
remain open. Ongoing PR completion is a prerequisite, not something this planning
task has verified. See the [design](design.md) and [decisions](decisions.md).

## Phase 0: planning deliverables

- [x] Record the proposed package, dependency, testing, and release architecture.
- [x] Inventory a representative set of local source commits and their relationships.
- [x] Separate proposed defaults from decisions needing evidence.
- [x] Record implementation gates and preservation of existing local work.

## Phase 1: select a ready baseline

After the ongoing work settles, fill this register. Each selected package needs
its own row; the grouped entries currently identify the scope to assess. A gate
may be marked not applicable with a reason. No blank entry means ready.

| Candidate group | PRs that must finish | Selected merged SHA / release | Owner | Readiness |
| --- | --- | --- | --- | --- |
| `datacache`, `gtfparse`, `sercol` | To inventory | Unselected | Unassigned | Not assessed |
| `pyensembl`, `varcode`, `isovar` | To inventory | Unselected | Unassigned | Not assessed |
| `mhctools`, `topiary`, `vaxrank` | To inventory | Unselected | Unassigned | Not assessed |
| `serializable`, `mhcgnomes`, any additional members | Scope and PRs to inventory | Unselected | Unassigned | Not assessed |

- [ ] Confirm the first-wave allowlist and canonical source repositories.
- [ ] Inspect live PRs/issues and identify only those that block migration; do not
  require all unrelated backlog work to finish.
- [ ] Verify required PRs have merged and their expected releases are available.
- [ ] Record exact source commits, package versions, Python/platform support,
  dependency bounds, current release procedures, and existing CI baselines.
- [ ] Resolve candidate constraint conflicts with behavioral tests. Record any
  stable version that remains blocked and why; do not silently downgrade.
- [ ] Inventory uncommitted work, branches, worktrees, and editable paths without
  resetting or moving existing checkouts.
- [ ] Settle the remaining implementation decisions needed from D01–D08. The
  planning repository is hosted at `openvax/openvax2`; confirm package ownership
  and migration access before source import.

Exit evidence: per-package readiness rows, a selected compatible source set, and
an explicit user request to begin the implementation sweep.

## Phase 2: import and establish the workspace

- [ ] Use fresh temporary clones/import branches, leaving source checkouts intact.
- [ ] Rehearse history import under `packages/<name>/`; preserve authorship,
  licenses, notices, and traceability to original SHAs. Inspect history and
  archive size before selecting the final import method.
- [ ] Namespace conflicting historical tags and record the mapping. Original
  repositories and their tags remain available.
- [ ] Import tracked source and needed fixtures. Audit tracked large artifacts
  before import; copying tracked history can also import obsolete large files.
- [ ] Preserve package internals and existing build backends. Add minimal
  `pyproject.toml` metadata where workspace membership requires it.
- [ ] Add the non-published root, explicit members, source mappings, pinned tool
  versions, and a compatible lockfile in a dedicated workspace environment.
- [ ] Prove the lock resolves the selected member versions and bounds without
  overrides, path dependencies in published metadata, or forced installs.
- [ ] Reconcile imported agent instructions, release scripts, and tool settings
  with the agreed monorepo policy. Preserve package-specific scientific checks.

Exit evidence: reviewable import, source-SHA mapping, clean workspace install,
and documented metadata changes. Import/build-backend modernization/API changes
should be separable in review.

## Phase 3: prove packaging and tests

- [ ] Run the required lint/test commands for every imported package in the new
  layout, recording any baseline failures separately from migration regressions.
- [ ] Run cross-package smoke tests for annotation, peptide generation,
  prediction adapters, and ranking/reporting where those packages are included.
- [ ] Build each wheel and sdist; build a wheel from each sdist in isolation.
- [ ] Compare before/after metadata, public entry points, import names, licenses,
  and required package data against the selected source baseline. Explain all
  intended differences, including repository URLs and release version changes.
- [ ] Install each candidate wheel in a fresh environment outside the source
  checkout. Run import/CLI/resource checks, relevant behavioral tests, and
  `pip check` with no editable dependencies.
- [ ] Validate the candidate release set together and representative supported
  dependency boundaries on the agreed Python/platform matrix.
- [ ] Adapt root-relative paths, fixture acquisition, caches, coverage, and docs
  builds. Keep model/data downloads explicit and preserve provenance.
- [ ] Add CI that starts conservatively with the full applicable suite. Verify
  that failing checks block release preparation.

Exit evidence: green applicable checks, isolated artifacts, and no unexplained
behavior or packaging differences. Workspace-only success is insufficient.

## Phase 4: rehearse independent releases

- [ ] Implement version/release-note checks and a manifest for selected packages.
- [ ] Rehearse building, staging, and verifying a producer/consumer release pair
  while leaving an unrelated package untouched.
- [ ] Verify dependency ordering, cycle detection, package-qualified tags, and
  registry availability checks.
- [ ] Rehearse partial upload failure and resumption using the same artifacts.
- [ ] Inventory and configure the selected PyPI publisher identities, workflow
  names, and release environments before production cutover. Exercise TestPyPI
  when that publishing rehearsal is authorized.
- [ ] Prepare documentation links, issue references, project URLs, and the
  transition notices for old repositories.

Exit evidence: a reviewable release manifest, verified artifacts, rehearsal
results, and a concrete cutover checklist. This phase does not itself imply
production publication.

## Phase 5: cut over after validation

- [ ] Pause conflicting release activity for the selected packages and import
  any final changes since the rehearsal baseline.
- [ ] Re-run affected validation on the final source commit and artifacts.
- [ ] Establish the new release authority and retire the superseded automation
  in a coordinated change, avoiding two active publishers racing versions.
- [ ] Publish the intended package releases through the agreed release process;
  verify clean installs from PyPI after each dependent set is available.
- [ ] Add transition links in the former repositories and docs. Keep historical
  issues, releases, source references, and required downloads reachable.
- [ ] Switch relevant shared-environment editables from old paths only after
  preserving local work. Refresh metadata, upgrade related dependencies together,
  run `pip check` and relevant tests, and report remaining constraints.
- [ ] Evaluate the acceptance example in the decision log before expanding the
  monorepo to more packages.

## Recovery

Before cutover, abandon or revise the import branch; original repositories stay
authoritative. After a partial publication, record what exists, stop dependent
uploads if prerequisites are missing, and resume identical artifacts or publish
corrective versions. Git rollback does not roll back PyPI releases. If release
authority must return to an old repository, coordinate that handoff explicitly
and retain the source/version mapping. Archive old repositories only after the
transition has been verified; do not delete them as part of migration.
