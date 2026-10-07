"""Validate the static atlas and its package references before deployment."""

from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.selections = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                raise ValueError(f"Duplicate HTML id: {attrs['id']}")
            self.ids.add(attrs["id"])
        for attribute in ("href", "src"):
            if attribute in attrs:
                self.links.append(attrs[attribute])
        if "data-select" in attrs:
            self.selections.append(attrs["data-select"])


def main():
    root = Path(__file__).resolve().parents[1] / "site"
    page = Page()
    page.feed((root / "index.html").read_text())
    for target in page.links:
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc:
            continue
        path = (root / unquote(parsed.path)).resolve() if parsed.path else root / "index.html"
        if path.is_dir():
            path /= "index.html"
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError(f"Missing or escaping local asset: {target}")
        if parsed.fragment and path == root / "index.html" and parsed.fragment not in page.ids:
            raise ValueError(f"Unknown fragment: {target}")
    data = json.loads((root / "packages.json").read_text())
    packages = data["packages"]
    names = [package["id"] for package in packages]
    if not names or len(set(names)) != len(names):
        raise ValueError("Package identifiers must be unique and nonempty")
    required = ("label", "category", "tagline", "summary", "input", "output", "boundary", "repository")
    for package in packages:
        if any(not isinstance(package.get(key), str) or not package[key].strip() for key in required):
            raise ValueError(f"Incomplete package description: {package['id']}")
        if not package["repository"].startswith("https://github.com/"):
            raise ValueError(f"Invalid package repository: {package['id']}")
        if package["repository"] not in page.links:
            raise ValueError(f"Package missing from static directory: {package['id']}")
        for dependency in package["dependencies"]:
            if dependency not in names or dependency == package["id"]:
                raise ValueError(f"Invalid dependency: {package['id']} -> {dependency}")
    if set(page.selections) - set(names):
        raise ValueError("Workflow links refer to unknown packages")
    print(f"Atlas validated: {len(names)} packages, {len(page.links)} links/assets, all dependency targets present.")


if __name__ == "__main__":
    main()
