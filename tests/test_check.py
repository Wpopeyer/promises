import pathlib
import textwrap

from promises.cli import check, key_literals

ROOT = pathlib.Path(__file__).resolve().parent.parent


def test_example_passes():
    assert check(str(ROOT / "examples" / "promises.yaml")) == []


def test_key_literals():
    assert key_literals("firestore.field", "sessions/{plate}.is_parked") == ["is_parked"]
    assert key_literals("firestore.field", "a/{x}.p, a/{x}.q") == ["p", "q"]
    assert key_literals("http.route", "POST https://h/fn/firestore_upsert") == ["firestore_upsert"]
    assert key_literals("pubsub.topic", "parking-session") == ["parking-session"]
    assert key_literals("env", "MODE") == ["MODE"]


def test_missing_key_and_missing_file_fail(tmp_path):
    (tmp_path / "w.py").write_text("doc.set({'is_parked': True})\n")
    (tmp_path / "promises.yaml").write_text(textwrap.dedent("""
        version: 1
        promises:
          - kind: firestore.field
            id: sessions/{plate}.is_parked
            meaning: open session
            invariant: true iff ended_at is null
            written_by: [w.py]
          - kind: firestore.field
            id: sessions/{plate}.gone
            meaning: x
            invariant: y
            written_by: [w.py, nope/*.py]
    """))
    assert check(str(tmp_path / "promises.yaml")) == [
        "sessions/{plate}.gone: written_by 'nope/*.py' matches no file",
        "sessions/{plate}.gone: 'gone' not found in any written_by file",
    ]


def test_schema_rejects_missing_invariant(tmp_path):
    (tmp_path / "promises.yaml").write_text(textwrap.dedent("""
        version: 1
        promises:
          - kind: env
            id: MODE
            meaning: x
    """))
    errs = check(str(tmp_path / "promises.yaml"))
    assert len(errs) == 1 and errs[0].startswith("schema: 'invariant' is a required property")


def test_written_by_cannot_escape_workspace(tmp_path):
    (tmp_path / "outside.txt").write_text("not yours to read\n")
    ws = tmp_path / "ws"
    ws.mkdir()
    (ws / "promises.yaml").write_text(textwrap.dedent("""
        version: 1
        promises:
          - kind: env
            id: SOMEVAR
            meaning: x
            invariant: y
            written_by: ["../outside.txt"]
    """))
    assert check(str(ws / "promises.yaml")) == ["SOMEVAR: written_by '../outside.txt' escapes the workspace"]
