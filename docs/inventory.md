# Source inventory

Observed 2026-10-07 from local checkouts. This is a planning sample, not a complete
organization census or a verified migration baseline. Repository identities below
come from local `origin` URLs; canonical ownership and redirects must be checked
before import. Several checkouts are on feature branches. Remote PR status and
current PyPI versions were not queried.

Metadata was read at each recorded commit without executing package setup code.
Working-tree edits were excluded. `oncoref` and `pirlygenes` had tracked local
changes at inspection time; those changes are not represented here. No source
checkout or Python environment was changed.

## Candidate packages

"Core" and "evaluate" are proposed scope, not accepted membership. "External"
means keep the package outside the initial import while testing any required
runtime dependency normally. Python ranges are declarations, not verified support.

| Package | Source repository / recorded commit | Python | Initial disposition |
| --- | --- | --- | --- |
| `datacache` | [openvax/datacache @ 3e81c40957d3](https://github.com/openvax/datacache/tree/3e81c40957d37a752ceafb4273c3e341cd19658d) | `>=3.9` | Core candidate |
| `gtfparse` | [openvax/gtfparse @ a80b0827e982](https://github.com/openvax/gtfparse/tree/a80b0827e982c32409d78aa707d6350374b6555a) | `>=3.9` | Core candidate |
| `pyensembl` | [openvax/pyensembl @ 8de64486e096](https://github.com/openvax/pyensembl/tree/8de64486e096e57752d279632ddbb80ff56bf026) | `>=3.9` | Core candidate |
| `varcode` | [openvax/varcode @ 72c2e6ce3e61](https://github.com/openvax/varcode/tree/72c2e6ce3e6181130a444082ff16d299b3d12b71) | `>=3.9` | Core candidate |
| `isovar` | [openvax/isovar @ 511ae460a383](https://github.com/openvax/isovar/tree/511ae460a383485beff6f47c9c1f8e22dfdd8346) | `>=3.9` | Core candidate |
| `mhcgnomes` | [pirl-unc/mhcgnomes @ 5565acdc4f8e](https://github.com/pirl-unc/mhcgnomes/tree/5565acdc4f8e2d13b4255c4f742f18178fe5efae) | `>=3.9` | Evaluate with core |
| `mhcseqs` | [pirl-unc/mhcseqs @ 135b1e3f41c5](https://github.com/pirl-unc/mhcseqs/tree/135b1e3f41c52be4b4b3af7aa35d6296e3524b0f) | `>=3.10` | External initially |
| `mhctools` | [openvax/mhctools @ 434b4320a69e](https://github.com/openvax/mhctools/tree/434b4320a69ea638f9efc7710b99987a8f6790ab) | `>=3.9` | Core candidate |
| `topiary` | [openvax/topiary @ 62cf7ca8b41c](https://github.com/openvax/topiary/tree/62cf7ca8b41c4dc9a04ab25f28ee30213b13ffdf) | `>=3.10` | Core candidate |
| `vaxrank` | [openvax/vaxrank @ 54c3200db824](https://github.com/openvax/vaxrank/tree/54c3200db8244fd025701980446b4e920667f0dd) | `>=3.10` | Core candidate |
| `serializable` | [iskandr/serializable @ 83dbac8fcd29](https://github.com/iskandr/serializable/tree/83dbac8fcd290bfc1b43c82cd4bc09e083ca3934) | `>=3.9` | Evaluate with core |
| `sercol` | [openvax/sercol @ 4125930bead8](https://github.com/openvax/sercol/tree/4125930bead84738bd45265151297c18bc8c3d52) | `>=3.9` | Core candidate |
| `mhcflurry` | [openvax/mhcflurry @ 5744b647e709](https://github.com/openvax/mhcflurry/tree/5744b647e7099df147c6657e297749164bf35e2f) | `>=3.10` | External initially |
| `osteosarc` | [iskandr/osteosarc @ 27d2901da09f](https://github.com/iskandr/osteosarc/tree/27d2901da09f16545acb124cc245f2200fefa73f) | `>=3.9` | External initially |
| `oncoref` | [pirl-unc/oncoref @ b242d3ac604c](https://github.com/pirl-unc/oncoref/tree/b242d3ac604c2b868003a3db4c9215b3e021b688) | `>=3.9` | External initially |
| `pirlygenes` | [pirl-unc/pirlygenes @ cefb19ce20ed](https://github.com/pirl-unc/pirlygenes/tree/cefb19ce20ede3aa3d6e3d563eef9c31136930ba) | `>=3.9` | External initially |

## Declared relationships within this sample

The table lists direct runtime dependencies on other sampled packages. It omits
third-party requirements, extras, test/build dependencies, and dynamic imports;
it must not be used as a complete CI change-selection graph. Source links point
to the recorded commit.

| Consumer | Sampled direct dependencies | Metadata source |
| --- | --- | --- |
| `datacache` | None in this sample | [requirements.txt](https://github.com/openvax/datacache/blob/3e81c40957d37a752ceafb4273c3e341cd19658d/requirements.txt) |
| `gtfparse` | None in this sample | [requirements.txt](https://github.com/openvax/gtfparse/blob/a80b0827e982c32409d78aa707d6350374b6555a/requirements.txt) |
| `pyensembl` | `datacache[progress]>=1.14.0,<2.0.0`, `gtfparse>=2.9.0,<4.0.0`, `serializable>=0.2.1,<2.0.0` | [pyproject.toml](https://github.com/openvax/pyensembl/blob/8de64486e096e57752d279632ddbb80ff56bf026/pyproject.toml) |
| `varcode` | `pyensembl>=2.24.1`, `gtfparse>=3.0.2,<4.0.0`, `serializable>=1.1.0`, `sercol>=1.0.3` | [requirements.txt](https://github.com/openvax/varcode/blob/72c2e6ce3e6181130a444082ff16d299b3d12b71/requirements.txt) |
| `isovar` | `pyensembl>=1.5.0`, `varcode>=10.5.2,<11`, `osteosarc>=0.15.4,<0.16` | [requirements.txt](https://github.com/openvax/isovar/blob/511ae460a383485beff6f47c9c1f8e22dfdd8346/requirements.txt) |
| `mhcgnomes` | None in this sample | [pyproject.toml](https://github.com/pirl-unc/mhcgnomes/blob/5565acdc4f8e2d13b4255c4f742f18178fe5efae/pyproject.toml) |
| `mhcseqs` | `mhcgnomes>=3.41.0` | [pyproject.toml](https://github.com/pirl-unc/mhcseqs/blob/135b1e3f41c52be4b4b3af7aa35d6296e3524b0f/pyproject.toml) |
| `mhctools` | `pyensembl>=2.3.0,<3.0.0`, `sercol>=0.0.2`, `mhcflurry>=2.0.0`, `mhcgnomes>=3.4.0` | [pyproject.toml](https://github.com/openvax/mhctools/blob/434b4320a69ea638f9efc7710b99987a8f6790ab/pyproject.toml) |
| `topiary` | `mhctools>=3.45.1`, `varcode>=4.18.0`, `gtfparse>=3.0.2,<4.0.0`, `mhcgnomes>=3.4.0`, `pyensembl>=2.24.1,<3.0.0`, `osteosarc>=0.14.0,<0.16` | [requirements.txt](https://github.com/openvax/topiary/blob/62cf7ca8b41c4dc9a04ab25f28ee30213b13ffdf/requirements.txt) |
| `vaxrank` | `datacache>=1.14.0,<2.0.0`, `osteosarc>=0.14.4,<0.15`, `pyensembl>=2.16.0,<3.0.0`, `varcode>=10.9.0,<11.0.0`, `isovar>=1.39.11,<1.40.0`, `mhcgnomes>=3.64.4,<4.0.0`, `mhctools>=3.44.64,<4.0.0`, `topiary>=5.86.1,<6.0.0`, `serializable>=1.1.0,<2.0.0`, `oncoref==1.8.206` | [setup.py + requirements.txt](https://github.com/openvax/vaxrank/blob/54c3200db8244fd025701980446b4e920667f0dd/setup.py) |
| `serializable` | None in this sample | [pyproject.toml](https://github.com/iskandr/serializable/blob/83dbac8fcd290bfc1b43c82cd4bc09e083ca3934/pyproject.toml) |
| `sercol` | `serializable>=1.0.0,<2.0.0` | [requirements.txt](https://github.com/openvax/sercol/blob/4125930bead84738bd45265151297c18bc8c3d52/requirements.txt) |
| `mhcflurry` | `mhcgnomes>=3.33.6` | [setup.py](https://github.com/openvax/mhcflurry/blob/5744b647e7099df147c6657e297749164bf35e2f/setup.py) |
| `osteosarc` | `datacache>=1.12.0` | [pyproject.toml](https://github.com/iskandr/osteosarc/blob/27d2901da09f16545acb124cc245f2200fefa73f/pyproject.toml) |
| `oncoref` | None in this sample | [pyproject.toml](https://github.com/pirl-unc/oncoref/blob/b242d3ac604c2b868003a3db4c9215b3e021b688/pyproject.toml) |
| `pirlygenes` | `oncoref==1.8.194`, `pyensembl>=2.6.0` | [pyproject.toml](https://github.com/pirl-unc/pirlygenes/blob/cefb19ce20ede3aa3d6e3d563eef9c31136930ba/pyproject.toml) |

## Constraints to revisit after the ongoing PRs

1. **The sampled source versions are not a compatible release set.** The recorded
   [Isovar requirements](https://github.com/openvax/isovar/blob/511ae460a383485beff6f47c9c1f8e22dfdd8346/requirements.txt)
   require `osteosarc>=0.15.4,<0.16`, while the recorded
   [Vaxrank requirements](https://github.com/openvax/vaxrank/blob/54c3200db8244fd025701980446b4e920667f0dd/requirements.txt)
   require `osteosarc>=0.14.4,<0.15`. Those ranges do not overlap. This is evidence
   that these particular source snapshots cannot share one resolution, not a
   finding that the currently published Vaxrank dependency set is broken. Vaxrank
   also selects an older Isovar minor series. Refresh both after their intended
   PRs and adaptations land.

2. **External membership does not eliminate runtime requirements.**
   [MHCTools](https://github.com/openvax/mhctools/blob/434b4320a69ea638f9efc7710b99987a8f6790ab/pyproject.toml)
   declares MHCflurry as a runtime dependency. Keeping MHCflurry outside the
   first import still requires the selected released MHCflurry and its runtime
   dependencies to resolve in relevant MHCTools environments. Changing that
   dependency to an extra would be a separate product/API decision.

3. **Adjacent projects can have conflicting exact references.** Vaxrank selects
   `oncoref==1.8.206`; the recorded
   [PirlyGenes metadata](https://github.com/pirl-unc/pirlygenes/blob/cefb19ce20ede3aa3d6e3d563eef9c31136930ba/pyproject.toml)
   selects `oncoref==1.8.194`. These snapshots cannot be combined unchanged in
   one environment. This matters if PirlyGenes is later included or the shared
   environment is maintained; it does not by itself block a core-only import.

4. **Packaging authority varies.** Most candidates use setuptools through
   `pyproject.toml`; several load dependencies from `requirements.txt`.
   [Vaxrank](https://github.com/openvax/vaxrank/blob/54c3200db8244fd025701980446b4e920667f0dd/setup.py) and
   [MHCflurry](https://github.com/openvax/mhcflurry/blob/5744b647e7099df147c6657e297749164bf35e2f/setup.py)
   currently build through `setup.py`. MHCflurry declares its install requirements
   directly there; a requirements-file scan alone misses `ahocorasick-rs`.
   [MHCgnomes](https://github.com/pirl-unc/mhcgnomes/blob/5565acdc4f8e2d13b4255c4f742f18178fe5efae/pyproject.toml)
   declares dependencies directly in `pyproject.toml`, so its separate
   `requirements.txt` should not be mistaken for wheel metadata. Verify built
   distribution metadata during implementation.

5. **Release automation is heterogeneous.** Most sampled core repositories have
   a `deploy.sh`; MHCflurry instead documents its release process in
   [CONTRIBUTING.md](https://github.com/openvax/mhcflurry/blob/5744b647e7099df147c6657e297749164bf35e2f/CONTRIBUTING.md) and
   [model release instructions](https://github.com/openvax/mhcflurry/blob/5744b647e7099df147c6657e297749164bf35e2f/scripts/release/README.md).
   MHCgnomes and MHCseqs also have release workflows. Inventory triggers, version
   sources, tags, credentials/publishers, docs deployment, and script assumptions
   before replacing any release path. Do not execute deployment scripts merely
   to inspect them.

## Scope intentionally left open

Other local OpenVax repositories include `pepdata`, `varlens`, `gene-lists`,
`netmhc-bundle`, and the organization website. They were not deeply inventoried
for the initial migration. Small dependencies such as `typechecks`,
`memoized-property`, and `tinytimer` remain ordinary external dependencies unless
their inclusion has a concrete maintenance benefit. Additional local worktrees
of the same repository are not separate packages.

## Refresh before implementation

Use the [readiness register](migration-plan.md) to replace this exploratory
snapshot with selected merged source commits and verified release versions.
Read runtime and optional dependencies from the authoritative build metadata,
add test/build/data relationships, and check the intended Python/platform
combinations. Preserve local changes and editable paths during that work.
