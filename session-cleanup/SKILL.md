---
name: session-cleanup
description: Review or prune stale Codex session JSONL files under ~/.codex/sessions while keeping live Desktop sessions and any user-named chats safe. Use when the user wants a preview-first cleanup flow, a keep/delete report, or deletion only after explicit confirmation.
---

# Session Cleanup

Safely inspect or delete stale Codex Desktop session files under `~/.codex/sessions`.

## Core Rules

- Preview first. Delete only after explicit user confirmation.
- Never delete live Codex Desktop sessions.
- Protect additional sessions the user names as `project | chat title`.
- Reject targets outside `~/.codex/sessions`.
- Do not create helper scripts for cleanup.
- If matching is ambiguous, stop without deleting.

## Inputs

Optional:

- target path: `~/.codex/sessions`, `~/.codex/sessions/YYYY`, `YYYY/MM`, or `YYYY/MM/DD`
- keep specs, one per line: `project | chat title`

`project` can be an absolute cwd, final path segment, or cwd suffix. `chat title` must match the visible Codex Desktop thread title exactly.

## Workflow

1. Canonicalize `~/.codex/sessions` and the requested target. Reject anything outside the sessions root.
2. Find the live Codex Desktop root process on macOS by matching `/Applications/Codex.app/Contents/MacOS/Codex`.
3. Expand the Desktop process tree and use `lsof` to collect open `rollout-*.jsonl` and `rollout-*.jsonl.sb-*` files.
4. Normalize sidecars by mapping `rollout-*.jsonl.sb-*` to the base `rollout-*.jsonl`.
5. Resolve user keep specs by scanning candidate JSONL files for:
   - `session_meta.payload.cwd`
   - latest `thread_name_updated.payload.thread_name`
6. Each keep spec must resolve to exactly one base JSONL file.
7. Build protected bases from live sessions plus keep-spec matches.
8. Preview:
   - target
   - protected live count
   - protected explicit keep count
   - candidate file count
   - delete candidate count
   - exact delete paths or a compact path list if large
   - estimated reclaimable size
9. Stop and ask for confirmation unless the user has already confirmed deletion after seeing the preview.
10. Before deleting, rerun the same resolution. Delete only unprotected candidates, then prune empty directories under the target.

## Implementation Notes

Use shell commands with temporary files. Prefer `rg`, `find`, `lsof`, `ps`, `awk`, `sort`, and `mktemp`.

Live protection:

```bash
ps -axo pid=,command= | awk '$2=="/Applications/Codex.app/Contents/MacOS/Codex"{print $1}'
```

Then walk descendants with `ps -axo pid=,ppid=`, run `lsof -p <pid-list>`, and keep paths matching:

```text
~/.codex/sessions/**/rollout-*.jsonl
~/.codex/sessions/**/rollout-*.jsonl.sb-*
```

Normalize sidecars:

```bash
sed 's#\.jsonl\.sb-.*$#.jsonl#'
```

Keep-spec matching:

- read the first `session_meta` cwd
- read the latest `thread_name_updated` title
- match cwd by exact path, final segment, or suffix
- require exact title match

## Confirmation

Delete only when the user clearly confirms after preview, such as:

- `이대로 삭제해`
- `preview 맞으면 진행`
- `delete them now`

If the user only asks to inspect, preview, compare, or report, do not delete.

## Failure Handling

Stop without deleting when:

- target cannot be canonicalized
- target is outside `~/.codex/sessions`
- no live Codex Desktop root process is found
- live sessions cannot be detected
- a keep spec is malformed
- a keep spec matches zero or multiple sessions
- any delete candidate is also in the protected base set

## Output

Report compactly:

- target path
- protected live base count
- protected explicit keep count
- candidate file count
- delete candidate count
- deleted file count, if deletion ran
- failed delete count, if deletion ran
- reclaimed size estimate or actual reclaimed size
- resolved keep specs, if provided
