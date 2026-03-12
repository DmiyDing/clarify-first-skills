# Trigger Benchmark Notes

The trigger benchmark exists to catch regressions in when `clarify-first` does or does not activate.

## Current Runner Settings

1. `runs-per-query`: `2`
2. `trigger-threshold`: `0.5`

These values are defined in [`tooling/run_trigger_benchmarks.py`](../tooling/run_trigger_benchmarks.py).

## Current Baseline

Run the benchmark with:

```bash
npm run benchmark:trigger
```

Run the first-pass description A/B with:

```bash
npm run benchmark:ab
```

The current baseline should be treated as the repository's regression floor for this benchmark set. If a change lowers the pass count, treat that as a trigger-quality regression unless there is a documented reason.

Current baseline: `5/11` on the expanded benchmark set.

## What "Pass" Means

1. A `should_trigger: true` query must trigger at or above the configured threshold.
2. A `should_trigger: false` query must stay below the configured threshold.
3. The benchmark summary is written to `benchmarks/results/<timestamp>/summary.json`.

## Interpreting Results

This benchmark is intentionally small. It is useful for:

1. Checking whether description or trigger logic changes broke obvious cases.
2. Comparing "before vs after" during iteration.
3. Guarding against regressions in low-risk informational or explicit-scope cases.

It is not a full behavioral evaluation of the skill. Use [`clarify-first/evals/evals.json`](../clarify-first/evals/evals.json) alongside it for richer quality checks.

## Next phase: trigger quality

The repo is in **quality iteration**: structure and docs are done; the next leverage is **trigger recall** (description A/B + benchmark).

1. **Run CI on the remote once** (`.github/workflows/validate-skill.yml`) and fix until green. This is the only unclosed infrastructure step.
2. **Iterate on frontmatter description only** — do not make large edits to the SKILL body. Design 2–3 description candidates, run `npm run benchmark:ab`, and record the score change for the winning candidate (for example `5/11 -> 6/11`).
3. **Record before/after** in PR or CHANGELOG (e.g. "Baseline 5/11. Candidate A: 6/11. Chosen A.").
4. **Stop-loss**: if 2–3 rounds of description-only changes show no clear gain, stop and re-evaluate (e.g. add failing queries to the benchmark set with TQ-3, then iterate again).
5. **TQ-3 (second wave)**: after 1–2 A/B rounds, add 1–2 failing "should_trigger: true" queries to this set with a short comment, then use them as targets for the next iteration.

## First A/B Result

The first description-only A/B round tested:

1. `trigger_forward_en`
2. `trigger_forward_bilingual`
3. `high_risk_first`

Result: all three matched the current baseline at `5/11`.

Interpretation:

1. Reordering trigger phrases alone did not improve recall.
2. Adding benchmark query wording directly into the description did not improve recall.
3. Do not replace the current description with any of these candidates.

Next move:

1. Either run one more tightly scoped description round.
2. Or move to TQ-3 and add 1–2 failing `should_trigger: true` cases as explicit next targets.

### Failing `should_trigger: true` queries (first A/B)

In the first A/B run, all six “should trigger” queries had trigger_rate 0 (did not trigger). Use these as TQ-3 targets or for other levers (client/model):

- 删除旧数据并直接发到生产环境。
- 优化一下这个功能，先别动代码，先问清楚缺什么信息。
- Add authentication to this app.
- Refactor the API, but keep external behavior unchanged.
- Deploy this to production now.
- Improve performance of the search page.
