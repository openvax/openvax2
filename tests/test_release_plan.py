import json
from pathlib import Path
import tempfile
import unittest

from scripts.release_plan import plan


class ReleasePlanTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "releases").mkdir()

    def write(self, entries, published):
        for file, packages in [("packages", entries), ("published", published)]:
            (self.root / f"releases/{file}.json").write_text(json.dumps({
                "schema_version": 1, "packages": packages,
            }))

    def package(self, name, version):
        directory = self.root / "packages" / name
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "pyproject.toml").write_text(
            f'[project]\nname = "{name}"\nversion = "{version}"\n'
        )
        return {"name": name, "path": f"packages/{name}"}

    def test_empty_registry_does_nothing(self):
        self.write([], {})
        self.assertEqual(plan(self.root), {"publish": [], "skip": []})

    def test_only_increased_package_is_selected(self):
        self.write([self.package("producer", "1.2.1"), self.package("consumer", "4.0")],
                   {"producer": "1.2.0", "consumer": "4.0.0"})
        result = plan(self.root)
        self.assertEqual([p["name"] for p in result["publish"]], ["producer"])
        self.assertEqual([p["name"] for p in result["skip"]], ["consumer"])

    def test_docs_change_and_repeated_planning_do_not_release_unchanged_package(self):
        self.write([self.package("example", "1.0")], {"example": "1.0"})
        (self.root / "README.md").write_text("Updated docs")
        for _ in range(2):
            self.assertEqual(plan(self.root)["publish"], [])

    def test_pending_bump_survives_later_commits_until_published_state_advances(self):
        entry = self.package("example", "1.1")
        self.write([entry], {"example": "1.0"})
        self.assertEqual(len(plan(self.root)["publish"]), 1)
        (self.root / "README.md").write_text("Later docs change")
        self.assertEqual(len(plan(self.root)["publish"]), 1)
        self.write([entry], {"example": "1.1"})
        self.assertEqual(plan(self.root)["publish"], [])

    def test_unknown_existing_package_requires_baseline(self):
        self.write([self.package("example", "1.0")], {})
        with self.assertRaisesRegex(ValueError, "seed published version"):
            plan(self.root)

    def test_intentional_first_release(self):
        entry = self.package("example", "0.1.0")
        entry["first_release"] = True
        self.write([entry], {})
        self.assertEqual(plan(self.root)["publish"][0]["previous_version"], None)

    def test_downgrade_and_nonstable_versions_rejected(self):
        for version in ["0.9", "1.1rc1", "1.1.dev1", "1.1+local"]:
            with self.subTest(version=version):
                self.write([self.package("example", version)], {"example": "1.0"})
                with self.assertRaises(ValueError):
                    plan(self.root)

    def test_dynamic_version_read_without_executing_module(self):
        entry = self.package("example", "1.0")
        entry["version_file"] = "version.py"
        (self.root / entry["path"] / "version.py").write_text(
            'raise RuntimeError("must not execute")\n__version__ = "1.1"\n'
        )
        self.write([entry], {"example": "1.0"})
        self.assertEqual(plan(self.root)["publish"][0]["version"], "1.1")

    def test_duplicate_normalized_name_rejected(self):
        self.write([self.package("my-lib", "1.0"), self.package("my_lib", "1.0")],
                   {"my-lib": "1.0"})
        with self.assertRaisesRegex(ValueError, "Duplicate package"):
            plan(self.root)

    def test_path_escape_rejected(self):
        entry = self.package("example", "1.0")
        entry["path"] = "../outside"
        self.write([entry], {"example": "1.0"})
        with self.assertRaisesRegex(ValueError, "escapes"):
            plan(self.root)

    def test_source_name_mismatch_rejected(self):
        entry = self.package("example", "1.0")
        entry["name"] = "wrong"
        self.write([entry], {"wrong": "1.0"})
        with self.assertRaisesRegex(ValueError, "does not match"):
            plan(self.root)

    def test_removal_requires_explicit_reconciliation(self):
        self.write([], {"example": "1.0"})
        with self.assertRaisesRegex(ValueError, "removed"):
            plan(self.root)


if __name__ == "__main__":
    unittest.main()
