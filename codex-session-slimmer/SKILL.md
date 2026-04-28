---
name: codex-session-slimmer
description: Slim old Codex session JSONL files under ~/.codex/sessions when the user wants month-level or day-level cleanup without deleting whole sessions or creating separate archives. Use when the user asks Codex to inspect a selected YYYY/MM or YYYY/MM/DD folder, identify what makes each rollout-*.jsonl file large, and directly edit each file in place while preserving valid JSONL that Codex App or CLI can still parse.
---

# Codex Session Slimmer

## Overview

This skill is instruction-only. Do not create helper scripts for the cleanup itself. Inspect the chosen month or day, determine what makes each session file large, and edit files directly only when the expected savings are meaningful.

## Workflow

1. Confirm the target directory under `~/.codex/sessions`, usually `YYYY/MM` or `YYYY/MM/DD`.
2. Inspect the target before changing anything:

```bash
du -sh TARGET
find TARGET -type f -name 'rollout-*.jsonl' -exec du -h {} + | sort -hr | head -30
```

3. For each large file, inspect the first line and the size drivers.
4. Choose the smallest safe set of edits for that file.
5. Rewrite the file in place using a temp file plus atomic replace.
6. Re-validate the rewritten file by parsing every line as JSON.
7. Report before and after sizes for the directory and for the files changed.

## Per-file analysis

For each large `rollout-*.jsonl`, inspect:

```bash
f="ABSOLUTE_PATH_TO_FILE"
sed -n '1p' "$f" | jq '{kind:(if .payload.forked_from_id then "forked" else "main" end), role:(.payload.agent_role // "main"), cwd:.payload.cwd}'
```

Then inspect what dominates the file:

```bash
jq -r '.type' "$f" | sort | uniq -c | sort -nr
jq -r 'select(.type=="event_msg") | .payload.type // empty' "$f" | sort | uniq -c | sort -nr
jq -r 'select(.type=="response_item") | .payload.type // empty' "$f" | sort | uniq -c | sort -nr
```

When needed, estimate the heavy fields:

- `event_msg.payload.type=="token_count"`
- `response_item.payload.type=="reasoning"` with `payload.encrypted_content`
- `compacted.payload.replacement_history`
- `response_item.payload.type=="function_call_output"` or `custom_tool_call_output` with long `payload.output`

## Edit rules

Preserve these invariants:

- Keep valid JSONL.
- Keep one JSON object per line.
- Preserve line order.
- Preserve top-level `timestamp`, `type`, and `payload` keys.
- Preserve `session_meta`, `turn_context`, `message`, `user_message`, and `function_call` records.
- Prefer preserving key names and value types where possible.

Apply edits conservatively and per file:

1. `token_count` records:
   Keep the record but set `payload.info = null` and `payload.rate_limits = null`.

2. `reasoning` records:
   Keep the record but blank `payload.encrypted_content` to `""`.

3. `compacted` records:
   Keep the record but replace `payload.replacement_history` with `[]`.
   This is usually the largest win in old main sessions.

4. `function_call_output` and `custom_tool_call_output`:
   Only trim when the file is still too large after the safer edits or when these outputs are clearly dominant.
   Preserve the field as a string and keep head and tail with a marker in the middle.

5. Do not delete whole lines unless they are obviously disposable and low risk. Prefer mutating fields over removing records.

## Safety threshold

Use this default order:

1. `token_count`
2. `reasoning.encrypted_content`
3. `compacted.replacement_history`
4. Large tool outputs

For older `forked` sessions, more aggressive trimming is acceptable.
For older `main` sessions, stop after step 3 unless tool outputs are clearly the remaining cause.

Avoid touching the current active month unless the user explicitly asks.

## Rewrite pattern

When editing a file, use a temp file in the same directory and replace the original only after the rewrite succeeds. After rewriting, verify:

```bash
jq -c . "$f" >/dev/null
du -h "$f"
```

If a rewrite would save little space, skip it and report that the file is not worth touching.

## What to report

After the run, report:

- target directory
- files inspected
- files changed
- major causes found per large file
- before and after sizes
- any files intentionally skipped because the risk was higher than the expected savings
