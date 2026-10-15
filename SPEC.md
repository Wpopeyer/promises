# promises.yaml — specification (v1)

A `promises.yaml` lives at the root of a workspace that contains several repositories. It declares, from the **producer's** side, every value that one repository writes and a different repository reads. Consumers are not enumerated; they are found by grepping, and the file exists so that whoever greps knows what the value is supposed to mean.

## File

```yaml
version: 1
promises:
  - <row>
  - <row>
```

Paths in the file are relative to the directory the file is in.

## Row

| Key | Required | Meaning |
|---|---|---|
| `kind` | yes | One of `firestore.field`, `pubsub.topic`, `http.route`, `env`. |
| `id` | yes | The thing being promised, in the form below. Unique across the file. Several ids may share a row, separated by `, `, when they are written together and mean the same. |
| `type` | no | Free text: the value type, enum, or payload shape. |
| `meaning` | yes | One or two sentences: what the value means to whoever reads it. Write it for the reader, not the writer. |
| `invariant` | yes | A rule the producer must keep, checkable by a reviewer reading the diff. When none can be stated: `UNKNOWN — <owner> to confirm`. |
| `written_by` | no | Globs of the files that write it (`**` allowed). Empty list when the value is written outside any repository (a console, a secret store); say where in `meaning`. |
| `consumed_by` | no | Repository names, optionally with a short hint. Never a file list. |
| `schema` | no | Path to a JSON Schema or a model file that pins the payload shape. Informational. |
| `status` | no | `live` (default), `deprecated`, `dead`. The lint skips writer checks for `dead` rows. |
| `note` | no | Free text. |

## `id` forms

| kind | form | examples |
|---|---|---|
| `firestore.field` | `collection/{doc-id pattern}.field` — nested fields with `.`, map keys with `{name}` | `sessions/{plate}.is_parked`, `drivers/{email}.devices.{device_id}.enabled` |
| `pubsub.topic` | topic name | `parking-session` |
| `http.route` | `METHOD path` or `METHOD full-url` | `GET /api/app/sessions`, `POST https://<region>-<project>.cloudfunctions.net/firestore_upsert` |
| `env` | variable name | `MODE` |

## Rules

1. **Producers declare, consumers grep.** The file does not list consumer files. The instructions file for your agents carries the sentence that makes them grep. Both together are the mechanism.
2. **`invariant` is a sentence, not a schema.** "true iff ended_at is null; never hard-code" is an invariant. A type is not.
3. **Unknown is a valid answer.** `UNKNOWN — <owner> to confirm` marks a row whose rule nobody has stated. Agents should raise it, not resolve it.
4. **One file at the workspace root.** Not one per repo. It is read by the person or agent who has every repo in view.

## The lint

`promises check [path]` fails when:

- the file does not match `promises.schema.json` (missing `meaning` or `invariant`, unknown `kind`, unknown key);
- two rows share an `id`;
- a `written_by` glob matches no file;
- a declared key no longer appears in any file matched by `written_by`. The key is the last path segment of the `id`: the field name, the topic name, the final route segment, the variable name.

The last check is deliberately crude. It catches a field being renamed or dropped from its writer; it does not catch its meaning changing. That is what `invariant` and the grep are for.

## Installation

Add one line to the file your agents read first:

> Cross-repo contracts and their invariants are declared in `promises.yaml`. Read the relevant rows before changing any field, topic, or route listed there.

Run `uvx --from promises-yaml promises check` in CI from the workspace root.
