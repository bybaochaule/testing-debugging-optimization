---
name: testing-debugging-optimization
description: Use this skill to test, debug, benchmark, and optimize agent behavior using real scenarios, edge cases, accuracy checks, latency measurements, issue fixes, and iteration logs. Trigger when the user asks to test an agent, debug failures, evaluate edge cases, measure accuracy or latency, compare versions, optimize behavior, or create an agent evaluation plan. Do not use it for live production monitoring, unauthorized telemetry collection, security exploitation, or unrelated software QA.
---

# Testing, Debugging & Optimization

## Purpose

Help an agent test, debug, measure, and improve another agent, prompt, workflow, or tool-using behavior through a repeatable evaluation loop. The skill emphasizes real scenarios, edge cases, accuracy tracking, latency tracking, regression checks, and clear iteration records.

Use this skill to move from subjective impressions such as "it seems better" to evidence-backed findings such as "version B improved pass rate from 72% to 86% on the same 50 scenarios, while p95 latency increased by 8%."

## When to use

Use this skill when the user asks to:

- Test an agent, prompt, workflow, or automation against realistic scenarios.
- Build edge-case, regression, or adversarial test suites.
- Debug failures such as hallucinations, missed constraints, tool misuse, formatting breaks, refusals, loops, or brittle routing.
- Measure accuracy, pass rate, rubric score, latency, stability, or cost-adjacent proxy metrics.
- Compare baseline and candidate versions using the same scenarios and scoring criteria.
- Produce a test plan, evaluation matrix, debug report, optimization plan, or iteration log.
- Decide what to fix next based on severity, frequency, and user impact.

## Do not use

Do not use this skill when:

- The task is unrelated to agent, prompt, workflow, or automation behavior.
- The user wants live production monitoring, incident response, or telemetry access that has not been explicitly authorized.
- The user asks to collect secrets, private records, credentials, or unnecessary sensitive data.
- The user asks for hidden instruction extraction, bypassing safety controls, exploit development, or destructive testing.
- The available evidence is too thin to support a performance claim; in that case, state what is missing and provide a test plan instead.
- A high-stakes domain evaluation would be used as the sole approval gate without expert human review.

## Required inputs

Use information already provided by the user before asking for more. The most useful inputs are:

- Target behavior: what the agent should do and for whom.
- Scope: channels, tools, files, workflows, integrations, or task types to evaluate.
- Scenarios: real user requests, transcripts, logs, support tickets, examples, or a representative task list.
- Expected behavior: gold answers, acceptance criteria, rubric, or human-review rules.
- Baseline and candidate versions: prompt text, configuration, model settings, routing rules, or code changes.
- Metrics: accuracy, pass rate, rubric score, latency, stability, format compliance, tool-call success, or other constraints.
- Run evidence: outputs, tool logs, timestamps, latency measurements, screenshots, or structured result files.
- Constraints: privacy requirements, safety requirements, budget, latency limits, and deployment risk level.

When essential inputs are missing and the user still needs progress, generate a clearly labeled draft scenario suite and mark it as synthetic until real examples are supplied.

## Workflow

1. **Scope the evaluation.** Identify the target agent behavior, users, supported task types, non-goals, and risk level.
2. **Create a scenario matrix.** Include happy paths, edge cases, ambiguous requests, missing inputs, conflicting instructions, tool errors, stale data, privacy-sensitive requests, formatting constraints, multi-turn corrections, and long-context cases.
3. **Define scoring before testing.** Select pass/fail checks, rubric dimensions, required citations or evidence, allowed assumptions, latency thresholds, and failure severity levels.
4. **Run or review the baseline.** Use user-provided outputs and logs when available. Do not invent test results; label unexecuted cases as planned.
5. **Measure accuracy and latency.** Track sample count, pass rate, failure categories, p50 latency, p95 latency, maximum latency, and any missing measurements.
6. **Debug failures.** For each failure, separate observed symptom from likely root cause. Classify causes such as unclear instructions, missing context, retrieval failure, tool-selection error, parameter error, safety mismatch, state leak, output-format drift, or timeout.
7. **Prioritize fixes.** Rank issues by severity, frequency, user impact, and implementation effort. Fix high-impact recurring failures before isolated cosmetic issues.
8. **Apply targeted optimizations.** Improve instructions, add examples, tighten tool-routing rules, add validation checks, simplify prompts, reduce unnecessary tool calls, add fallback behavior, or improve output schemas.
9. **Regression test the candidate.** Re-run the same scenarios used for the baseline, then add new tests for each fixed bug.
10. **Compare versions.** Report metric deltas, qualitative improvements, regressions, latency tradeoffs, and confidence limits.
11. **Document the iteration.** Record what changed, why it changed, what evidence supports it, and what remains risky.
12. **Recommend the next loop.** Suggest the smallest next set of tests or fixes that would most improve reliability.

## Output format

Choose the output that matches the user's request.

### Test plan

```markdown
# Agent Test Plan

## Scope
## Success criteria
## Scenario matrix
## Metrics and thresholds
## Test procedure
## Evidence to collect
## Review and signoff
```

### Debug report

```markdown
# Agent Debug Report

## Issue summary
## Reproduction steps or scenario IDs
## Observed behavior
## Expected behavior
## Suspected root cause
## Fix recommendation
## Regression tests
## Remaining risks
```

### Optimization report

```markdown
# Agent Optimization Report

## Baseline
## Candidate change
## Scenario coverage
## Accuracy results
## Latency results
## Failure taxonomy
## Improvements
## Regressions or tradeoffs
## Next iteration
```

### Metrics table

Use this compact table when reporting measured results:

| Version | Scenarios | Pass rate | Failed | p50 latency | p95 latency | Max latency | Notes |
|---|---:|---:|---:|---:|---:|---:|---|

## Quality checklist

Before finalizing:

- The test scope, scenario count, and evidence source are clear.
- Real user scenarios are used when available; synthetic scenarios are labeled as synthetic.
- The same scoring rules are used for baseline and candidate comparisons.
- Accuracy claims include sample count and scoring method.
- Latency claims include units, sample count, and percentile method or caveat.
- Observed facts are separated from hypotheses and recommendations.
- Each proposed fix maps to at least one failing or high-risk scenario.
- Regression tests cover previously fixed failures.
- Remaining risks and missing data are explicitly stated.
- No private data, secrets, or unnecessary sensitive details are exposed.

## Safety and privacy

- Redact secrets, credentials, private records, and unrelated personal data from logs and scenarios.
- Do not request or store sensitive data unless it is essential and authorized.
- Do not use production telemetry, private repositories, or customer data unless the user confirms access rights and scope.
- Do not run destructive commands, stress tests, exploit attempts, or automated actions against live systems.
- Preserve higher-priority safety instructions while optimizing behavior.
- For medical, legal, financial, hiring, education, or other high-stakes use cases, recommend expert human review and conservative deployment gates.
