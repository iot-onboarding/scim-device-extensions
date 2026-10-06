#!/usr/bin/env python3
# Copyright 2026 Cisco Systems, Inc. and its affiliates
# SPDX-License-Identifier: Apache-2.0
"""Validate SCIM Schema resources against the repository authoring profile."""

import argparse
from dataclasses import dataclass
import json
import math
from pathlib import Path
import re
import sys

from jsonschema import Draft202012Validator, FormatChecker


REPOSITORY = Path(__file__).resolve().parents[1]
DEFINITION = REPOSITORY / "scripts" / "scim-schema-resource.schema.json"
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
ATTRIBUTE_NAME = re.compile(r"[A-Za-z][A-Za-z0-9$_-]*")


@dataclass(frozen=True)
class Issue:
    file: Path
    path: tuple
    message: str

    def __str__(self):
        pointer = "$" + "".join(
            f"[{part}]" if isinstance(part, int) else f"[{json.dumps(part)}]"
            for part in self.path
        )
        return f"{self.file}: {pointer}: {self.message}"


class ObjectPairs(list):
    """Distinguish JSON objects from arrays until duplicate keys are checked."""


class InvalidJSON(ValueError):
    def __init__(self, path, message):
        self.path = path
        super().__init__(message)


def load_json(path):
    """Read strict UTF-8 JSON while retaining paths for duplicate keys."""
    def reject_constant(value):
        raise InvalidJSON((), f"non-finite constant {value} is not JSON")

    def unpack(value, pointer=()):
        if isinstance(value, ObjectPairs):
            result = {}
            for key, child in value:
                if key in result:
                    raise InvalidJSON(pointer + (key,), "duplicate JSON object key")
                result[key] = unpack(child, pointer + (key,))
            return result
        if isinstance(value, list):
            return [unpack(child, pointer + (index,)) for index, child in enumerate(value)]
        # An overflowing exponent such as 1e9999 can become infinity even though
        # parse_constant rejects the literal Infinity.
        if isinstance(value, float):
            if not math.isfinite(value):
                raise InvalidJSON(pointer, "number is outside finite JSON range")
        return value

    return unpack(json.loads(
        Path(path).read_text(encoding="utf-8"),
        object_pairs_hook=ObjectPairs,
        parse_constant=reject_constant,
    ))


def make_validator():
    definition = load_json(DEFINITION)
    Draft202012Validator.check_schema(definition)
    return Draft202012Validator(definition, format_checker=FormatChecker())


def semantic_issues(document, file):
    """Check cross-field SCIM semantics after structural validation succeeds."""
    issues = []

    def check_scope(attributes, pointer, subattribute=False):
        seen = set()
        for index, attribute in enumerate(attributes):
            location = pointer + (index,)
            name = attribute["name"]
            folded = name.casefold()
            if folded in seen:
                issues.append(Issue(file, location + ("name",), "duplicate attribute name (case insensitive)"))
            seen.add(folded)
            if not ATTRIBUTE_NAME.fullmatch(name) and not (subattribute and folded == "$ref"):
                issues.append(Issue(file, location + ("name",), "invalid SCIM attribute name; $ref is a subattribute"))

            kind = attribute["type"]
            if kind in {"binary", "reference"} and not attribute["caseExact"]:
                issues.append(Issue(file, location + ("caseExact",), f"{kind} attributes must be case exact"))
            if kind in {"boolean", "decimal", "integer", "dateTime", "complex"} and attribute["caseExact"]:
                issues.append(Issue(file, location + ("caseExact",), f"{kind} attributes have no case sensitivity; use false"))
            if kind in {"binary", "boolean", "dateTime", "complex"} and attribute["uniqueness"] != "none":
                issues.append(Issue(file, location + ("uniqueness",), f"{kind} attributes have no uniqueness; use none"))
            if attribute["mutability"] == "writeOnly" and attribute["returned"] != "never":
                issues.append(Issue(file, location + ("returned",), "repository convention requires writeOnly attributes to be never returned"))
            if kind == "complex":
                check_scope(attribute["subAttributes"], location + ("subAttributes",), True)

    check_scope(document["attributes"], ("attributes",))
    # JSON Schema's ECMA-style $ anchor can also match before a final newline.
    if document["id"].endswith("\n"):
        issues.append(Issue(file, ("id",), "schema URI must not contain a newline"))
    return issues


def validate_files(paths, validator=None):
    validator = validator if validator is not None else make_validator()
    issues = []
    identifiers = {}
    for file in map(Path, paths):
        try:
            document = load_json(file)
        except InvalidJSON as error:
            issues.append(Issue(file, error.path, str(error)))
            continue
        except json.JSONDecodeError as error:
            issues.append(Issue(file, (), f"invalid JSON at line {error.lineno}, column {error.colno}"))
            continue
        except (OSError, UnicodeError) as error:
            issues.append(Issue(file, (), f"cannot read UTF-8 JSON: {error}"))
            continue

        errors = sorted(validator.iter_errors(document), key=lambda error: str(list(error.absolute_path)))
        for error in errors:
            # Use the failing rule, not the input value, to avoid exposing
            # accidentally supplied credentials in CI diagnostics.
            detail = f"invalid schema metadata ({error.validator})"
            if error.validator == "required":
                missing = [key for key in error.validator_value if key not in error.instance]
                detail += ": missing " + ", ".join(missing)
            issues.append(Issue(file, tuple(error.absolute_path), detail))
        if not errors:
            issues.extend(semantic_issues(document, file))
            identifier = document["id"]
            if identifier in identifiers:
                issues.append(Issue(file, ("id",), f"duplicate extension URI; also defined in {identifiers[identifier]}"))
            identifiers[identifier] = file
    return list(dict.fromkeys(issues))


def discover(root):
    paths = []
    issues = []
    extension_root = root / "extensions"
    if not extension_root.is_dir():
        issues.append(Issue(extension_root, (), "missing extensions directory"))
        return paths, issues
    for bundle in sorted(extension_root.iterdir()):
        if bundle.is_dir() and not bundle.name.startswith("."):
            if not SLUG.fullmatch(bundle.name):
                issues.append(Issue(bundle, (), "extension directory must use lowercase kebab-case"))
            paths.append(bundle / "scim-schema.json")
    return paths, issues


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="explicit Schema resource files")
    parser.add_argument("--root", type=Path, default=REPOSITORY, help="root for default bundle discovery")
    args = parser.parse_args(argv)
    validator = make_validator()
    if args.paths:
        paths = args.paths
        issues = validate_files(paths, validator)
        template_count = 0
    else:
        paths, issues = discover(args.root)
        issues.extend(validate_files(paths, validator))
        template = args.root / "templates" / "extension" / "scim-schema.json"
        # The illustrative template is not a real registration and does not
        # participate in extension URI uniqueness.
        issues.extend(validate_files([template], validator))
        template_count = 1
    for issue in issues:
        print(issue, file=sys.stderr)
    if issues:
        print(f"Validation failed with {len(issues)} error(s).", file=sys.stderr)
        return 1
    print(f"Validated {len(paths)} schema resource(s) and {template_count} template(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
