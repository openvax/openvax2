# OpenVax2 planning and release preparation

## Current scope

The user requested documentation and design planning, then authorized public
hosting, Apache 2.0 licensing, independent release preparation, and a GitHub Pages
site explaining the ecosystem. Maintain and deploy the site from `site/` using
the Pages workflow. The package migration sweep remains deferred until ongoing
package PRs finish.

- Work on a documentation branch; keep recommendations distinct from accepted
  decisions and observed facts.
- Read sibling repositories as evidence. Preserve their branches, worktrees,
  uncommitted changes, editables, tags, and release state.
- Prepare and test release tooling in an isolated tooling environment as needed.
  Do not import library source, change sibling package bounds, or publish Python
  packages/container images as part of this preparation.
- Date observations and identify source commits. A local branch is not evidence
  that a PR has merged or a package has shipped.
- Planning documents do not require library version bumps or releases. Check
  document links and consistency. For release-tooling changes, run the tests in
  CONTRIBUTING.md and inspect the generated release plan.
- Before implementation, refresh the inventory and read the applicable source
  repository instructions. Resolve their release rules explicitly for the
  monorepo instead of copying automatic release behavior into the root.

## Shared Python environment

When maintaining `/Users/iskander/code/shared-virtual-env`, keep the OpenVax stack
and its dependencies on the most recent mutually compatible stable versions.
Leave unrelated notebook, AI, and other packages outside this maintenance scope.
Upgrade related packages together when necessary to resolve constraints.
Preserve editable checkouts and local work; refresh stale editable package
metadata from the existing checkout. Verify with `pip check` and relevant tests,
and report any constraint that prevents a current version. Do not silently
downgrade packages or force incompatible installs. Distinguish this shared
environment from repository-local release environments.

This preparation does not maintain that environment. Future workspace and
release validation should use dedicated environments. Switching the shared
environment's editable paths is a separate migration step after validation.
