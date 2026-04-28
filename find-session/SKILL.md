---
name: find-session
description: "Find which `~/.codex/sessions` `rollout-*.jsonl` file corresponds to the current live Codex conversation. Use when the user asks which session file this conversation is using, wants the exact current JSONL path, or wants to verify the current thread id against the local `~/.codex/sessions` store. This skill is global and project-agnostic. It is read-only: inspect and report, but do not modify session files."
---

# Find Session

Use this skill to identify the exact `rollout-*.jsonl` file under `~/.codex/sessions` for the current active Codex conversation.

Prefer the live process environment first. The most reliable identifier is usually `CODEX_THREAD_ID`.

This skill is read-only:

- do not edit session files
- do not rename or move session files
- do not create helper scripts unless the user explicitly asks

## Inputs

Usually no extra input is required.

Optional user inputs that can help:

- an expected thread id
- a known date range
- a known working directory

## Workflow

1. Read the current process environment and look for a live thread id.

```bash
env | sort | rg '^CODEX_THREAD_ID='
```

2. If `CODEX_THREAD_ID` exists, search `~/.codex/sessions` for that id in filenames and file contents.

```bash
thread_id="$(env | awk -F= '/^CODEX_THREAD_ID=/{print $2}')"
rg -n -l "$thread_id" "$HOME/.codex/sessions"
```

3. If one file matches, validate it by checking the first `session_meta` line.

```bash
f="ABSOLUTE_PATH_TO_FILE"
sed -n '1p' "$f"
```

Confirm that:

- `payload.id` matches `CODEX_THREAD_ID`
- `payload.cwd` matches the current workspace if relevant

4. If `CODEX_THREAD_ID` is missing, fall back to recent-session inspection.

Use these signals together:

- recent file modification time
- `session_meta.payload.cwd`
- current working directory

```bash
find "$HOME/.codex/sessions" -type f -name 'rollout-*.jsonl' -print0 \
  | xargs -0 stat -f '%Sm %N' -t '%Y-%m-%d %H:%M:%S' \
  | sort -r | head -n 30
```

Then inspect candidate files:

```bash
sed -n '1p' "CANDIDATE_FILE"
```

5. If multiple files match, do not guess silently.

Instead:

- report every matching file
- explain why the match is ambiguous
- state what additional signal would disambiguate it

## Verification

Before finalizing, verify at least these:

1. The returned path is an absolute path under `~/.codex/sessions`.
2. The file is a `rollout-*.jsonl` file.
3. The file's `session_meta.payload.id` matches the live `CODEX_THREAD_ID` when that env var exists.
4. If a fallback path was used, say explicitly that the result is a best-effort inference rather than an exact thread-id match.

## Output

Report in a compact format:

- current thread id, if available
- exact session file path
- `session_meta.payload.cwd`
- whether the result is exact or fallback/inferred

Example:

```text
Current thread id: 019ce117-e857-7e33-af48-f3e62c4aefb4
Session file: /Users/alex/.codex/sessions/2026/03/12/rollout-2026-03-12T17-09-26-019ce117-e857-7e33-af48-f3e62c4aefb4.jsonl
Session cwd: /Users/alex/project/townpet
Confidence: exact match via CODEX_THREAD_ID
```

## Failure handling

If no match is found:

- say that no exact session file was found
- show the thread id used, if any
- summarize what was checked
- do not invent a path
