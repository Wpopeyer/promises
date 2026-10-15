"""promises check — lint a promises.yaml. See SPEC.md for what is checked."""

import argparse
import glob
import json
import os
import sys

import jsonschema
import yaml

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "promises.schema.json")


def key_literals(kind: str, row_id: str) -> list[str]:
    """The literal(s) a writer file must contain for this row to still be live."""
    # shortcut: the key is the last path segment of each id. Right for every row we have
    # declared so far; wrong for a route whose decorator splits the path across a blueprint
    # prefix. Upgrade to per-kind extractors when a real row needs it.
    out = []
    for part in row_id.split(", "):  # ", " separates ids; a bare "," belongs to a doc-id pattern
        if kind == "firestore.field":
            out.append(part.rsplit(".", 1)[-1])
        elif kind == "http.route":
            out.append(part.split()[-1].rstrip("/").rsplit("/", 1)[-1])
        else:
            out.append(part)
    return out


def check(path: str) -> list[str]:
    base = os.path.dirname(os.path.abspath(path))
    with open(path) as f:
        doc = yaml.safe_load(f)
    with open(SCHEMA_PATH) as f:
        schema = json.load(f)
    try:
        jsonschema.validate(doc, schema)
    except jsonschema.ValidationError as e:
        where = "/".join(str(p) for p in e.absolute_path) or "<root>"
        return [f"schema: {e.message} at {where}"]

    errors: list[str] = []
    seen: set[str] = set()
    for row in doc["promises"]:
        rid = row["id"]
        if rid in seen:
            errors.append(f"{rid}: duplicate id")
        seen.add(rid)
        if row.get("status") == "dead":
            continue
        files: list[str] = []
        for pattern in row.get("written_by", []):
            matched = [p for p in glob.glob(os.path.join(base, pattern), recursive=True) if os.path.isfile(p)]
            if not matched:
                errors.append(f"{rid}: written_by {pattern!r} matches no file")
            # Never read outside the workspace: a crafted yaml must not turn the lint into a file oracle.
            inside = [p for p in matched if os.path.realpath(p).startswith(os.path.realpath(base) + os.sep)]
            if len(inside) != len(matched):
                errors.append(f"{rid}: written_by {pattern!r} escapes the workspace")
            files.extend(inside)
        if not files:
            continue
        text = ""
        for fp in files:
            with open(fp, errors="ignore") as f:
                text += f.read()
        for literal in key_literals(row["kind"], rid):
            if literal not in text:
                errors.append(f"{rid}: {literal!r} not found in any written_by file")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="promises")
    sub = parser.add_subparsers(dest="cmd", required=True)
    chk = sub.add_parser("check", help="lint a promises.yaml")
    chk.add_argument("path", nargs="?", default="promises.yaml")
    args = parser.parse_args(argv)

    errors = check(args.path)
    for e in errors:
        print(e, file=sys.stderr)
    n = len(errors)
    print(f"{'FAIL' if errors else 'OK'}: {args.path} ({n} problem{'' if n == 1 else 's'})")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
