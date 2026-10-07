# OpenVax2 planning repository

## Current scope

The user requested documentation and design planning now, with an implementation
sweep later, after ongoing package PRs finish. Maintain that phase boundary until
the user requests implementation.

- Work on a documentation branch; keep recommendations distinct from accepted
  decisions and observed facts.
- Read sibling repositories as evidence. Preserve their branches, worktrees,
  uncommitted changes, editables, tags, and release state.
- Do not import package source, change dependency bounds, create environments,
  install packages, or enable releases as part of planning.
- Date observations and identify source commits. A local branch is not evidence
  that a PR has merged or a package has shipped.
- Planning documents do not require package version bumps, package tests, or
  releases. Check document links and consistency instead.
- Before implementation, refresh the inventory and read the applicable source
  repository instructions. Resolve their release rules explicitly for the
  monorepo instead of copying automatic release behavior into the root.

## Shared Python environment

When maintaining `/Users/iskander/code/shared-virtual-env`, keep the OpenVax stack
and its dependencies on the most recent mutually compatible stable versions.
Leave unrelated notebook, AI, and other packages outside this maintenance scope.
Upgrade related packages together when necessary to resolve constraints.
Preserve editable checkouts and local work; refresh stale editable package
metadata from the existing checkout. Verify with `pip check` and relevant tests,
and report any constraint that prevents a current version. Do not silently
downgrade packages or force incompatible installs. Distinguish this shared
environment from repository-local release environments.

This planning task does not maintain that environment. Future workspace and
release validation should use dedicated environments. Switching the shared
environment's editable paths is a separate migration step after validation.
