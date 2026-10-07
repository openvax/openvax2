# Contributing to OpenVax2

## Current phase: design and release-tooling preparation

Open a branch and PR for changes. The repository currently contains documentation
and a release planner, with no imported library packages. Run these checks using
Python 3.11 or later in a repository-local environment:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/release_plan.py
git diff --check
```

The current plan should contain empty `publish` and `skip` arrays. Do not invent
placeholder package versions, create empty PyPI projects, or migrate source just
to populate the registry. Root documentation/tooling changes do not require
library version bumps. Preserve the shared environment as described in
[AGENTS.md](AGENTS.md).

## After migration: work on one package

The following commands describe the intended workflow after the workspace and
its `test` dependency group exist. They are not runnable in today's scaffold.

```sh
# From the monorepo root, install varcode and its dependency closure.
uv sync --package varcode --group test

# Run from the package directory so tests and fixtures have their expected paths.
cd packages/varcode
uv run --package varcode --group test python -m pytest tests
```

Workspace dependencies resolve to sibling source, so editing `pyensembl` can be
tested immediately through `varcode`. Selecting one member does not create a
separate virtual environment per member. Preserve each package's established
lint/test wrapper where it supplies required environment or fixture setup;
the direct pytest command above is the simple case.
[uv workspace behavior](https://docs.astral.sh/uv/concepts/projects/workspaces/)

For a public API change, identify and test transitive consumers. CI initially
runs all core suites, then may select affected suites once dependency tracking
is proven. Do not remove a compatibility bound merely to make a local sync pass.

## Independent-package validation

Build from the package directory with workspace sources disabled, then test the
wheel in a fresh environment outside the checkout. For example, after migration:

```sh
# Run from packages/varcode; uv must be available on PATH.
uv build --no-sources --out-dir /tmp/openvax-varcode-dist
```

Install the resulting exact wheel into a dedicated test environment and run
`python -m pip check`, import/CLI/resource checks, and its behavioral tests without
editable installs or `PYTHONPATH` pointing at source. Build from the sdist too.
If the change needs an unreleased sibling, install its candidate wheel in the
same clean environment. A separate lane checks compatibility with released
dependencies where applicable. The build flag alone does not test runtime
dependency correctness.
[uv build guidance](https://docs.astral.sh/uv/guides/package/)

## Cross-package PRs and versions

Keep implementation and consumer changes together. Identify touched packages,
new API requirements, and validation in the PR. When ready to release, bump the
existing authoritative version in each affected package and update its notes.
Published dependency metadata changes count as package changes. Do not bump an
unchanged consumer just because it depends on a newly released producer.

Example: change `varcode` and adapt `isovar`; release those two if both need new
versions. If `gtfparse` is unchanged, its version and PyPI files remain untouched.
Tests may run for all three. If an `openvax` stack release should adopt the new
pair, update its exact component pins, run stack integration tests, and bump its
own version. Otherwise, existing stack releases keep their previous pins.

Never publish from a working developer environment. The future release job
builds from a clean selected commit, validates candidate artifacts, and uploads
those exact files. See [release policy](releases/README.md).

## Contributions and licensing

New original contributions use Apache 2.0. Keep existing copyright/license
notices when importing source and document third-party material separately.
