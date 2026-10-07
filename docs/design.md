# Proposed monorepo design

Status: proposed, 2026-10-07. Package scope and cutover await the
[decision log](decisions.md) and [migration gates](migration-plan.md).

## Problem and intended behavior

Changes to shared APIs currently require coordinated updates across separate
repositories, dependency declarations, CI configurations, and releases. The
monorepo should allow a producer change and its consumer updates to be reviewed
and tested in one PR. Users should continue installing the individual packages
they need from PyPI.

Success means less coordination work without hiding incompatibilities behind a
development environment. Moving files alone will not fix version constraints or
automate releases.

## Package boundaries and layout

Start by evaluating `datacache`, `gtfparse`, `sercol`, `pyensembl`, `varcode`,
`isovar`, `mhctools`, `topiary`, and `vaxrank`. Evaluate `serializable` and
`mhcgnomes` alongside them, with their source ownership confirmed. The
[inventory](inventory.md) distinguishes these candidates from adjacent projects.

Proposed eventual structure; these directories are not implemented yet:

```text
openvax2/
  pyproject.toml           # non-published workspace/tooling root
  uv.lock
  packages/
    pyensembl/
      pyproject.toml
      pyensembl/
      tests/
      LICENSE
    varcode/
    isovar/
    ...
  docs/
  .github/workflows/
```

Preserve each package's existing internal layout, public imports, CLI names,
data files, tests, version source, and license notices during import. A wholesale
move to `src/`, API consolidation, build-backend replacement, and scientific
behavior changes are separate work. Add the minimal packaging configuration
needed for workspace membership where it is missing.

Repository membership and environment membership are separate decisions.
MHCflurry can remain an external package initially; if imported later, its model
and training workflows can remain separate from the core workspace. Heavy model
files, reference downloads, caches, and analysis outputs do not belong in the
source import. Preserve mechanisms for acquiring required versioned assets.

## Development dependencies and published dependencies

uv workspaces provide member-specific `pyproject.toml` files, a common lockfile,
and editable dependencies between members. Use explicit workspace membership
and source mappings for the selected packages. A member excluded from the
workspace needs separate environment configuration; exclusion does not make its
runtime dependency disappear from consumers.
[uv workspace reference](https://docs.astral.sh/uv/concepts/projects/workspaces/)

Maintain three distinct concerns:

| Concern | Authority | Intended use |
| --- | --- | --- |
| Public compatibility | Each distribution's build metadata | Dependencies pip resolves for users |
| Workspace source selection | Workspace source mappings | Develop against sibling source |
| Reproducible development | Workspace lockfile | Repeat the tested development resolution |

Keep ordinary package-name dependencies and meaningful version bounds in each
distribution. Workspace sources select local code during development; they do
not replace published dependency declarations. Development groups should not
become runtime requirements. Preserve current dynamic requirements-file readers
until a deliberate metadata migration removes duplication.
[uv dependency fields](https://docs.astral.sh/uv/concepts/projects/dependencies/#dependency-fields)

Prefer the most recent mutually compatible stable dependency set. When a newer
version is blocked, report the blocking declarations and test the required
consumer adaptations. Do not delete upper bounds or use resolver overrides just
to make the workspace install. A library's lower bound should reflect the first
version whose API it actually uses; an upper bound needs a documented reason.
One shared lockfile cannot promise all combinations allowed by package metadata.

The initial Python development version remains to be selected. Some candidate
packages declare Python 3.9+, others 3.10+. uv uses the intersection of members'
Python requirements. Preserve individual support promises and test them outside
the workspace when necessary; do not raise every minimum merely to simplify CI.
[Workspace Python constraints](https://docs.astral.sh/uv/concepts/projects/workspaces/#when-not-to-use-workspaces)

The workspace environment is separate from `shared-virtual-env` and from clean
release environments. See [AGENTS.md](../AGENTS.md) for the shared environment's
maintenance requirements.

## CI and validation

Begin with all core package suites for package changes. Add selective execution
only after there is evidence that change detection is reliable. The eventual
selection includes changed packages and their transitive consumers, with
runtime, optional, build, and shared-test relationships represented. Changes to
the lockfile, shared tools, or selection logic trigger the full applicable set.

Run package suites separately from their package roots to preserve fixture paths
and avoid collisions between identically named `tests` modules. Retain existing
lint and test scripts during the first migration, adapting assumptions about
working directories and repository roots deliberately. Tool configuration
inheritance must be explicit; nested configurations can override root settings.

| Validation lane | What it proves |
| --- | --- |
| Workspace integration | Coordinated source changes work together |
| Isolated wheel installation | Imports, CLI, package data, and declared dependencies work without checkout leakage |
| Candidate release set | New producer and consumer wheels resolve and operate together before upload |
| Supported Python/platform matrix | Package support promises remain true outside the common development environment |
| Compatibility boundary tests | Representative minimum dependencies and current stable dependencies exercise supported APIs |
| Data/model integration | Versioned fixtures and predictors still produce expected results where affected |

For isolated wheel tests, start outside the checkout with a clean environment,
no editable installs, and no source-path injection. Install only the target wheel,
its declared dependency closure, and explicitly identified test tooling. Test
dependencies must not conceal missing runtime requirements. Run `pip check` as
well as behavioral tests. Build a wheel from the sdist too, checking that license
files, templates, configuration, and required data survived packaging.

A package relying on another package's new API must use that candidate wheel in
the pre-release lane. Test unaffected consumers against released dependencies
where relevant; do not require unreleased wheels to already exist on PyPI.

## Versioning and release behavior

Keep independent package versions and changelogs. A PR identifies packages with
code, metadata, or shipped-data changes and supplies their version/release-note
updates. If a consumer starts requiring a new producer version, its changed
dependency metadata requires a consumer release even if its code is unchanged.
An unchanged consumer whose existing bounds still apply does not need a release.
Root planning and tooling documentation alone should not release every package.
This proposed policy must explicitly replace conflicting imported instructions.

Release tags are package-qualified, for example `varcode/v10.10.0` (illustrative,
not a reserved release). Each package keeps one authoritative version source;
the build and tag must agree. No repository-wide version is required.

The proposed release workflow is:

1. Produce a reviewable manifest of package names, versions, source commit,
   dependency changes, and required verification.
2. Build only the planned distributions from a clean checkout. Confirm each
   sdist builds independently; collect artifact hashes.
3. Validate isolated installs and the complete candidate dependency set.
4. Publish the verified artifacts in dependency order, waiting for availability
   before publishing consumers that require them.
5. Verify registry installs and record tags, artifacts, and release notes per
   package. Record any partial completion and resume from that state.

uv can build a named workspace member; `uv build --no-sources` checks that build
dependencies do not require workspace-specific sources. That check does not
replace testing runtime dependencies from built wheels.
[uv build and publishing guide](https://docs.astral.sh/uv/guides/package/)

Multi-package publication is not atomic. A failure must not cause an already
uploaded version to be rebuilt or replaced. Retry identical verified artifacts;
release a new version for corrections. Stop consumer publication if a required
producer is unavailable. Detect dependency cycles before scheduling releases
and resolve them explicitly rather than assuming a topological order exists.

Preserve existing PyPI projects and ownership. Configure the new GitHub publisher
for each participating PyPI project, including the correct repository, workflow,
and release environment. Test the publishing path before retiring old automation,
and ensure there is only one active release authority per package at cutover.
[PyPI Trusted Publisher configuration](https://docs.pypi.org/trusted-publishers/adding-a-publisher/)

## Alternatives and costs

Keeping separate repositories with common CI and dependency-update automation
would reduce repeated maintenance, but cross-package changes would still span
multiple PRs. Use that approach for packages with separate ownership or weak
coupling. A single combined distribution would reduce release count but change
the installation footprint and existing package boundaries. A single version
for every distribution would simplify numbering at the cost of unrelated releases.

The monorepo adds migration work for history, issue links, CI paths, documentation
hosting, and publishing permissions. The first implementation should preserve
behavior and measure whether a representative producer/consumer change can be
tested and released with less manual coordination before expanding the scope.
