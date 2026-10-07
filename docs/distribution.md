# Individual packages and the combined stack

Status: recommended product design; artifacts are not built or published yet.
The implementation sweep will establish the exact member set and supported
platforms after ongoing PRs finish.

## Three artifacts with different responsibilities

| Artifact | Contains | Does not contain |
| --- | --- | --- |
| Individual library wheel/sdist | That library, its required bundled resources, and dependency metadata | Sibling source bundled into the library |
| `openvax` metapackage | Metadata selecting a tested set of exact component versions | Duplicate implementation, system packages, or a new combined import API |
| OpenVax2 container image | Released components, locked Python dependencies, Python interpreter, and required redistributable native runtime | User samples, every reference genome/model, or restricted third-party executables |

The metapackage and image serve different installation needs, so plan for both.
Researchers extending Python code can use the individual wheels or metapackage.
Pipeline operators can use a verified container digest to reproduce the shipped
runtime without assembling native dependencies manually.

## The `openvax` metapackage

Put it under `packages/openvax/`; keep the workspace root non-published. It has an
independent stack version and ordinary Python dependency metadata, so pip users
need no workspace or Git checkout. Pin the included OpenVax component versions
exactly. Keep normal compatible dependency ranges in the reusable libraries.

The intended interface is `python -m pip install openvax==<stack-version>`.
Version placeholders in this document are illustrative, not commands for an
existing release. PyPI returned 404 for `openvax` on 2026-10-07; that does not
reserve the name or prove it can be claimed. Confirm availability and ownership
at publication time; `openvax-stack` is a possible fallback name.

Start with one curated core stack. Add extras for genuinely optional capabilities
only when the dependency graph supports them; do not advertise a lightweight
extra if a required library already pulls in its heavy dependencies. In
particular, current MHCTools requires MHCflurry. An inference stack should not
implicitly include every development, notebook, or model-training dependency.

The stack version is a compatibility snapshot, not a shared version imposed on
every component. A new `varcode` release can ship independently. Adopting it in
the stack is a separate change to the metapackage pins and its version, with
integration tests. Previously published metapackage versions retain their pins.

Component pins do not freeze the entire third-party dependency graph. Distribute
resolved environment locks alongside each stack release for supported targets,
with hashes and the selected Python/platform recorded. Users needing the shipped
runtime use those locks or the container digest. A development `uv.lock` with
editable workspace members is not the production installation manifest.

Dependencies belong in standard distribution metadata, which installers use to
resolve requirements. [PyPA metadata specification](https://packaging.python.org/en/latest/specifications/pyproject-toml/#dependencies-optional-dependencies)

## Runtime image

Target `ghcr.io/openvax/openvax2:<stack-version>-r<image-revision>`, backed by an
immutable image digest. Build from the metapackage's released wheels and exported
production locks, never editable source. Start with a CPU inference/runtime image
on the first validated Linux architecture. Add GPU and additional architectures
only with dedicated build and behavioral checks.

Pin the base image by digest, record the OS packages and resolved Python graph,
and attach a manifest identifying component versions, source commits, lock hashes,
image digest, and required external asset versions. Use ordinary package CLIs in
the container; keep it usable for Python scripts as well. Smoke-test installed
CLIs, resource loading, prediction adapters, and representative reports.
[Docker guidance on base-image pinning](https://docs.docker.com/build/building/best-practices/#pin-base-image-versions)

"All dependencies" means the dependencies required for the documented stack and
its supported capabilities. Inventory the actual native requirements during
implementation, including report-generation libraries. Document external service
requirements and host GPU drivers separately if GPU support is added.

Keep user inputs and outputs on mounts. Provide an explicit data/cache volume for
versioned genome annotations, reference tables, and model bundles. Record model
and dataset identifiers/checksums with results. Redistribute only assets permitted
by their terms; Apache 2.0 on this repository does not relicense third-party
predictors or data. Package-specific downloads and licensed-tool setup remain
visible steps, not surprise downloads during imports.

An OS-only update produces a new image revision, for example from `S-r1` to
`S-r2`, while keeping stack version `S` and all Python package versions unchanged.
Do not overwrite immutable version/revision tags. A convenience tag such as
`latest` may move, but reproducible runs should use the digest.

## Delivery order and release examples

1. Migrate and independently validate the selected libraries.
2. Build the metapackage against their published releases; verify a clean pip
   install and stack integration tests before its first release.
3. Build and test the runtime image from that released stack and production locks.

| Change | Individual distributions | Metapackage | Image |
| --- | --- | --- | --- |
| Root README edit | No publication | No publication | No release required |
| Varcode fix, same supported API | Publish Varcode only after its version bump | Update only when a new stack snapshot adopts it | Build when that stack snapshot is selected |
| Varcode API change requiring Isovar adaptation | Bump/publish both, dependency first | Bump if adopting the new pair | Build after the selected stack is released |
| New tested component combination | Reuse existing releases | Bump/publish its changed pins | Build corresponding stack image |
| System-library fix with the same Python stack | No publication | No publication | Increment image revision |

The release planner never infers that a component bump requires all these
artifacts. Each Python distribution has its own version gate; the image has its
own reviewed build inputs and revision. See [release policy](../releases/README.md).
