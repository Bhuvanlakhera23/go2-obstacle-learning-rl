# Reproduce the public analysis on CPU

This repository reproduces numerical aggregation and figures from published
terminal labels. It does not reproduce PPO training, observation construction,
physics experiments or the private supported-traversal detector.

## Install, verify, render

Use Python 3.10–3.12 in a fresh environment. The recorded local run uses Python
3.10, NumPy 1.21.5 and Matplotlib 3.5.1. The requirements include a separate
3.11/3.12 plotting profile; it has not been run locally. The verified GitHub CI profile uses Python 3.10.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -B scripts/verify_current.py
python -B -m unittest discover -s tests -v
python -B scripts/render_figures.py --tables tables --output outputs/reproduced-figures
```

The rendering output leaf must not exist. No command here imports a model,
starts a simulator, contacts hardware or needs private files. No dependency
installation or GitHub workflow execution was performed during V4 preparation.
The current verifier uses only the standard library.

## What the current verifier proves

`verify_current.py` checks the scientific file set and SHA256 values in
`provenance/scientific_assets_v4.json`. These were selected from the retained
public layout receipt, with the renderer and historical verification snapshots
also sealed. Missing/corrupt/extra scientific files are reported individually.
Later README and citation edits are outside this scientific inventory.

It then independently aggregates the 6,912 published first-episode records and
compares all numerical fields in 396 endpoint cohorts, 216 fixture rows, nine
high-failure rows and 18 evaluation-seed rows. Integer counts must match exactly;
continuous means use absolute and relative tolerances of 1e-12. The initial V4
run reports zero absolute difference for every compared continuous value.

Run just the reducer with:

```bash
python -B scripts/reduce_records.py --tables tables
```

The reducer validates the complete policy × suite × evaluation seed × environment
bank, environment-to-task indexing, finite metrics, terminal categories and
stored milestone consistency. See [reduction rules](REDUCTION_RULES.md). It reads
existing terminal labels; these are **not physical-contact** truth reobserved
from trajectories. First-foot event times and force histories are not available.

## Units and replication

Continuous metrics are **equal episode** means: vx/vy errors in m/s, yaw-rate error
in rad/s, mean squared applied joint torque in Nm², and squared raw-action
increments in raw action units². They are simulation proxies, not electrical
energy or measured wear. Exposure is environment-time, not wall-clock time.

Two evaluation seeds (173, 271) supply 16 first episodes per fixture per seed.
Each policy/suite has 768 records across 24 fixtures. The learning comparison is
one matched training-seed-73 pair; evaluation seeds are not independent training
replications. Native fixtures use seven 10.5 cm risers, distinct from the explicit
16/18 cm fixtures. Historical counts and their original contract are unchanged.

## Historical snapshots and rendering limits

`scripts/verify_public.py`, `VERIFICATION.json`, `MEDIA_UPDATE.json` and
`provenance/LAYOUT_VERIFICATION_V1.json` remain byte-preserved. The historical
checker compares a whole earlier layout and fails on subsequent presentation
changes. It is not the supported command for this current tree. Do not update
those receipts to make that old whole-tree check pass.

The original renderer remains byte-preserved. It reads only packaged tables and
writes a fresh directory with six PNG/SVG pairs and provenance. Cross-platform
image-byte identity is not promised; source tables, units and labels are checked.
The [CPU CI run](https://github.com/Bhuvanlakhera23/go2-obstacle-learning-rl/actions/runs/43008976023)
passed at commit `26670a717132ab7b4e2e361b07e1f78091c00253`, verifying
the current integrity/reduction command and the 14-test CPU suite. This does not
validate training or physics execution.

The [identity appendix](POLICY_IDENTITY_MAPPING.md) retains original checkpoint
and experiment identifiers; it grants no access to or rights over those files.
