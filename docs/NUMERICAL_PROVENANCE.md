# Numerical provenance

All 11 [table exports](NUMERICAL_VERIFICATION.md) are byte-identical to V1. They
come from the original B development study, not later retention protocols or
prospective confirmation. Exact original file hashes are retained in the
[historical inventory](../provenance/historical_inventory.json).

| Quantities | Table | Original evidence |
|---|---|---|
| Endpoint/high/suite/ordinary summaries | [Cohorts](../tables/endpoint_cohorts.csv) | Original first-terminal records, grouped by the retained offline reducer |
| All signed commands and obstacle fixtures | [Per-fixture](../tables/per_fixture.csv) | Exact task-name grouping across the two original evaluation seeds |
| Seed-specific high counts | [Evaluation seeds](../tables/high_by_evaluation_seed.csv) | Four fixtures × 16 episodes per invocation; not training replicates |
| Failure distribution | [Reasons](../tables/high_failure_reasons.csv) | Recorded terminal reason codes; no inferred biomechanical diagnosis |
| Individual terminal summaries | [Episodes](../tables/first_episode_records.csv) | All 6,912 unique original policy/suite/seed/env records; not trajectories |
| Assignment/time/outcome totals | [Exposure](../tables/training_exposure.csv) | Original final exposure ledgers and verified audit entries |
| Probability/outcome histories | [Snapshots](../tables/training_snapshot_history.csv) | 62 periodic windows plus endpoint per arm |
| Geometry and commands | [Training](../tables/training_tasks.csv), [evaluation](../tables/evaluation_tasks.csv) | Recorded task descriptors; not a new held-out bank |
| Budget and detector constants | [Budget](../tables/method_budget.csv), [thresholds](../tables/detector_thresholds.csv) | Original protocol and literal source Thresholds values |

CSV `source` fields use B/S logical aliases, source files and grouping keys. The
four architectural/checkpoint identities and the historical source documents
are indexed in [reproducibility](REPRODUCIBILITY.md) and
[evidence sources](EVIDENCE_SOURCES.md). Rendering uses only these portable CSVs;
per-figure table hashes are in [figure provenance](../figures/figure_provenance.json).
No original experiment file is modified or silently corrected.
