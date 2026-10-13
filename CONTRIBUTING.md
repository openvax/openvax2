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

The current plan should contain empty `publish` and `skip` arrays.

Root documentation and tooling changes do not require library version bumps.
Do not invent placeholder package versions, create empty PyPI projects, or
migrate source just to populate the registry. Preserve the shared environment
as described in [AGENTS.md](AGENTS.md).

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

Workspace dependencies resolve to sibling source, so an edit to `pyensembl`
can be tested immediately through `varcode`. Selecting one member does not
create a separate virtual environment for it; see
[uv workspace behavior](https://docs.astral.sh/uv/concepts/projects/workspaces/).

The direct pytest command above is the simple case. Where a package has its
own lint or test wrapper that sets up its environment or fixtures, keep using it.

For a public API change, identify and test transitive consumers. CI initially
runs all core suites, then may select affected suites once dependency tracking
is proven. Do not remove a compatibility bound merely to make a local sync pass.

## Independent-package validation

A workspace install can hide missing dependencies, so check each changed
package as a standalone wheel. After migration:

1. Build from the package directory with workspace sources disabled:

   ```sh
   # Run from packages/varcode; uv must be available on PATH.
   uv build --no-sources --out-dir /tmp/openvax-varcode-dist
   ```

2. Install that exact wheel into a fresh environment outside the checkout, with
   no editable installs and no `PYTHONPATH` pointing at source. If the change
   needs an unreleased sibling, install its candidate wheel in the same
   environment.
3. Run `python -m pip check`, import, CLI, and resource checks, and the
   package's behavioral tests.
4. Build a wheel from the sdist as well and check it the same way.

`--no-sources` only checks that the build does not rely on workspace sources;
steps 2 to 4 test the runtime dependencies. A separate validation lane checks
compatibility with released dependencies where applicable. See
[uv build guidance](https://docs.astral.sh/uv/guides/package/).

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
