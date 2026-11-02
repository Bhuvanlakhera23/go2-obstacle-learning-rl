# Evidence-source index

This portable index replaces links requiring a private workstation. It identifies
existing documents, not new validation. Exact file identities are in
[evidence_sources.json](provenance/evidence_sources.json) and the full
[historical inventory](provenance/historical_inventory.json). B denotes the
original `artifacts/foundation02b/learning_v1_inferencefix2` data root; S the
original experiment repository; STUDY the central research workspace.
EXTERNAL identifiers are stable aliases for protected out-of-tree inputs.

## Audit

STUDY/reports/EVIDENCE_AUDIT_V1.md; STUDY/reports/metrics.json;
STUDY/reports/provenance.json. These establish the original matched run identities,
raw-record reduction, detector interpretation and documented uncertainties.
The V1 package's complete file inventory is also retained in
[v1_files.json](provenance/v1_files.json).

## Comparison

STUDY/docs/EXPERIMENT_COMPARISON.md. Saved B/fixed/params and B/adaptive/params
agent/environment YAMLs and original source identify the shared architecture,
initializer, PPO recipe and sampling intervention. Checkpoint and task hashes are
listed in [the reproducibility appendix](REPRODUCIBILITY.md).

## Publication gate

STUDY/reports/PUBLICATION_READINESS_GATE_V1.md. Its replication requirement is
not converted into multi-seed evidence by editing this report.

## Prospective gate

STUDY/reports/PROSPECTIVE_STUDY_GATE_V1.md. Prospective observable confirmation
remains blocked/unexecuted; no untouched test bank is created retrospectively.

## Native closure

STUDY/reports/PHASE3_R3_EVAL_SNAPSHOT_REPAIR_AND_COLLECTOR_AUDIT_V1.md.
R1 failed startup, R2 failed the step-9 inference-tensor pose edit and R3 failed
periodic evaluation-snapshot telemetry. An isolated GPU-physics probe succeeded,
but did not validate robot contact collection. The evaluation-snapshot repair
remained regression-unqualified; collector liveness remained unresolved. An empty
contact file is not evidence of no physical contact. No R4 is authorized.

## Export closure

STUDY/reports/PASSIVE_OBSERVABLE_EXPORT_ADAPTER_V1.md. Per-view isolation remained
unqualified for co-located task replicas; independent visual traversal adjudication
was not established. No camera-export result is introduced by V1.1.

These source documents are not bundled as licensed public artifacts. Custodian
access and redistribution review are separate from the integrity checks in this
package. The technical report's scientific limitations are self-contained and
do not depend on a reader treating inaccessible source links as validation.
