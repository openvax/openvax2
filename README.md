[![Checks](https://github.com/openvax/openvax2/actions/workflows/checks.yml/badge.svg)](https://github.com/openvax/openvax2/actions/workflows/checks.yml)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

# OpenVax2

OpenVax is a set of Python libraries for variant annotation, RNA-supported
protein reconstruction, MHC prediction, and vaccine candidate ranking. Each
library is a separate package on PyPI.

This repository plans a monorepo for those libraries. It holds the design
documents, a release planner, and the [package atlas](https://openvax.github.io/openvax2/),
a website showing what each package does and how they depend on each other.

## Status

Design and release-tooling preparation. No libraries have been migrated, and
no packages or container images are published from this repository yet.
Ongoing PRs continue in each library's original repository until the
implementation sweep. The [source inventory](docs/inventory.md) records a dated
planning snapshot.

To use OpenVax now, install the individual packages from PyPI, for example:

```sh
pip install varcode
```

## Packages

The main libraries, in the order of the variant-to-candidate workflow:

| Package | What it does |
| --- | --- |
| [PyEnsembl](https://github.com/openvax/pyensembl) | Query Ensembl genes, transcripts, exons, and sequences |
| [Varcode](https://github.com/openvax/varcode) | Predict how variants change transcripts and protein sequence |
| [Isovar](https://github.com/openvax/isovar) | Reconstruct mutant protein sequences supported by tumor RNA reads |
| [MHCflurry](https://github.com/openvax/mhcflurry) | Predict MHC class I binding, antigen processing, and presentation |
| [MHCTools](https://github.com/openvax/mhctools) | Run binding, presentation, immunogenicity, and processing predictors through shared interfaces |
| [Topiary](https://github.com/openvax/topiary) | Combine peptide prediction with filtering and ranking |
| [Vaxrank](https://github.com/openvax/vaxrank) | Rank vaccine peptide candidates and write reports |

The [package atlas](https://openvax.github.io/openvax2/) also covers the
supporting libraries (GTFparse, DataCache, Serializable, Sercol, MHCgnomes,
MHCseqs) and reference-data packages (Osteosarc, Oncoref, PirlyGenes), with
their direct dependencies as of 2026-10-07.

## Installation options

Individual packages stay the primary way to install OpenVax. Two combined
products are planned, both built from the same individual releases:

| Artifact | Purpose | Version | Availability |
| --- | --- | --- | --- |
| Individual PyPI packages, e.g. `varcode`, `isovar`, `vaxrank` | One library or CLI with its declared dependencies | Each keeps its own version | Available now; existing releases stay on PyPI |
| `openvax` PyPI metapackage | A tested combination of OpenVax packages in one install | Its own stack version, pinning component versions | Planned; the PyPI name must be confirmed first |
| `ghcr.io/openvax/openvax2` container image | The combined stack plus Python and required system libraries | Stack version plus image revision; use the digest | Planned |

The metapackage will contain only dependency metadata, so existing imports such
as `from varcode import Variant` stay the same. It will not pin every
third-party dependency or install system libraries; the container image adds
those. Genomes, model downloads, user data, and restricted predictor binaries
remain separate inputs in both cases. `pip install openvax` describes the
planned interface; nothing is published under that name yet.
[Combined artifacts](docs/distribution.md) gives the details.

## Development model

After migration, each library will live under `packages/<name>/` with its own
code, tests, build metadata, version, and release notes. A uv workspace will
link sibling packages during development, so one PR can change a library and
the packages that use it. Each changed wheel will still be built and tested on
its own, outside the checkout. The repository root is tooling and will not be
a Python distribution.

[CONTRIBUTING.md](CONTRIBUTING.md) has the commands for today's tooling and the
planned per-package workflow.

## Release policy

A package is published only when its own version increases. A docs edit, a
new commit, another package's version bump, or a container rebuild does not
republish unchanged packages.

The [release planner](scripts/release_plan.py) compares each registered
package's version with its last published version: it selects increases, skips
equal versions, and rejects downgrades. No packages are registered yet, so the
current plan is empty. CI runs the planner and its tests; there is no
publishing step and no publishing credentials. The metapackage follows the same
rule, and container images have their own revision numbers so system updates
don't force Python releases.

The production publisher is still to be built. It will recheck PyPI, validate
artifacts, and publish only the selected package versions in dependency order.
See [release tooling and policy](releases/README.md).

## Documentation

For contributors:

- [Contributing](CONTRIBUTING.md): current checks and the planned development workflow
- [Release policy](releases/README.md): how the planner selects package versions to publish
- [Package atlas website](docs/site.md): editing, previewing, and deploying the site

Planning documents (proposals and records, not usage guides):

- [Design](docs/design.md): workspace, dependencies, validation, and release architecture
- [Combined artifacts](docs/distribution.md): metapackage, lock files, container image, and data/model boundaries
- [Migration plan](docs/migration-plan.md): readiness gates, import, validation, and cutover
- [Decision log](docs/decisions.md): established direction and open decisions
- [Inventory](docs/inventory.md): dated source snapshot and constraints to revisit

## License

Original OpenVax2 materials are licensed under the [Apache License 2.0](LICENSE).
See [NOTICE](NOTICE). Imported packages keep their own licenses and attribution;
third-party tools, reference datasets, and model assets keep their own terms.
