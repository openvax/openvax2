# Decision log

Updated 2026-10-07. Proposed defaults can guide planning; they are not completed
implementation or permission to publish packages.

## Established direction

- **Prepare now, migrate later.** The user requested design planning and release
  preparation now, with package migration after ongoing PRs finish.
- **Preserve individual PyPI packages.** This is the direction being evaluated;
  existing names and imports should continue working.
- **Preserve the shared environment and local work.** The user's environment
  maintenance policy is recorded in [AGENTS.md](../AGENTS.md).
- **Hosting and license.** The user explicitly requested public visibility and
  Apache 2.0 for `openvax/openvax2`. The default branch is `main`.
- **Independent release gates.** Publish a distribution only when its own
  version increases (or for an intentional first release); unchanged versions
  are skipped. The read-only planner and its CI tests implement selection now.

## Decision register

| ID | Decision | Proposed default | Evidence or decision needed |
| --- | --- | --- | --- |
| D01 | Initial members | Closely coupled core listed in the design; evaluate `serializable` and `mhcgnomes` with it | Confirm canonical repositories, ownership, coupling, and the final allowlist |
| D02 | Adjacent projects | Keep MHCflurry, MHCseqs, Osteosarc, Oncoref, and PirlyGenes external initially | Confirm which change frequently enough with the core to justify inclusion; external constraints still matter |
| D03 | Dependency manager | uv workspace for the compatible core | Resolve post-PR constraints in a fresh environment and record chosen uv/Python versions |
| D04 | Versions and releases | Independent versions, package-qualified tags, release manifest; unchanged versions never republished | Version gating requested by user; finish publisher and reconcile imported release rules at migration |
| D05 | Git history | Import full source histories without rewriting original repositories; rehearse a prefix/subtree merge | Verify history navigation, license retention, historical tag naming, and repository size |
| D06 | Hosting and license | `openvax/openvax2`, public, Apache 2.0, default branch `main` | Explicitly requested by user; preserve imported licenses and confirm package ownership at migration |
| D07 | Cutover baseline | Import selected merged commits after ongoing PRs settle | Fill the readiness register with PR links, exact SHAs, releases, and owners |
| D08 | Python and platforms | Preserve current package support; choose a common development interpreter | Verify actual wheel availability and tests for each supported combination |
| D09 | Publishing authority | One release path per package using existing PyPI projects | Inventory current automation; test replacement publisher configuration before cutover |
| D10 | Issues and docs | Preserve original URLs, link selected active issues into the new workflow, retain docs redirects | Decide tracking location and per-package documentation hosting |
| D11 | Editables after migration | Switch paths deliberately only after wheel/workspace verification | Inventory existing editable paths and any local work; follow the shared environment policy |
| D12 | Combined Python install | `openvax` metapackage with its own version and exact tested component pins | Recommended design; confirm PyPI name/ownership and core package set before first release |
| D13 | Combined runtime | `ghcr.io/openvax/openvax2`, stack version plus image revision | Recommended design; validate Linux targets, production locks, native libraries, and external model/data acquisition |

## Evidence that would change the recommendation

- Core packages cannot share a tested stable dependency resolution without
  substantial unrelated changes: split environments or narrow the first wave.
- Most maintenance proves independent rather than coordinated: retain those
  repositories and share tooling instead.
- History or data makes a combined repository impractical: narrow the import or
  choose a documented snapshot strategy with immutable source references.

## Acceptance example for the implementation sweep

A representative change to a `varcode` API and its `isovar` consumer should be
reviewable in one PR. CI should test the workspace and separately install the
candidate wheels. A release plan should identify only the packages requiring
new versions, publish their dependencies first, and leave an unchanged package
such as `gtfparse` unreleased. Users should be able to install the resulting
`isovar` release from PyPI with no Git checkout or uv-specific configuration.
