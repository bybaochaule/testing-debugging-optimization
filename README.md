# Testing, Debugging & Optimization

## Overview

This skill helps an agent test edge cases, debug behavior, measure accuracy and latency, and continuously improve agent, prompt, workflow, or tool-using systems. It turns evaluation work into a repeatable loop: scope, scenario design, scoring, baseline measurement, failure analysis, targeted fixes, regression testing, and iteration tracking.

## When to use

Use this skill when a user asks to test an agent, evaluate real scenarios, debug failures, compare versions, track accuracy, track latency, create regression tests, or optimize behavior over time.

Do not use it for unrelated software QA, unauthorized telemetry collection, hidden instruction extraction, destructive testing, or live production monitoring without confirmed authorization.

## Contents

- `SKILL.md`: agent-facing instructions, triggers, boundaries, workflow, output formats, quality checks, and safety rules.
- `README.md`: human-readable package overview.
- `agents/openai.yaml`: OpenAI metadata and invocation policy.
- `assets/test-matrix-template.csv`: reusable scenario matrix starter.
- `assets/optimization-log-template.md`: reusable iteration log template.
- `assets/run-results-example.jsonl`: sample structured run data for the helper script.
- `references/style-guide.md`: report style, metric definitions, failure taxonomy, and optimization rules.
- `references/evaluation-scenarios.md`: scenario categories and realistic examples to adapt.
- `scripts/example_helper.py`: deterministic local helper for summarizing pass rate and latency from JSONL or CSV results.

## Basic workflow

1. Define the behavior to evaluate and the deployment risk.
2. Build a scenario matrix with real examples first, then synthetic edge cases where needed.
3. Define scoring rules before reviewing outputs.
4. Measure baseline accuracy and latency.
5. Classify failures and identify likely root causes.
6. Apply targeted fixes.
7. Re-run the same tests against the candidate version.
8. Track deltas, regressions, and remaining risks.

## Helper script input schema

`scripts/example_helper.py` accepts JSONL or CSV records with these fields:

| Field | Required | Example | Notes |
|---|---|---|---|
| `scenario_id` | Yes | `S-001` | Unique scenario identifier. |
| `passed` | Yes | `true` | Accepts true/false, yes/no, pass/fail, or 1/0. |
| `latency_ms` | Recommended | `1240` | Milliseconds for the full agent response. |
| `error_type` | No | `tool_selection` | Use `none` or blank when passed. |
| `severity` | No | `high` | Suggested values: low, medium, high, critical. |
| `notes` | No | `Wrong tool used` | Short reviewer note. |

Example:

```bash
python scripts/example_helper.py assets/run-results-example.jsonl --format markdown
```

## Package structure

```text
testing-debugging-optimization/
|-- SKILL.md
|-- README.md
|-- agents/
|   `-- openai.yaml
|-- assets/
|   |-- .gitkeep
|   |-- optimization-log-template.md
|   |-- run-results-example.jsonl
|   `-- test-matrix-template.csv
|-- references/
|   |-- evaluation-scenarios.md
|   `-- style-guide.md
`-- scripts/
    `-- example_helper.py
```
