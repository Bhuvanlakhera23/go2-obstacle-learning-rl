# Experience Allocation and Acquisition–Retention Trade-offs in Blind Quadruped Obstacle Learning

### A Single-Seed Quadruped Reinforcement Learning Simulation Study

**Bhuvan Lakhera and Deepan Muthirayan**  
ARK Foundation Robotics Lab, Plaksha University, India.

Technical report V1.1 · version `v1.1.0` · Not a peer-reviewed conference publication.

## Why experience allocation?

A blind quadruped may spend a large training budget without acquiring difficult
obstacle skills. This development study compares a fixed retention/ascent mixture
with one specified competence-frontier sampler over the same task bank. Both
trained policies start from the same prior, use the same reward and receive
131,072,000 environment transitions. There is **one matched training-seed pair**.

## Principal findings

| Policy | Nominal explicit 16–18 cm detector-defined completions |
|---|---:|
| Fixed-Mixture Policy | **117/128** |
| Adaptive-Frontier Policy | **47/128** |
| Pretrained Reference (historical; not an equal-budget control) | **1/128** |

The fixed run received approximately 13.1× as many assignments and 17.1× as much
environment-time on the two hardest explicit training tasks. This association
does not isolate a causal mediator. Acquisition gains coexist with ordinary
locomotion costs, and adaptive-over-fixed counterexamples remain in the report.

## Read and reproduce

- [Complete technical report](TECHNICAL_REPORT.md).
- [CPU-only reproduction instructions](REPRODUCIBILITY.md).
- [Policy/checkpoint identity mapping](POLICY_IDENTITY_MAPPING.md).
- [Numerical invariance](NUMERICAL_VERIFICATION.md), [provenance](NUMERICAL_PROVENANCE.md)
  and [checksum/integrity receipt](VERIFICATION.json).
- [Related work](RELATED_WORK_VERIFICATION.md), [BibTeX references](references.bib),
  [claims and limitations](CLAIM_EVIDENCE_LIMITATIONS.md), [missing evidence](MISSING_EVIDENCE.md).

| Figure | SVG | PNG |
|---|---|---|
| High-obstacle completion | [Vector](figures/01_high_completion.svg) | [Preview](figures/01_high_completion.png) |
| Training-task exposure | [Vector](figures/02_training_exposure.svg) | [Preview](figures/02_training_exposure.png) |
| Allocation probabilities | [Vector](figures/03_allocation_probabilities.svg) | [Preview](figures/03_allocation_probabilities.png) |
| Cumulative training outcomes | [Vector](figures/04_training_outcomes.svg) | [Preview](figures/04_training_outcomes.png) |
| Acquisition–retention | [Vector](figures/05_acquisition_retention.svg) | [Preview](figures/05_acquisition_retention.png) |
| Per-fixture counterexamples | [Vector](figures/06_fixture_counterexamples.svg) | [Preview](figures/06_fixture_counterexamples.png) |

## Scope and limitations

Completion is detector-defined, **not independently validated physical traversal**.
There is no qualified independent contact or visual ground truth, no completed
reward-OFF ablation, no hardware-transfer result and no multi-training-seed
reliability claim. This does not disprove adaptive curricula or establish a new
curriculum algorithm. Evaluation episodes are not independent training seeds.
Ordinary squared raw-action change and squared torque are proxies, not mechanical
energy or measured hardware wear.

## Citation

Bhuvan Lakhera and Deepan Muthirayan (2026). *Experience Allocation and
Acquisition–Retention Trade-offs in Blind Quadruped Obstacle Learning.* Technical
Report V1.1. See [CITATION.cff](CITATION.cff). No DOI is assigned here. A separately
published Zenodo technical-report DOI may be added later without changing any
experimental record; automatic GitHub software archiving is not used.

## Licensing and exclusions

© 2026 Bhuvan Lakhera and Deepan Muthirayan. Manuscript, figures and numerical
tables: **CC BY 4.0**. Included plotting and verification code: **MIT**. See the
[file-scoped license statement](LICENSE.md). Original checkpoints, simulator/
experiment sources, robot assets, raw logs and internal approval evidence are
excluded. No institutional ownership, extra coauthor, ORCID or email is inferred.
