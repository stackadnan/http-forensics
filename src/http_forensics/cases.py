"""Loading and validation of case.yaml files."""

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

SCHEMA_VERSION = 1

CATEGORIES = ("redirects", "cookies", "caching", "headers", "requests", "responses")
PROTOCOLS = ("http/1.0", "http/1.1")

ID_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*-\d{3}$")
TAG_PATTERN = re.compile(r"^[a-z0-9][a-z0-9.-]*$")

REQUIRED_STRINGS = ("id", "title", "question", "category", "reproduce")
KNOWN_FIELDS = {
    "schema_version", "id", "title", "question", "category", "tags",
    "protocol", "clients", "servers", "environment", "reproduce", "expected",
}


class CaseError(Exception):
    """A case.yaml could not be read or does not follow the schema."""


@dataclass
class Case:
    path: Path
    data: dict

    @property
    def id(self):
        return self.data["id"]

    @property
    def category(self):
        return self.data["category"]

    @property
    def directory(self):
        return self.path.parent


def _is_string_list(value):
    return isinstance(value, list) and all(isinstance(v, str) and v for v in value)


def validate(data):
    """Return a list of problems found in a parsed case. Empty means valid."""
    if not isinstance(data, dict):
        return ["case must be a YAML mapping"]

    problems = []

    if data.get("schema_version") != SCHEMA_VERSION:
        problems.append(f"schema_version must be {SCHEMA_VERSION}")

    for field in REQUIRED_STRINGS:
        if field not in data:
            problems.append(f"missing required field: {field}")
        elif not isinstance(data[field], str) or not data[field].strip():
            problems.append(f"{field} must be a non-empty string")

    case_id = data.get("id")
    if isinstance(case_id, str) and not ID_PATTERN.match(case_id):
        problems.append(f"invalid id {case_id!r}: expected lowercase words ending in a 3-digit number, e.g. redirect-post-301-001")

    category = data.get("category")
    if isinstance(category, str) and category not in CATEGORIES:
        problems.append(f"invalid category {category!r}: expected one of {', '.join(CATEGORIES)}")

    for field in ("tags", "protocol", "clients", "servers"):
        if field not in data:
            problems.append(f"missing required field: {field}")
        elif not _is_string_list(data[field]) or not data[field]:
            problems.append(f"{field} must be a non-empty list of strings")

    for tag in data.get("tags") or []:
        if isinstance(tag, str) and not TAG_PATTERN.match(tag):
            problems.append(f"invalid tag {tag!r}: use lowercase letters, digits, '.' and '-'")

    for protocol in data.get("protocol") or []:
        if isinstance(protocol, str) and protocol not in PROTOCOLS:
            problems.append(f"unsupported protocol {protocol!r}: expected one of {', '.join(PROTOCOLS)}")

    environment = data.get("environment")
    if not isinstance(environment, dict) or not _is_string_list(environment.get("requires")):
        problems.append("environment must be a mapping with a 'requires' list of strings")

    if "expected" in data and (not isinstance(data["expected"], str) or not data["expected"].strip()):
        problems.append("expected must be a non-empty string when present")

    for field in sorted(set(data) - KNOWN_FIELDS):
        problems.append(f"unknown field: {field}")

    return problems


def load_case(path):
    """Read and validate one case.yaml, also checking it against its location."""
    path = Path(path)
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise CaseError(f"{path}: malformed YAML: {exc}") from exc
    except OSError as exc:
        raise CaseError(f"{path}: cannot read file: {exc}") from exc

    problems = validate(data)
    if not problems:
        directory = path.parent
        if directory.name != data["id"]:
            problems.append(f"directory name {directory.name!r} must match id {data['id']!r}")
        if directory.parent.name != data["category"]:
            problems.append(f"case must live under cases/{data['category']}/")
        for name in (data["reproduce"], "README.md"):
            if not (directory / name).is_file():
                problems.append(f"missing file: {name}")
    if problems:
        raise CaseError(f"{path}: " + "; ".join(problems))

    return Case(path=path, data=data)


def load_cases(root):
    """Load every case under root, failing on any invalid case or duplicate id."""
    cases = []
    seen = {}
    for path in sorted(Path(root).glob("*/*/case.yaml")):
        case = load_case(path)
        if case.id in seen:
            raise CaseError(f"duplicate id {case.id!r} in {seen[case.id]} and {path}")
        seen[case.id] = path
        cases.append(case)
    return cases
