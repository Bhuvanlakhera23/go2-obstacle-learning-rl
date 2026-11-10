# Read the report and check its analysis

Start with the research question and methods in the
[technical report](../TECHNICAL_REPORT.md), then compare the completion,
training-exposure and ordinary-locomotion figures. The published tables preserve
per-task results and counterexamples as well as aggregate outcomes.

## What can be reproduced here

The repository packages numerical tables and plotting code. With Python 3.10+,
NumPy and Matplotlib, regenerate the figures into a fresh directory:

```bash
F02B_FIGURES=$(mktemp -d)
PYTHONDONTWRITEBYTECODE=1 python3 scripts/render_figures.py \
  --tables tables --output "$F02B_FIGURES/figures"
```

This reads tables and draws figures on CPU. It does not run PPO, policy inference
or a simulator. Different plotting-library versions may produce different image
bytes even when the data agree. See the original
[analysis reproduction notes](REPRODUCIBILITY.md) for units and aggregation.

## Verify the unchanged scientific assets

From the repository root, this standard-library check compares the report,
tables, figures and references with the existing public layout receipt:

```bash
python3 -B - <<'PY'
import hashlib
import json
from pathlib import Path
root = Path('.')
receipt = json.loads((root / 'provenance/LAYOUT_VERIFICATION_V1.json').read_text())
selected = {
    path: expected for path, expected in receipt['files_sha256'].items()
    if path.startswith(('tables/', 'figures/'))
    or path in {'TECHNICAL_REPORT.md', 'references.bib'}
}
assert selected, 'No scientific assets selected'
mismatches = [path for path, expected in selected.items()
              if not (root / path).is_file()
              or hashlib.sha256((root / path).read_bytes()).hexdigest() != expected]
assert not mismatches, mismatches
print(f'{len(selected)} scientific assets match the recorded hashes.')
PY
```

The original whole-repository inventory checker and receipts describe earlier
presentation snapshots. They remain unchanged; later README/citation edits are
outside those byte inventories. The check above targets the scientific assets
without rewriting the historical receipts.

## Reading the results

There are two evaluation seeds, 173 and 271, with 16 first episodes per fixture and
seed. Each nominal frontier fixture therefore contributes 32 episodes, and the
four 16–18 cm fixtures contribute 128. These evaluation seeds do not add independent
PPO training replications.

Ordinary velocity errors are in m/s, yaw-rate error is in rad/s, mean squared
torque is in Nm², and squared raw-action increments use raw action units².
Episode means are averaged equally; exposure time is environment-time, not wall
clock time. Cumulative training outcomes are not held-out learning curves.

The current README is an introduction to the same study. It changes neither the
original v1.1.0 report nor its numerical results. The policies, raw experiment logs
and training implementation are not distributed by this report repository.
