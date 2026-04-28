---
name: session-cleanup
description: Review or prune stale Codex session JSONL files under ~/.codex/sessions while keeping live Desktop sessions and any user-named chats safe. Use when the user wants a preview-first cleanup flow, a keep/delete report, or deletion only after explicit confirmation.
---

# Session Cleanup

## Overview

This skill is for safe cleanup of old Codex Desktop session files.

- Default to preview first.
- Delete only after explicit user confirmation.
- Always protect sessions currently open by the live Codex Desktop app.
- Also protect any extra sessions the user names as `project | chat title` pairs.
- Do not create helper scripts for the cleanup.

## Inputs

Optional user input:

- target path under `~/.codex/sessions`
- explicit keep specs, one per line, in `project | chat title` format

Allowed targets:

- `~/.codex/sessions`
- `~/.codex/sessions/YYYY`
- `~/.codex/sessions/YYYY/MM`
- `~/.codex/sessions/YYYY/MM/DD`

Accepted `project` values:

- absolute cwd path
- last path segment such as `game_maker`
- cwd suffix such as `kindergarten_ERP/erp`

`chat title` must match the visible Codex Desktop thread title exactly, including spaces.

Example keep specs:

```text
game_maker | 게임 제작
altteulmap | 기능 개발
kindergarten_ERP/erp | 배포
townpet | 배포
```

## Workflow

1. Canonicalize the sessions root and target, and reject anything outside `~/.codex/sessions`.
2. Find the live Codex Desktop root process on macOS using only `/Applications/Codex.app/Contents/MacOS/Codex`.
3. Expand the Desktop process tree and collect live-open `rollout-*.jsonl` and `rollout-*.jsonl.sb-*` paths with `lsof`.
4. Normalize live sidecars to their base `.jsonl` so the whole live session stays protected.
5. If the user gave explicit keep specs, resolve each spec to exactly one base session file by matching:
   - `session_meta.payload.cwd`
   - the last `thread_name_updated.payload.thread_name`
6. Build the protected base set as:
   - live-open base sessions
   - explicit keep matches
7. Build a preview report before deleting anything:
   - protected live session bases
   - protected explicit keep bases
   - total candidates
   - exact keep matches
   - exact delete candidates
8. If the user has not explicitly confirmed deletion after seeing scope, stop at the preview and ask for confirmation.
9. If the user explicitly confirms deletion, rerun the same resolution and then delete only the unprotected candidates.
10. Prune empty directories under the target and report reclaimed space.

## Matching Rules

For explicit keep specs:

- If a spec is malformed, stop.
- If a spec matches zero sessions, stop.
- If a spec matches multiple sessions, stop.
- Do not guess between multiple matches.

For live protection:

- Keep the base `rollout-*.jsonl`.
- Keep any `.sb-*` sidecars whose normalized base is protected.

## Preview Commands

Use shell variables like this:

```bash
sessions_root="$(cd "$HOME/.codex/sessions" && pwd -P)"
target="${target:-$sessions_root}"
target_abs="$(cd "$target" && pwd -P)" || exit 1
keep_specs="${keep_specs:-}"
```

Collect live-open sessions from the Desktop process tree:

```bash
root_pids="$(
  ps -axo pid=,command= \
    | awk '$2=="/Applications/Codex.app/Contents/MacOS/Codex"{print $1}' \
    | tr '\n' ' '
)"
```

```bash
descendants="$(
  ps -axo pid=,ppid= \
    | awk -v roots="$root_pids" '
        BEGIN {
          n=split(roots,a,/ /)
          for (i=1; i<=n; i++) if (a[i] != "") keep[a[i]]=1
        }
        {
          pid=$1
          ppid=$2
          parent[pid]=ppid
        }
        END {
          changed=1
          while (changed) {
            changed=0
            for (pid in parent) {
              if ((parent[pid] in keep) && !(pid in keep)) {
                keep[pid]=1
                changed=1
              }
            }
          }
          for (pid in keep) print pid
        }
      ' \
    | sort -n \
    | paste -sd, -
)"
```

```bash
live_exact="$(mktemp)"
live_base="$(mktemp)"
explicit_specs="$(mktemp)"
explicit_matches="$(mktemp)"
explicit_base="$(mktemp)"
protected_base="$(mktemp)"
candidates="$(mktemp)"
to_delete="$(mktemp)"
failed="$(mktemp)"
trap 'rm -f "$live_exact" "$live_base" "$explicit_specs" "$explicit_matches" "$explicit_base" "$protected_base" "$candidates" "$to_delete" "$failed"' EXIT

lsof -p "$descendants" 2>/dev/null \
  | awk '{print $NF}' \
  | awk -v root="$sessions_root" '
      index($0, root "/") == 1 && $0 ~ /rollout-.*\.jsonl(\.sb-.*)?$/ { print }
    ' \
  | sort -u > "$live_exact"

sed 's#\.jsonl\.sb-.*$#.jsonl#' "$live_exact" | sort -u > "$live_base"
```

Resolve explicit keep specs:

```bash
printf '%s\n' "$keep_specs" \
  | sed '/^[[:space:]]*$/d' \
  > "$explicit_specs"

: > "$explicit_matches"
: > "$explicit_base"

if [ -s "$explicit_specs" ]; then
  while IFS= read -r spec; do
    project="$(printf '%s\n' "$spec" | awk -F'|' '{print $1}' | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')"
    title="$(printf '%s\n' "$spec" | awk -F'|' '{ $1=""; sub(/^\|/, ""); print }' | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')"

    [ -n "$project" ] && [ -n "$title" ] || exit 1

    matches="$(
      find "$target_abs" -type f -name 'rollout-*.jsonl' | sort -u \
        | while IFS= read -r f; do
            cwd="$(
              rg -m1 '"type":"session_meta"' "$f" \
                | sed -n 's/.*"cwd":"\([^"]*\)".*/\1/p'
            )"
            [ -n "$cwd" ] || continue

            current_title="$(
              rg 'thread_name_updated' "$f" \
                | tail -n1 \
                | sed -n 's/.*"thread_name":"\([^"]*\)".*/\1/p'
            )"
            [ -n "$current_title" ] || continue

            case "$cwd" in
              "$project"|*/"$project") cwd_match=1 ;;
              *) cwd_match=0 ;;
            esac

            if [ "$cwd_match" -eq 1 ] && [ "$current_title" = "$title" ]; then
              printf '%s\n' "$f"
            fi
          done
    )"

    match_count="$(printf '%s\n' "$matches" | sed '/^$/d' | wc -l | tr -d ' ')"
    [ "$match_count" -eq 1 ] || exit 1

    printf '%s\n' "$spec -> $matches" >> "$explicit_matches"
    printf '%s\n' "$matches" >> "$explicit_base"
  done < "$explicit_specs"
fi
```

Build the final protected set and preview delete candidates:

```bash
cat "$live_base" "$explicit_base" | sed '/^$/d' | sort -u > "$protected_base"

find "$target_abs" -type f \( -name 'rollout-*.jsonl' -o -name 'rollout-*.jsonl.sb-*' \) \
  | sort -u > "$candidates"

while IFS= read -r f; do
  base="$(printf '%s\n' "$f" | sed 's#\.jsonl\.sb-.*$#.jsonl#')"
  if rg -Fxq -- "$base" "$protected_base"; then
    continue
  fi
  printf '%s\n' "$f" >> "$to_delete"
done < "$candidates"
```

## Confirmation Rule

Delete only if the user clearly confirms after the preview, for example:

- `이대로 삭제해`
- `preview 맞으면 진행`
- `delete them now`

If the user only asked to inspect, preview, or compare, do not delete.

## Delete Step

After explicit confirmation, rerun the preview logic first. Then delete:

```bash
deleted_count=0

while IFS= read -r f; do
  [ -n "$f" ] || continue
  if rm -f -- "$f"; then
    deleted_count=$((deleted_count + 1))
  else
    printf '%s\n' "$f" >> "$failed"
  fi
done < "$to_delete"

find "$target_abs" -depth -type d -empty ! -path "$target_abs" -delete
```

## Output

Report compactly:

- target path
- Desktop root PID(s)
- protected live session base count
- protected explicit keep base count
- protected total base count
- candidate file count
- delete candidate count
- deleted file count
- failed delete count
- before size
- after size
- reclaimed size

If explicit keep specs were used, also list the resolved matches.
If there are failures, also list the failed paths.

## Failure Handling

Stop without deleting anything when:

- the target cannot be canonicalized
- the target is outside `~/.codex/sessions`
- no live Codex Desktop root process is found
- the Desktop descendant PID set cannot be built
- no live session files are open by Codex Desktop
- an explicit keep spec is malformed
- an explicit keep spec does not resolve uniquely

## Notes

- This skill is intentionally safer than immediate-delete cleanup flows.
- Use this skill when the user values a keep/delete report or wants explicit guardrails.
- If the user specifically wants an immediate destructive cleanup and understands the scope, the older destructive skill may still be more direct.
