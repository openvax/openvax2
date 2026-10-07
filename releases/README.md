# Version-gated releases

## Implemented now

`scripts/release_plan.py` is a read-only planner. CI runs its tests and prints a
JSON plan. No package publishing, image building, registry access, or state
updates occur in this script or the current workflow. The package registry and
published baseline are intentionally empty until packages migrate.

The planner uses these inputs:

- [packages.json](packages.json): explicit package allowlist, directory, and
  optional Python version-file location. Versions are not duplicated here.
- [published.json](published.json): last confirmed published version per package.
  Seed existing packages from verified PyPI releases at migration time.

For a migrated package, an illustrative registration is:

```json
{
  "name": "varcode",
  "path": "packages/varcode",
  "version_file": "varcode/version.py",
  "version_variable": "__version__"
}
```

`version_file` is relative to the package directory. The planner reads a literal
top-level assignment with Python's AST; it never imports the module. Omit that
field for a package whose version lives in `project.version` in `pyproject.toml`.
Other dynamic version schemes need an explicit adapter before registration.
The future build check must verify that wheel metadata matches the planned name
and version, particularly for dynamic metadata.

The published baseline maps distribution names to version strings. A completely
new distribution must explicitly set `"first_release": true` instead of
accidentally treating an unknown existing package as new. This flag does not
skip future registry, name-ownership, or artifact checks.

| Version relative to last confirmed publication | Planner result |
| --- | --- |
| Equal, including equivalent PEP 440 spellings | Skip |
| Higher stable version | Candidate for publication |
| Lower version | Error |
| Missing baseline without explicit first release | Error |
| Prerelease, development, or local version | Error; initial policy is stable releases only |

Comparison is against the last published version, not the previous Git commit.
A version bump remains pending through subsequent documentation commits until
publication completes. A changed file with an unchanged version never causes
automatic publication. The planner sorts output by name for readability; that
order is **not** dependency order or authorization to deploy.

## Required production publisher, implemented in the later sweep

1. Lock release execution to one run per repository and use a clean selected
   `main` commit. Resolve the plan's versions from that commit, not a moving branch.
2. Reconcile the baseline with actual PyPI state. If the version already exists,
   do not rebuild/overwrite it. Verify recorded artifact identity, finish a
   recorded partial upload using identical files, or stop for reconciliation.
   The local ledger alone is not sufficient protection against duplicate uploads.
3. Compare package/shipped inputs with the last released source commit. Reject a
   proposed release that omits required dependency/version changes. For normal
   PRs, surface pending package changes without automatically publishing or
   forcing unrelated version bumps. Shared build-input changes need explicit
   affected-package accounting.
4. Build wheels and sdists only for candidate packages. Check names, versions,
   supported Python, dependency metadata, package data, licenses, and the sdist
   round trip. Hash and retain artifacts before publication.
5. Resolve and test the full candidate dependency set. Derive dependency order
   from built metadata; reject cycles and unavailable prerequisites. Test the
   affected consumers even when their unchanged versions will not be published.
6. Publish the selected artifacts through per-project PyPI Trusted Publishers.
   Wait for dependencies to be installable before publishing consumers. A
   package tag such as `varcode/v10.10.0` must match the built version and source.
7. After verifying each successful package/version, record publication state,
   source SHA, hashes, and URLs. Update the version baseline through a reviewed
   state change; a partial failure must preserve completed records and keep
   remaining candidates pending. A state-only commit must not cause new uploads.

Do not attach a generic `uv publish dist/*` to every push. Do not run all legacy
`deploy.sh` scripts after any monorepo merge. Branch protection and release
workflow permissions will be configured with the migrated packages and their
existing PyPI ownership. No production publisher is enabled in this preparation.

## Metapackage and image

Register the `openvax` metapackage like any other distribution when implemented.
Changing its component pins requires its own version bump. Publishing a library
alone does not update the metapackage automatically.

Images are keyed by a released stack version plus an image revision. A base-OS
or runtime-lock update can produce a new image revision without republishing
Python packages. The image pipeline must use verified released artifacts and
record immutable digests. See [combined artifacts](../docs/distribution.md).
