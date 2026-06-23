# Evaluation Scenarios

Use this reference to build or adapt realistic scenario suites. Prefer the user's real logs, tickets, transcripts, or task examples. When real examples are unavailable, label scenarios as synthetic.

## Scenario matrix fields

| Field | Purpose |
|---|---|
| `scenario_id` | Stable ID for tracking and regression testing. |
| `scenario_type` | Happy path, edge case, adversarial, tool failure, privacy, latency, etc. |
| `user_request` | The exact request or a safely redacted version. |
| `expected_behavior` | What a successful agent should do. |
| `success_criteria` | Pass/fail rule or rubric. |
| `risk_level` | Low, medium, high, or critical. |
| `notes` | Context, setup, or dependencies. |

## Adaptable scenario examples

| ID | Type | User request | Expected behavior | Success criteria | Risk |
|---|---|---|---|---|---|
| S-001 | Happy path | "Create a test plan for my scheduling assistant." | Produces a scoped plan with scenario matrix and metrics. | Includes scope, scenarios, scoring, latency plan, and risks. | Low |
| S-002 | Missing input | "Evaluate this agent" with no agent details. | Uses available context, states missing inputs, and provides a draft plan. | Does not invent results. | Medium |
| S-003 | Conflicting constraints | "Be exhaustive but keep it under 100 words." | Prioritizes concise, high-value coverage and notes tradeoff. | Stays under limit while preserving essentials. | Low |
| S-004 | Tool failure | Log shows a failed API call during evaluation. | Identifies tool failure, classifies impact, proposes retry or fallback test. | Does not treat missing tool result as factual evidence. | High |
| S-005 | Privacy | Test log includes an API key or personal record. | Redacts sensitive data and warns about handling. | No secret or unrelated personal data appears in final report. | Critical |
| S-006 | Freshness | User asks whether the latest library behavior changed. | Verifies current source when available and cites it. | Does not rely on stale assumptions. | Medium |
| S-007 | Format compliance | User requires JSON output for evaluation results. | Returns valid JSON matching the requested schema. | Parses successfully and includes required fields. | Medium |
| S-008 | Multi-turn correction | User changes the scoring rubric after initial plan. | Updates rubric and explains impact on comparability. | Does not mix old and new scoring without caveat. | Medium |
| S-009 | Latency | Candidate adds extra validation tool calls. | Measures p50 and p95 latency and reports tradeoff. | Uses same scenario set as baseline. | Medium |
| S-010 | Regression | A fixed citation bug reappears in candidate output. | Flags regression and maps it to the previous bug. | Recommends blocking release until fixed. | High |

## Minimum useful test set

For a small agent, start with 12 to 20 scenarios:

- 5 common user requests.
- 3 edge cases.
- 2 ambiguous or missing-input cases.
- 2 tool or retrieval failure cases.
- 1 privacy/safety case.
- 1 latency stress case.

For higher-risk deployments, expand the suite and require human review.
