[![Checks](https://github.com/openvax/openvax2/actions/workflows/checks.yml/badge.svg)](https://github.com/openvax/openvax2/actions/workflows/checks.yml)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

# OpenVax2

**One development repository. Independent Python packages. A tested combined stack.**

OpenVax2 is the public home for planning the OpenVax monorepo: annotation,
variant interpretation, peptide generation, MHC prediction, and vaccine ranking.
The goal is to change related libraries in one PR while preserving their existing
PyPI names, imports, command-line tools, and independent versions.

**Status:** design and release-tooling preparation. No libraries have been
migrated and no packages or container images are published from this repository
yet. Ongoing PRs continue in their original repositories before the implementation
sweep. The [source inventory](docs/inventory.md) records a dated planning snapshot.

## What will users install?

We plan to support all three paths. The combined products are conveniences built
from the same individual releases; users can keep installing just one library.

| Artifact | Purpose | Version policy | Availability |
| --- | --- | --- | --- |
| Individual PyPI packages, e.g. `varcode`, `isovar`, `vaxrank` | Use a library or CLI with its declared dependencies | Each retains its own version | Existing upstream releases remain available |
| `openvax` PyPI metapackage | Install a tested combination of OpenVax Python packages with one command | Its own stack version pins the selected component versions | Planned; name availability/ownership must be confirmed before publishing |
| `ghcr.io/openvax/openvax2` runtime image | Run that combined stack with Python and required redistributable system libraries | Stack version plus image revision; record immutable digest | Planned |

**Yes, the intended Python convenience install is `pip install openvax`.** It
will be a small dependency-only metapackage under `packages/openvax/`, not a copy
of all the library source or a replacement import namespace. Existing imports
such as `from varcode import Variant` will remain. That install command is a
future interface, not an installation instruction for a released product today.

The metapackage pins a compatible set of component releases. It does not freeze
every third-party dependency or install operating-system libraries. The Docker
image adds the full locked Python environment and system runtime. Large genomes,
model downloads, and user data remain explicit, versioned inputs mounted or
downloaded into caches. Restricted predictor binaries require separate provision.
See [combined artifacts](docs/distribution.md) for exact boundaries and examples.

## Developing one package or several

Each imported package will own its code, tests, build metadata, version, release
notes, and public dependencies under `packages/<name>/`. A uv workspace will
resolve sibling dependencies to editable source during development.

- **One-package change:** work in its directory, run its tests, and test affected
  consumers. Bump only that package when preparing its release.
- **Cross-package change:** update the producer and consumers together in one PR.
  Bump each package whose code or published dependency requirements change.
- **Independent install check:** build each affected wheel and test it outside
  the checkout against declared dependencies. A shared development environment
  cannot prove an individual distribution is complete.
- **Combined-stack update:** choose tested component versions and bump the
  metapackage separately. A component release need not immediately update the
  combined stack or release unrelated libraries.

[CONTRIBUTING.md](CONTRIBUTING.md) gives the current tooling commands and the
planned workspace/isolated development commands. The repository root is tooling;
it will not itself be a Python distribution.

## Releases follow package versions

**An unchanged package version is never republished.** A new repository commit,
docs edit, another package's version bump, or a Docker rebuild is not a reason
to upload every package again.

The checked-in [release planner](scripts/release_plan.py) compares each registered
package's authoritative version with its last recorded published version. It
selects increases, skips equal versions, and rejects downgrades. The registry is
empty until migration, so today's plan has no release candidates. CI runs the
planner and its tests; it has no publishing step or publishing credentials.

The eventual publisher will recheck PyPI, validate artifacts and dependency
order, and publish only the selected package/version pairs. Stack metapackage
releases follow the same rule. Docker image revisions have their own lifecycle
so system updates do not force Python package releases.

Read [release tooling and policy](releases/README.md) for state management,
version sources, retries, and the remaining production work.

## Documentation

| Document | Purpose |
| --- | --- |
| [Contributing](CONTRIBUTING.md) | Individual and coordinated development |
| [Combined artifacts](docs/distribution.md) | Metapackage, locks, Docker, and data/model boundaries |
| [Release policy](releases/README.md) | Publish only changed package versions |
| [Design](docs/design.md) | Workspace, dependencies, validation, and architecture |
| [Inventory](docs/inventory.md) | Source snapshots and constraints to revisit after PRs land |
| [Migration plan](docs/migration-plan.md) | Readiness, implementation, validation, and cutover |
| [Decision log](docs/decisions.md) | Established direction and open decisions |

## License

Original OpenVax2 materials are licensed under the [Apache License 2.0](LICENSE).
See [NOTICE](NOTICE). Imported packages preserve their licenses and attribution;
third-party tools, reference datasets, and model assets retain their own terms.
