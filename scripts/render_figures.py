#!/usr/bin/env python3
"""Portable CPU-only V1.1 rendering from byte-preserved V1 tables.

Plot construction follows V1 build_figures.py, SHA-256 recorded in preparation.
Only Figures 5/6 have editorial changes. No experiment imports or execution.
"""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile

POLICIES = ('Pretrained Reference', 'Fixed-Mixture Policy', 'Adaptive-Frontier Policy')
ARMS = ('Fixed-Mixture Policy', 'Adaptive-Frontier Policy')
SUITES = ('nominal', 'slippery', 'disturbance')
COLORS = {'Pretrained Reference': '#66717c', 'Fixed-Mixture Policy': '#007c83', 'Adaptive-Frontier Policy': '#d77b24'}
LABELS = {p: p for p in POLICIES}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, data):
    with path.open('x') as f:
        json.dump(data, f, indent=2, sort_keys=True, allow_nan=False)
        f.write('\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tables', type=Path, default=Path(__file__).resolve().parents[1] / 'tables')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError('Fresh rendering directory required')
    def load(name):
        with (args.tables / name).open(newline='') as f:
            return list(csv.DictReader(f))
    all_groups = {p: {s: {} for s in SUITES} for p in POLICIES}
    for r in load('endpoint_cohorts.csv'):
        cell = dict(n=int(r['n']), success=int(r['success']), smoothness=float(r['smoothness']),
                    effort=float(r['effort']), tracking_axes=[float(r[k]) for k in ('vx_mae', 'vy_mae', 'yaw_mae')])
        cell['success_rate'] = cell['success'] / cell['n']
        all_groups[r['policy']][r['suite']][r['cohort']] = cell
    exposure = [dict(r, assigned=int(r['assigned']), exposure_seconds=float(r['exposure_seconds']))
                for r in load('training_exposure.csv')]
    history = [dict(r, environment_transitions=int(r['environment_transitions']),
                    probability=float(r['probability']),
                    cumulative_closed_detector_success=int(r['cumulative_closed_detector_success']))
               for r in load('training_snapshot_history.csv')]
    tasks = load('evaluation_tasks.csv')
    os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp(prefix='f02b-v1-1-mpl-')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.patches import Rectangle
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'svg.fonttype': 'none', 'svg.hashsalt': 'f02b-public-report-v1',
                         'axes.titleweight': 'semibold'})
    out = args.output
    out.mkdir(parents=True, exist_ok=False)
    registry = []
    def save(fig, name, title, tables, note):
        fig.suptitle(title, fontsize=12, fontweight='semibold', y=.99)
        fig.text(.5, .012, note, ha='center', fontsize=7, color='#444444')
        fig.savefig(out / f'{name}.svg', metadata={'Date': None})
        fig.savefig(out / f'{name}.png', dpi=180)
        registry.append(dict(id=name, title=title, tables=tables, note=note,
                             tables_sha256={n: sha(args.tables / n) for n in tables},
                             uncertainty='None: one training seed pair; no invented intervals or trajectories'))
        plt.close(fig)
    # Figures 1–4 retain V1 plotting values, colors, scales and construction.
    fig, ax = plt.subplots(figsize=(8, 4.3))
    fig.subplots_adjust(top=.79, bottom=.19, left=.09, right=.99)
    for j, p in enumerate(POLICIES):
        v = [all_groups[p][s]['high_16_18'] for s in SUITES]
        bars = ax.bar(np.arange(3) + (j-1)*.25, [100*c['success_rate'] for c in v],
                      width=.23, color=COLORS[p], label=LABELS[p])
        for bar, c in zip(bars, v):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1.5,
                    f'{c["success"]}/{c["n"]}', ha='center', fontsize=8)
    ax.set(xticks=np.arange(3), xticklabels=['Nominal', 'Slippery material', 'Velocity disturbance'],
           ylim=(0, 103), ylabel='Detector-defined completion (%)')
    ax.legend(ncol=3, frameon=False, loc='upper center', bbox_to_anchor=(.5, 1.20), fontsize=8)
    save(fig, '01_high_completion', 'Explicit 16/18 cm endpoint evaluation', ['endpoint_cohorts.csv'],
         'Four fixtures; 128 assigned episodes/policy/suite. One training seed pair; evaluation seeds 173/271.')
    fig, axes = plt.subplots(1, 2, figsize=(8, 4.1))
    fig.subplots_adjust(top=.74, bottom=.21, wspace=.32)
    hard = ('isolated_18', 'staircase_18')
    for ax, key, unit, scale in ((axes[0], 'assigned', 'Task assignments', 1),
                                (axes[1], 'exposure_seconds', 'Observed environment-seconds (thousands)', 1000)):
        for j, arm in enumerate(ARMS):
            values = [next(r[key] for r in exposure if r['arm'] == arm and r['task'] == task) for task in hard]
            bars = ax.bar(np.arange(2)+(j-.5)*.32, [v/scale for v in values], width=.30,
                          color=COLORS[arm], label=LABELS[arm])
            for bar, v in zip(bars, values):
                ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()*1.01,
                        format(v/scale, '.1f') if scale != 1 else str(v), ha='center', fontsize=8)
        ax.set(xticks=np.arange(2), xticklabels=['Isolated 18 cm', 'Three-riser 18 cm'], ylabel=unit)
        ax.margins(y=.18)
    fig.legend(*axes[0].get_legend_handles_labels(), frameon=False, fontsize=8, ncol=2,
               loc='upper center', bbox_to_anchor=(.5, .91))
    save(fig, '02_training_exposure', 'Allocation to the two 18 cm training tasks', ['training_exposure.csv'],
         'One changing-policy training run per arm. Assignments and exposure time are not valid-contact encounter counts.')
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.8))
    fig.subplots_adjust(top=.80, bottom=.22, wspace=.24)
    for ax, task in zip(axes, hard):
        for arm in ARMS:
            rows = [r for r in history if r['arm'] == arm and r['task'] == task]
            ax.plot([r['environment_transitions']/1e6 for r in rows], [100*r['probability'] for r in rows],
                    '.-', markersize=3, lw=.9, color=COLORS[arm], label=LABELS[arm])
        ax.set(title=task.replace('_', ' '), xlabel='Environment transitions (millions)',
               ylabel='Logged allocation probability (%)', ylim=(0, 6))
    axes[0].legend(frameon=False, fontsize=8)
    save(fig, '03_allocation_probabilities', 'Task probabilities at saved training snapshots',
         ['training_snapshot_history.csv'],
         '62 periodic snapshots plus endpoint. Lines guide the eye; between-snapshot probabilities are not observed.')
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.8))
    fig.subplots_adjust(top=.80, bottom=.22, wspace=.29)
    for ax, task in zip(axes, hard):
        for arm in ARMS:
            rows = [r for r in history if r['arm'] == arm and r['task'] == task]
            ax.plot([r['environment_transitions']/1e6 for r in rows],
                    [r['cumulative_closed_detector_success'] for r in rows], '.-', markersize=2.7,
                    lw=1, color=COLORS[arm], label=LABELS[arm])
            ax.annotate(str(rows[-1]['cumulative_closed_detector_success']),
                        xy=(131.072, rows[-1]['cumulative_closed_detector_success']),
                        xytext=(-4, 5), textcoords='offset points', ha='right', fontsize=8, color=COLORS[arm])
        ax.set(title=task.replace('_', ' '), xlabel='Environment transitions (millions)',
               ylabel='Cumulative detector-defined\ncompletions')
        ax.margins(y=.12)
    axes[0].legend(frameon=False, fontsize=8)
    save(fig, '04_training_outcomes', 'Training outcomes under changing allocation and policy',
         ['training_snapshot_history.csv'],
         'Cumulative training counts, not endpoint rates or independently evaluated learning curves. Missing first-foothold events are not inferred.')
    # Figure 5: historical reference and squared raw-action-change semantics explicit.
    nominal = {p: all_groups[p]['nominal']['family/ordinary'] for p in POLICIES}
    ref = nominal['Pretrained Reference']
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.3))
    fig.subplots_adjust(top=.82, bottom=.24, wspace=.35)
    for p in POLICIES:
        x = 100*all_groups[p]['nominal']['high_16_18']['success_rate']
        y = 100*(nominal[p]['smoothness']/ref['smoothness']-1)
        axes[0].scatter([x], [y], color=COLORS[p], s=55, zorder=3)
        label = ('Pretrained Reference\n(historical)' if p == 'Pretrained Reference'
                 else 'Fixed-Mixture\nPolicy' if p == 'Fixed-Mixture Policy' else 'Adaptive-Frontier\nPolicy')
        axes[0].annotate(label, (x, y), xytext=(-6, -24) if p == 'Fixed-Mixture Policy' else (5, 6),
                         ha='right' if p == 'Fixed-Mixture Policy' else 'left',
                         textcoords='offset points', fontsize=8)
    axes[0].axhline(0, color='#aaaaaa', lw=.8)
    axes[0].set(xlim=(-3, 105), ylim=(-3, 24), xlabel='Nominal high detector-defined\ncompletion (%)',
                ylabel='Ordinary squared raw-action-change\nproxy increase vs historical reference (%)')
    for j, p in enumerate(ARMS):
        changes = [100*(nominal[p]['tracking_axes'][i]/ref['tracking_axes'][i]-1) for i in range(3)]
        changes += [100*(nominal[p]['effort']/ref['effort']-1)]
        axes[1].bar(np.arange(4)+(j-.5)*.32, changes, width=.30, color=COLORS[p], label=LABELS[p])
    axes[1].axhline(0, color='#aaaaaa', lw=.8)
    axes[1].set(xticks=np.arange(4), xticklabels=['vx MAE', 'vy MAE', 'Yaw MAE', 'Torque²'],
                ylabel='Ordinary metric change vs reference (%)')
    axes[1].legend(frameon=False, fontsize=8)
    save(fig, '05_acquisition_retention', 'Acquisition and retention: descriptive, not a causal frontier',
         ['endpoint_cohorts.csv'],
         '416 ordinary episodes/policy/suite. Pretrained Reference is not an equal-budget control. Action proxy is not energy or hardware wear.')
    # Figure 6: preserve native task order/counts; label both seven-riser fixtures.
    names = [t['name'] for t in tasks if t['family'] != 'ordinary']
    def fixture_label(name):
        if 'native' in name:
            direction = 'descent' if 'descent' in name else 'ascent'
            return 'Native 7-riser ' + direction + '\n(10.5 cm risers)'
        return name.removeprefix('heldout_').replace('_', ' ')
    fig, axes = plt.subplots(1, 2, figsize=(9, 6.4))
    fig.subplots_adjust(top=.88, bottom=.13, left=.24, right=.92, wspace=.18)
    for ax, suite in zip(axes, ('nominal', 'disturbance')):
        values = np.array([[all_groups[p][suite]['task/'+name]['success_rate']*100 for p in POLICIES] for name in names])
        im = ax.imshow(values, vmin=0, vmax=100, cmap='Blues', aspect='auto')
        for i, name in enumerate(names):
            for j, p in enumerate(POLICIES):
                c = all_groups[p][suite]['task/'+name]
                ax.text(j, i, f'{c["success"]}/{c["n"]}', ha='center', va='center', fontsize=8,
                        color='white' if values[i, j] > 58 else '#222222')
            if values[i, 2] > values[i, 1]:
                ax.add_patch(Rectangle((1.5, i-.5), 1, 1, fill=False, edgecolor='#d77b24', lw=2))
        ax.set(xticks=range(3), xticklabels=['Pretrained\nReference', 'Fixed-Mixture\nPolicy', 'Adaptive-Frontier\nPolicy'],
               yticks=range(len(names)), title=suite.capitalize())
        ax.tick_params(axis='x', labelsize=7)
        ax.set_yticklabels([fixture_label(n) for n in names] if ax is axes[0] else ['']*len(names), fontsize=8)
    fig.colorbar(im, ax=axes, fraction=.025, pad=.02, label='Detector-defined completion (%)')
    save(fig, '06_fixture_counterexamples', 'Per-fixture endpoint evaluation, including counterexamples',
         ['per_fixture.csv'],
         '32 episodes/fixture/policy/suite. Orange outline: adaptive exceeds fixed. Both native fixtures have 10.5 cm risers.')
    dump(out / 'figure_provenance.json', registry)
    forbidden = [n for n in sys.modules if n == 'torch' or n.startswith(('isaaclab', 'isaacsim', 'omni.'))]
    if forbidden:
        raise ValueError('Unexpected simulator/model imports')
    dump(out / 'render_receipt.json', dict(status='OFFLINE_V1_1_FIGURES_RENDERED',
         script_sha256=sha(Path(__file__)), python=sys.version,
         matplotlib=matplotlib.__version__, numpy=np.__version__,
         tables_sha256={p.name: sha(p) for p in sorted(args.tables.glob('*.csv'))},
         files_sha256={p.name: sha(p) for p in sorted(out.iterdir()) if p.is_file()},
         native_executed=False, cuda_executed=False, training_updates=0, forbidden_imports=forbidden))
    print('OFFLINE_V1_1_FIGURES_RENDERED: six SVG and six PNG files')


if __name__ == '__main__':
    main()
