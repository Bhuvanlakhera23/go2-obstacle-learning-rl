# Claim–evidence–limitation matrix

| Claim | Packaged evidence | Limitation |
|---|---|---|
| Fixed exceeds this adaptive arm on nominal high fixtures | [Cohorts](../tables/endpoint_cohorts.csv): 117/128 versus 47/128 | One matched training-seed pair; detector-defined completion only |
| Pretrained Reference has 1/128 nominal high completions | Same original cohort table | Historical reference, not equal-budget causal control |
| Fixed has greater hard-task exposure | [Exposure](../tables/training_exposure.csv): assignment/time ratios 13.1×/17.1× | Exposure is associated with outcome, not causally isolated |
| Allocation/outcome history is recoverable | [Saved histories](../tables/training_snapshot_history.csv) | Changing-policy cumulative counts, not held-out learning curves or first-contact traces |
| Ordinary-motion costs coexist with acquisition | [Per-fixture metrics](../tables/per_fixture.csv) | Squared action/torque proxies are not energy or hardware wear |
| Adaptive performs better on some fixtures | Native ascent and disturbance-descent cells in the same table | No blanket fixed or adaptive superiority |
| Shaping and detector are shared | [Source identities](../provenance/evidence_sources.json), [thresholds](../tables/detector_thresholds.csv) | No reward-OFF ablation; no independent contact or visual ground truth |
| The experiment is reproducible as an offline reduction | [Preparation scope](NUMERICAL_VERIFICATION.md), [verification](../VERIFICATION.json) | Historical record integrity, not simulator replay or physical validation |
| Cited allocation methods are relevant but different | [Related-work verification](RELATED_WORK_VERIFICATION.md) | No direct LP-ACRL/PSC evaluation, algorithmic novelty or comprehensive literature ranking |

Native/contact/export closure remains as recorded in [the evidence index](EVIDENCE_SOURCES.md).
No row authorizes an experiment, further repair or public distribution.
