import copy
import tempfile
import unittest
from pathlib import Path

import yaml

from http_forensics.cases import CaseError, load_case, load_cases, validate

REPO_ROOT = Path(__file__).resolve().parent.parent

VALID = {
    "schema_version": 1,
    "id": "redirect-post-301-001",
    "title": "POST followed by a 301 redirect",
    "question": "Does a client preserve the POST method after a 301 redirect?",
    "category": "redirects",
    "tags": ["redirects", "post"],
    "protocol": ["http/1.1"],
    "clients": ["curl"],
    "servers": ["python-http.server"],
    "environment": {"requires": ["python3", "curl"]},
    "reproduce": "reproduce.sh",
}


def write_case(root, data, text=None):
    """Create cases/<category>/<id>/ with the files a valid case needs."""
    directory = Path(root) / str(data["category"]) / str(data["id"])
    directory.mkdir(parents=True)
    (directory / "README.md").write_text("# test\n")
    (directory / "reproduce.sh").write_text("#!/bin/sh\n")
    path = directory / "case.yaml"
    path.write_text(text if text is not None else yaml.safe_dump(data))
    return path


def variant(**changes):
    data = copy.deepcopy(VALID)
    for key, value in changes.items():
        if value is None:
            data.pop(key, None)
        else:
            data[key] = value
    return data


class ValidateTest(unittest.TestCase):
    def test_valid_case(self):
        self.assertEqual(validate(VALID), [])

    def test_expected_is_optional_but_must_be_a_string(self):
        self.assertEqual(validate(variant(expected="curl switches to GET")), [])
        self.assertTrue(validate(variant(expected=["GET"])))

    def test_not_a_mapping(self):
        self.assertTrue(validate(["id"]))
        self.assertTrue(validate(None))

    def test_missing_id(self):
        self.assertIn("missing required field: id", validate(variant(id=None)))

    def test_invalid_ids(self):
        for bad in ("Redirect-001", "redirect_post_001", "redirect-post", "redirect-post-1", "-redirect-001"):
            with self.subTest(id=bad):
                problems = validate(variant(id=bad))
                self.assertTrue(any("invalid id" in p for p in problems), problems)

    def test_missing_title(self):
        self.assertIn("missing required field: title", validate(variant(title=None)))

    def test_empty_title(self):
        self.assertTrue(validate(variant(title="  ")))

    def test_invalid_category(self):
        problems = validate(variant(category="websockets"))
        self.assertTrue(any("invalid category" in p for p in problems))

    def test_wrong_types(self):
        for field, value in [
            ("title", 42),
            ("tags", "redirects"),
            ("tags", [1, 2]),
            ("protocol", "http/1.1"),
            ("clients", []),
            ("environment", ["curl"]),
            ("environment", {"requires": "curl"}),
            ("schema_version", "1"),
        ]:
            with self.subTest(field=field, value=value):
                self.assertTrue(validate(variant(**{field: value})))

    def test_unsupported_protocol(self):
        problems = validate(variant(protocol=["h3"]))
        self.assertTrue(any("unsupported protocol" in p for p in problems))

    def test_unknown_field(self):
        self.assertIn("unknown field: titel", validate(dict(VALID, titel="typo")))


class LoadTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_load_case(self):
        path = write_case(self.root, VALID)
        case = load_case(path)
        self.assertEqual(case.id, "redirect-post-301-001")
        self.assertEqual(case.category, "redirects")

    def test_malformed_yaml(self):
        path = write_case(self.root, VALID, text="id: [unclosed\ntitle: x: y\n")
        with self.assertRaisesRegex(CaseError, "malformed YAML"):
            load_case(path)

    def test_invalid_case_reports_path_and_problem(self):
        path = write_case(self.root, variant(id="BAD"))
        with self.assertRaisesRegex(CaseError, "invalid id"):
            load_case(path)

    def test_directory_must_match_id(self):
        path = write_case(self.root, VALID)
        moved = path.parent.rename(path.parent.with_name("something-else-001"))
        with self.assertRaisesRegex(CaseError, "must match id"):
            load_case(moved / "case.yaml")

    def test_category_must_match_parent_directory(self):
        path = write_case(self.root, VALID)
        wrong = self.root / "cookies"
        wrong.mkdir()
        moved = path.parent.rename(wrong / path.parent.name)
        with self.assertRaisesRegex(CaseError, "must live under"):
            load_case(moved / "case.yaml")

    def test_reproduce_file_must_exist(self):
        path = write_case(self.root, VALID)
        (path.parent / "reproduce.sh").unlink()
        with self.assertRaisesRegex(CaseError, "missing file: reproduce.sh"):
            load_case(path)

    def test_readme_required(self):
        path = write_case(self.root, VALID)
        (path.parent / "README.md").unlink()
        with self.assertRaisesRegex(CaseError, "missing file: README.md"):
            load_case(path)

    def test_load_cases(self):
        write_case(self.root, VALID)
        write_case(self.root, variant(id="cookie-path-001", category="cookies"))
        ids = [c.id for c in load_cases(self.root)]
        self.assertEqual(ids, ["cookie-path-001", "redirect-post-301-001"])

    def test_duplicate_ids(self):
        write_case(self.root, VALID)
        # Same id under another category: the directory layout is valid, the id is not unique.
        other = write_case(self.root, variant(category="cookies"))
        data = yaml.safe_load(other.read_text())
        self.assertEqual(data["id"], VALID["id"])
        with self.assertRaisesRegex(CaseError, "duplicate id"):
            load_cases(self.root)


class RepositoryCasesTest(unittest.TestCase):
    def test_all_cases_in_repository_are_valid(self):
        cases = load_cases(REPO_ROOT / "cases")
        self.assertTrue(cases)

    def test_reproduce_scripts_are_executable(self):
        for case in load_cases(REPO_ROOT / "cases"):
            script = case.directory / case.data["reproduce"]
            self.assertTrue(script.stat().st_mode & 0o100, f"{script} is not executable")


if __name__ == "__main__":
    unittest.main()
