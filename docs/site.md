# Package atlas website

The public GitHub Pages site explains the package ecosystem before migration.
Source lives in `site/`; the `Package atlas` workflow validates PRs and publishes
that directory from `main`. It does not build or upload Python distributions.

## Content and design

Audience: developers and researchers deciding which package handles a task and
how the packages compose. Start with the conceptual variant-to-candidate
workflow, then provide a searchable package map, installation choices, and the
development/release model. Keep existing packages and planned products distinct. Use descriptive technical
headings and factual explanations; avoid slogans and promotional phrasing.

Visual direction: a light scientific atlas with a diagram-led introduction,
grouped package controls, and a persistent detail panel. Palette: ink `#183c56`,
paper white `#ffffff`, pale blue `#eaf3f9`, teal `#147d76`, pale teal `#e6f4ef`,
and amber `#875b17`. Trebuchet headings give the page a humanist shape; Aptos or
the system sans face handles body text. Left-aligned copy, short lines, visible
keyboard focus, and text labels for every relationship make the map readable.
Motion only follows navigation, and respects reduced-motion preferences.

```text
Navigation
Workflow introduction       Three scientific questions
Five-stage conceptual flow
Search + relationship legend
Grouped package map         Selected package details
Individual wheels | Metapackage | Runtime image
Independent development and release example
Migration plan + sources
```

The package controls are grouped by responsibility, not arranged as a universal
pipeline. The workflow follows information through numbered stages; the interactive map uses
direct dependency declarations. This distinction prevents conceptual handoffs
from being mistaken for package requirements.

## Maintaining the content

- `site/packages.json` holds package roles and the selected dependency graph.
  Its initial edges come from the dated source inventory; package descriptions
  are grounded in the source READMEs inspected during site preparation.
- Update the snapshot date and source inventory when refreshing dependency
  edges. Include optional, third-party, or test dependencies only if the legend
  and explanatory text are expanded accordingly.
- Add/remove packages consistently in the JSON and the static repository
  directory in `index.html`. The checker verifies they agree on repository links.
- Keep package names, planned artifacts, and release rules consistent with the
  repository README and distribution design. Do not imply `openvax` or the
  Docker image has shipped before it has.
- External links go to package repositories or repository design documents.
  The static directory and narrative remain usable without JavaScript.

## Preview and validation

No frontend dependencies or build step are needed. From the repository root:

```sh
python3 scripts/check_site.py
node --check site/app.js
python3 -m http.server 8765 --bind 127.0.0.1 --directory site
```

Open `http://127.0.0.1:8765/`. Check desktop and narrow layouts, keyboard focus,
package selection, dependency/consumer highlighting, searching, empty results,
and the repository directory. Serve over HTTP so package JSON can load.

The Pages workflow uploads only `site/`, never local environments or repository
metadata. Pages uses GitHub Actions as its publishing source. Production
publication is restricted to `main`; pull requests run validation only.
