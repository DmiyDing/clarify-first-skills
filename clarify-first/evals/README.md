# Eval Schema Notes

`clarify-first/evals/evals.json` is for behavioral evaluation prompts. It mixes human-readable expectations with a few machine-checkable fields.

## Fields

1. `id`: Stable eval identifier.
2. `prompt`: The user request used for evaluation.
3. `expected_output`: Human-readable summary of the intended behavior.
4. `risk_level`: Expected risk classification (`LOW`, `MEDIUM`, `HIGH`).
5. `should_trigger`: Whether the clarification gate should activate.
6. `contains_blocking_questions`: Whether the reply should ask blocking questions.
7. `language`: Expected reply language context such as `en` or `zh-CN`.
8. `expectations`: Additional human-readable checks.

## Why Both Structured and Prose Fields Exist

1. Structured fields make future tooling and CI assertions easier.
2. Prose fields keep the evals understandable for human reviewers.

## Relationship to Trigger Benchmark

Use `evals/evals.json` for richer behavioral expectations.  
Use [`../../benchmarks/trigger-evals/clarify-first.json`](../../benchmarks/trigger-evals/clarify-first.json) for small trigger-regression checks.
