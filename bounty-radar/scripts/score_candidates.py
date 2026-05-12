#!/usr/bin/env python3
"""Score bounty candidates from a JSON array and print a Markdown table."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


BASE_FIELDS = {
    "reward_clarity": 20,
    "freshness": 15,
    "low_crowding": 20,
    "scope_fit": 15,
    "verification": 15,
    "diversification": 10,
    "safety": 5,
}

PENALTIES = {
    "assignment_unassigned": 25,
    "crowded": 25,
    "unclear_reward": 20,
    "manual_blocker": 20,
    "legal_or_ai_risk": 30,
    "same_repo_recent": 15,
}


def clamp_int(value: Any, minimum: int, maximum: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = 0
    return max(minimum, min(maximum, parsed))


def score_candidate(candidate: dict[str, Any]) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []

    for field, maximum in BASE_FIELDS.items():
        value = clamp_int(candidate.get(field, 0), 0, maximum)
        score += value
        if value < maximum // 2:
            reasons.append(f"low {field.replace('_', ' ')}")

    for flag, penalty in PENALTIES.items():
        if candidate.get(flag):
            score -= penalty
            reasons.append(flag.replace("_", " "))

    return max(0, min(100, score)), reasons


def decision_for(score: int, candidate: dict[str, Any]) -> str:
    if candidate.get("legal_or_ai_risk") or candidate.get("crowded"):
        return "reject"
    if candidate.get("assignment_unassigned"):
        return "claim_first"
    if candidate.get("manual_blocker") or candidate.get("unclear_reward"):
        return "hold"
    if score >= 80:
        return "submit_now"
    if score >= 65:
        return "claim_first"
    if score >= 45:
        return "hold"
    return "reject"


def load_candidates(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit("Input must be a JSON array of candidate objects.")
    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise SystemExit(f"Candidate at index {index} is not an object.")
    return data


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: score_candidates.py candidates.json", file=sys.stderr)
        return 2

    candidates = load_candidates(Path(sys.argv[1]))
    rows = []
    for candidate in candidates:
        score, reasons = score_candidate(candidate)
        rows.append(
            {
                "name": str(candidate.get("name", "unknown")),
                "reward": str(candidate.get("reward", "")),
                "state": str(candidate.get("state", "")),
                "score": score,
                "decision": decision_for(score, candidate),
                "rationale": "; ".join(reasons) if reasons else "strong signals",
            }
        )

    rows.sort(key=lambda row: row["score"], reverse=True)

    print("| Candidate | Reward | State | Score | Decision | Rationale |")
    print("|---|---:|---|---:|---|---|")
    for row in rows:
        print(
            f"| {row['name']} | {row['reward']} | {row['state']} | "
            f"{row['score']} | {row['decision']} | {row['rationale']} |"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
