#!/usr/bin/env python3
"""Summarize agent evaluation run results.

The script is intentionally local and deterministic. It reads JSONL or CSV records
with scenario_id, passed, latency_ms, error_type, severity, and notes fields, then
prints a compact accuracy and latency summary.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

TRUE_VALUES = {"true", "t", "yes", "y", "1", "pass", "passed"}
FALSE_VALUES = {"false", "f", "no", "n", "0", "fail", "failed"}


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in TRUE_VALUES:
        return True
    if text in FALSE_VALUES:
        return False
    raise ValueError(f"Cannot parse boolean value: {value!r}")


def parse_latency_ms(value: Any) -> float | None:
    if value is None or str(value).strip() == "":
        return None
    latency = float(value)
    if latency < 0:
        raise ValueError(f"latency_ms cannot be negative: {latency}")
    return latency


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_number, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_number}: {exc}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"Line {line_number} must be a JSON object")
            records.append(value)
    return records


def load_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def load_records(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".jsonl":
        return load_jsonl(path)
    if suffix == ".csv":
        return load_csv(path)
    raise ValueError("Input must be a .jsonl or .csv file")


def percentile(values: list[float], pct: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    rank = math.ceil((pct / 100.0) * len(ordered)) - 1
    rank = max(0, min(rank, len(ordered) - 1))
    return ordered[rank]


def summarize(records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    total = 0
    passed = 0
    latencies: list[float] = []
    errors: Counter[str] = Counter()
    severity: Counter[str] = Counter()
    failures: list[dict[str, Any]] = []

    for index, record in enumerate(records, start=1):
        if "passed" not in record:
            raise ValueError(f"Record {index} is missing required field: passed")
        scenario_id = str(record.get("scenario_id") or f"record-{index}")
        did_pass = parse_bool(record["passed"])
        latency = parse_latency_ms(record.get("latency_ms"))
        error_type = str(record.get("error_type") or "none").strip() or "none"
        sev = str(record.get("severity") or "unspecified").strip() or "unspecified"

        total += 1
        passed += int(did_pass)
        if latency is not None:
            latencies.append(latency)
        if not did_pass:
            errors[error_type] += 1
            severity[sev] += 1
            failures.append({
                "scenario_id": scenario_id,
                "error_type": error_type,
                "severity": sev,
                "notes": str(record.get("notes") or "").strip(),
            })

    if total == 0:
        raise ValueError("No records found")

    failed = total - passed
    pass_rate = passed / total
    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": pass_rate,
        "latency_count": len(latencies),
        "p50_latency_ms": percentile(latencies, 50),
        "p95_latency_ms": percentile(latencies, 95),
        "max_latency_ms": max(latencies) if latencies else None,
        "error_counts": dict(errors),
        "severity_counts": dict(severity),
        "failures": failures,
    }


def fmt_ms(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.0f} ms"


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Agent Evaluation Summary",
        "",
        "## Metrics",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Scenarios | {summary['total']} |",
        f"| Passed | {summary['passed']} |",
        f"| Failed | {summary['failed']} |",
        f"| Pass rate | {summary['pass_rate']:.1%} |",
        f"| Latency samples | {summary['latency_count']} |",
        f"| p50 latency | {fmt_ms(summary['p50_latency_ms'])} |",
        f"| p95 latency | {fmt_ms(summary['p95_latency_ms'])} |",
        f"| Max latency | {fmt_ms(summary['max_latency_ms'])} |",
        "",
        "## Error counts",
        "",
    ]
    if summary["error_counts"]:
        lines.extend(["| Error type | Count |", "|---|---:|"])
        for key, value in sorted(summary["error_counts"].items()):
            lines.append(f"| {key} | {value} |")
    else:
        lines.append("No failed scenarios.")

    lines.extend(["", "## Failed scenarios", ""])
    if summary["failures"]:
        lines.extend(["| Scenario | Error type | Severity | Notes |", "|---|---|---|---|"])
        for failure in summary["failures"]:
            notes = str(failure["notes"]).replace("|", "\\|")
            lines.append(
                f"| {failure['scenario_id']} | {failure['error_type']} | {failure['severity']} | {notes} |"
            )
    else:
        lines.append("No failed scenarios.")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Summarize agent evaluation accuracy and latency results.")
    parser.add_argument("input", type=Path, help="Path to a .jsonl or .csv result file")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--out", type=Path, help="Optional output file")
    args = parser.parse_args(argv)

    try:
        summary = summarize(load_records(args.input))
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        output = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    else:
        output = render_markdown(summary)

    if args.out:
        args.out.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
