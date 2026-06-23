# Testing, Debugging & Optimization Style Guide

## Voice

- Be evidence-driven, practical, and specific.
- Separate observations from hypotheses.
- Prefer reproducible test steps over broad judgments.
- State uncertainty when the evidence is incomplete.

## Report rules

- Always name the evaluated version or configuration when it is known.
- Include scenario count for every accuracy claim.
- Include units for every latency claim.
- Use the same scoring criteria when comparing versions.
- Label unexecuted tests as planned, not measured.
- Label synthetic scenarios as synthetic.

## Metric definitions

- **Pass rate**: passed scenarios divided by total scored scenarios.
- **Accuracy**: task-specific correctness, measured by pass/fail checks, exact match, rubric score, or human review.
- **Latency**: elapsed time from user request to final agent response, unless another boundary is specified.
- **p50 latency**: median latency.
- **p95 latency**: latency at or below which approximately 95% of measured runs complete.
- **Regression**: a previously passing scenario that fails after a change.
- **Stability**: consistency across repeated runs of the same scenario.

## Failure taxonomy

Use these categories when triaging issues:

- `instruction_following`: ignored or misread explicit instructions.
- `missing_context`: needed information was absent or not requested.
- `ambiguity_handling`: failed to clarify or make safe assumptions.
- `hallucination`: invented unsupported facts, files, tool results, or capabilities.
- `retrieval_or_citation`: used weak sources, missed relevant context, or cited incorrectly.
- `tool_selection`: chose the wrong tool or failed to use a needed tool.
- `tool_parameters`: used incorrect tool arguments, paths, filters, or formats.
- `format_compliance`: output did not match the requested schema, file type, or style.
- `safety_or_privacy`: exposed sensitive data or mishandled a policy boundary.
- `state_management`: forgot prior context, leaked unrelated context, or mishandled multi-turn corrections.
- `latency`: response path was slower than threshold or used unnecessary steps.
- `robustness`: failed on edge cases, malformed input, empty data, or long context.

## Scenario design rules

A balanced scenario suite should include:

1. Common happy-path requests.
2. High-value real user requests.
3. Ambiguous or underspecified requests.
4. Conflicting constraints.
5. Missing files, empty inputs, or malformed data.
6. Tool failures or unavailable information.
7. Privacy-sensitive requests requiring redaction.
8. Freshness-sensitive requests requiring current verification.
9. Multi-turn corrections and interruptions.
10. Long-context or large-artifact requests.

## Optimization rules

- Fix root causes, not only the visible symptom.
- Avoid overfitting to a single scenario.
- Preserve safety and privacy behavior when improving helpfulness.
- Prefer small, testable changes over broad prompt rewrites.
- Add a regression test for every fixed bug.
- Track latency tradeoffs when adding validation or tool calls.

## Output terminology

Use these labels consistently:

- **Measured**: supported by executed tests or supplied run evidence.
- **Observed**: visible in the provided output, log, or transcript.
- **Likely cause**: reasoned diagnosis that has not been conclusively proven.
- **Recommendation**: proposed fix that still needs implementation or validation.
- **Remaining risk**: known gap after the current iteration.
