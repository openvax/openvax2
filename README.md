# OpenVax monorepo planning

Status: **design draft; implementation deferred**. Started 2026-10-07.

The proposed monorepo would let related OpenVax libraries evolve in one pull
request while continuing to ship independent PyPI packages. Existing package
names, imports, command-line entry points, and version histories would remain.

This repository currently contains planning documents only. Ongoing work stays
in the existing repositories. The implementation sweep starts after the relevant
PRs land and the migration baseline is recorded.

## Read the plan

| Document | Purpose |
| --- | --- |
| [Design](docs/design.md) | Package layout, dependencies, CI, and independent releases |
| [Inventory](docs/inventory.md) | Dated source evidence, package relationships, and migration constraints |
| [Migration plan](docs/migration-plan.md) | Readiness gates, implementation work, validation, and cutover |
| [Decision log](docs/decisions.md) | Recommendations, unresolved choices, and acceptance criteria |
| [Agent instructions](AGENTS.md) | Planning scope and environment preservation |

## Working proposal

- Bring the closely coupled annotation and vaccine-ranking packages into
  `packages/<distribution-name>/`.
- Use a uv workspace for packages that can share a compatible development
  environment; retain separate environments where needed.
- Keep each package independently buildable, installable, versioned, and
  publishable. The repository root is tooling, not a new PyPI distribution.
- Validate cross-package changes together and validate individual wheels in
  clean environments.
- Automate release planning and publish only packages with releasable changes.

These are proposed defaults, not an approved migration or a working workspace.
There is no root `pyproject.toml`, lockfile, package import, or publishing workflow
yet. Repository hosting and the final package list remain open decisions.

## Next milestone

Complete the readiness register in the [migration plan](docs/migration-plan.md)
after ongoing PRs settle. Then select exact source commits and implement the
first workspace and packaging checks in a reviewable sweep.
