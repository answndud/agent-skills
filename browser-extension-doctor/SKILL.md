---
name: browser-extension-doctor
description: Run a browser extension quality and safety diagnosis after extension feature work, bug fixes, refactors, or before commit/PR/store submission. Use for Chrome/Firefox extension manifests, Manifest V3, permissions, host_permissions, content scripts, background service workers, messaging, storage, CSP, web_accessible_resources, externally_connectable, secrets, remote-code policy, DOM scraping fragility, browser compatibility, or extension store review risk. Default to Korean output for Korean users.
---

# Browser Extension Doctor

Run a focused post-change diagnosis for browser extensions. Treat this as a second-pass reviewer after implementation, not as generic extension advice.

Default to Korean output for Korean users. Keep manifest keys, APIs, commands, paths, permissions, and browser names in English when clearer.

## Core Rule

Do not declare extension work complete immediately after edits. Inspect the diff, classify the changed surface, run proportionate verification, fix blocking issues when allowed, and report residual risk.

## Scope

Use for changes touching:

- `manifest.json`, Manifest V2/V3 migration, permissions, `host_permissions`, `optional_permissions`
- content scripts, injected scripts, DOM scraping, selectors, page-context bridges
- background pages or MV3 service workers
- extension messaging, ports, alarms, context menus, commands, side panel, popup/options UI
- `chrome.storage`, `browser.storage`, IndexedDB, cache, sync/local storage behavior
- CSP, remote code, dynamic script injection, eval-like behavior
- `web_accessible_resources`, `externally_connectable`, declarativeNetRequest, proxy/webRequest
- secrets, API keys, tokens, Bearer headers, OAuth/client secrets
- Chrome Web Store / Firefox Add-ons policy or compatibility risk

Skip for unrelated website-only changes, pure README wording, or assets not referenced by the extension.

## Workflow

1. Detect extension shape: manifest version, target browsers, build step, package scripts, tests, lint/typecheck.
2. Inspect `git status --short`, relevant diff/stat, and changed files.
3. Classify surface: `manifest`, `permissions`, `content-script`, `background`, `messaging`, `storage`, `ui`, `network`, `security`, `compat`, `store-policy`, `docs`.
4. Read nearby safety context, not only the diff. For example, content-script changes often require manifest, messaging handlers, injected script boundaries, and tests.
5. Pick the smallest meaningful verification command or manual check.
6. Run feasible local checks. If skipped, record `not run` with the reason.
7. Apply the checklist below to changed surfaces.
8. Fix P0/P1 issues unless the user requested report-only mode.
9. Rerun relevant verification after fixes and report verdict, commands, issues, fixes, and remaining risks.

## Verification

Prefer project-defined commands first:

- `npm test`, `pnpm test`, `yarn test`
- `npm run lint`, `npm run typecheck`, `npm run build`
- extension packaging command if present
- browser smoke test when practical: load unpacked extension, exercise changed flow, inspect service worker/content-script console

Do not treat unrun checks as passed.

Do not call production APIs, mutate real accounts, publish to a store, rotate credentials, or use paid external services unless explicitly requested.

## Checklist

Use only checks relevant to the changed surface.

### Manifest And Permissions

- Manifest version and browser targets are intentional.
- Permissions are minimal and justified.
- `host_permissions` are as narrow as practical.
- `optional_permissions` are used when access can be requested at runtime.
- `content_scripts.matches` and `exclude_matches` avoid overbroad injection.
- `web_accessible_resources` exposes only needed files and matches.
- `externally_connectable` is absent or tightly scoped.
- `background.service_worker` is MV3-compatible and does not assume persistent state.

### Content Scripts And Page Context

- Content scripts do not rely on secrets, environment variables, or privileged data.
- DOM selectors and page parsing fail gracefully when the target site changes.
- Injected page scripts have a narrow, validated message bridge.
- Message payloads are validated and do not trust page-controlled input blindly.
- Extension APIs are not exposed to the page context.
- UI injection avoids breaking host-page layout and cleans up event listeners/timers.

### Messaging, Storage, And State

- `runtime.sendMessage`, `tabs.sendMessage`, ports, and listeners handle async responses correctly.
- Sender/origin/tab validation is present where trust matters.
- Service worker lifecycle, alarms, retries, and idempotency are considered.
- Storage schema changes are backward compatible or migrated.
- Sensitive data is not stored unnecessarily, especially in `sync` storage.

### Security And Store Policy

- No API-key-shaped strings, tokens, Bearer values, passwords, private keys, or client secrets are committed.
- No remote hosted code, dynamic code execution, `eval`, unsafe inline script, or policy-violating CDN execution unless clearly allowed and justified.
- CSP is not loosened unnecessarily.
- Network requests have clear purpose and user-visible permission rationale.
- OAuth/client flows do not embed confidential secrets in extension code.
- Logging avoids secrets, private page content, and personal data.

### Compatibility And UX

- Chrome/Firefox API differences are handled when multi-browser support is claimed.
- MV3 service worker limitations are handled: no persistent globals, resilient startup, no long-running assumptions.
- Popup/options/side panel UI handles loading, failure, empty state, and permission denial.
- User-facing errors are clear and non-leaky.
- Extension behavior degrades gracefully when target pages, APIs, or permissions are unavailable.

## Severity

- `P0`: secret leak, overbroad dangerous permission, store-policy blocker, auth/privacy leak, extension unusable, build/load failure.
- `P1`: broken core flow, unsafe message bridge, missing sender/origin validation, MV3 lifecycle bug, host permission significantly broader than needed, storage migration/data-loss risk.
- `P2`: fragile selector without graceful fallback, weak error state, missing test/smoke coverage, minor permission/docs drift, compatibility risk.
- `P3`: naming, cleanup, small UX polish, non-blocking maintainability.

P0/P1 block completion unless the user asked for report-only mode.

## Fix Policy

- Prefer narrow, evidence-backed fixes.
- Reduce permissions instead of documenting overbroad access when feasible.
- Remove committed secrets or credential-like values; do not replace them with another hardcoded key.
- For P2/P3, fix only when localized and low risk; otherwise report follow-up.
- Rerun relevant verification after fixes or state why it was not rerun.

## Final Report

Use this compact Korean shape:

```text
browser extension doctor

변경 영역: <manifest/permissions/content-script/background/messaging/storage/ui/network/security/compat/store-policy/docs>
판정: <통과 | 차단 | 위험 동반 통과>

실행한 명령:
- <command>: <passed/failed/not run> <짧은 이유>

발견한 이슈:
- [P0/P1/P2/P3] <issue> | 근거: <file/command> | 조치: <fixed/follow-up>

적용한 수정:
- <없음 또는 목록>

남은 리스크:
- <없음 또는 목록>
```
