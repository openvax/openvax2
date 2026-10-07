#!/usr/bin/env python3
"""Plan version-gated releases. Never build, upload, or change release state."""

import argparse
import ast
import json
from pathlib import Path
import sys
import tomllib

from packaging.utils import canonicalize_name
from packaging.version import Version


def load_manifest(path):
    data = json.loads(path.read_text())
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError(f"Unsupported manifest schema: {path}")
    return data["packages"]


def contained_path(root, relative):
    if not isinstance(relative, str) or Path(relative).is_absolute():
        raise ValueError(f"Expected relative path: {relative!r}")
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"Path escapes its package or repository: {relative}")
    return path


def stable_version(value):
    if not isinstance(value, str):
        raise ValueError("Versions must be strings")
    version = Version(value)
    if version.is_prerelease or version.is_devrelease or version.local is not None:
        raise ValueError(f"Expected a stable public version: {value}")
    return version


def package_version(root, entry, name):
    package = contained_path(root, entry["path"])
    source = entry.get("version_file")
    if source is None:
        metadata = tomllib.loads((package / "pyproject.toml").read_text())["project"]
        if canonicalize_name(metadata["name"], validate=True) != name:
            raise ValueError(f"Project name does not match registry: {name}")
        return stable_version(metadata["version"])
    source = contained_path(package, source)
    variable = entry.get("version_variable", "__version__")
    values = []
    for node in ast.parse(source.read_text()).body:
        targets = node.targets if isinstance(node, ast.Assign) else (
            [node.target] if isinstance(node, ast.AnnAssign) else []
        )
        if any(isinstance(target, ast.Name) and target.id == variable for target in targets):
            values.append(ast.literal_eval(node.value))
    if len(values) != 1:
        raise ValueError(f"Expected one literal {variable} assignment in {source}")
    return stable_version(values[0])


def plan(root):
    entries = load_manifest(root / "releases/packages.json")
    published = load_manifest(root / "releases/published.json")
    if not isinstance(entries, list) or not isinstance(published, dict):
        raise ValueError("Expected a package list and a published-version mapping")
    known = {}
    for name, version in published.items():
        normalized = canonicalize_name(name, validate=True)
        if normalized in known:
            raise ValueError(f"Duplicate published package: {normalized}")
        known[normalized] = stable_version(version)
    result = {"publish": [], "skip": []}
    seen = set()
    for entry in entries:
        name = canonicalize_name(entry["name"], validate=True)
        if name in seen:
            raise ValueError(f"Duplicate package registration: {name}")
        seen.add(name)
        current = package_version(root, entry, name)
        previous = known.get(name)
        if previous is None and entry.get("first_release") is not True:
            raise ValueError(f"{name}: seed published version or explicitly set first_release")
        if previous is not None and current < previous:
            raise ValueError(f"{name}: version decreased from {previous} to {current}")
        if previous is not None and current == previous:
            result["skip"].append({"name": name, "version": str(current), "reason": "unchanged version"})
        else:
            result["publish"].append({
                "name": name,
                "path": entry["path"],
                "version": str(current),
                "previous_version": str(previous) if previous is not None else None,
            })
    if set(known) - seen:
        raise ValueError("Published packages removed from registry; reconcile retirement explicitly")
    for rows in result.values():
        rows.sort(key=lambda row: row["name"])
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        result = plan(args.root.resolve())
    except (ValueError, TypeError, KeyError, OSError, SyntaxError) as error:
        print(f"Release planning failed: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
