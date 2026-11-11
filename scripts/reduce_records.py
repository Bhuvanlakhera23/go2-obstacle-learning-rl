#!/usr/bin/env python3
"""Independent offline aggregation of published labels, never a traversal detector.

Only CSV terminal summaries are read. No private source or model imports.
"""
import argparse
from collections import Counter, defaultdict
import csv
import json
import math
from pathlib import Path

POLICIES = ('Pretrained Reference', 'Fixed-Mixture Policy', 'Adaptive-Frontier Policy')
SUITES = ('nominal', 'slippery', 'disturbance')
EVALUATION_SEEDS = (173, 271)  # two evaluations, NOT two training replications
RECORD_FIELDS = 'policy suite evaluation_seed task_name env_id task outcome reason attempted hind_complete payout dwell_s seconds tracking tracking_axes effort smoothness source'.split()
UNITS = dict(vx_mae='m/s', vy_mae='m/s', yaw_mae='rad/s', effort='Nm²', smoothness='raw action units²', seconds='s')
COUNTS = ('n', 'success', 'failure', 'timeout', 'retention_horizon')
CONTINUOUS = ('tracking', 'effort', 'smoothness', 'vx_mae', 'vy_mae', 'yaw_mae')


def table(path, fields=None):
    with Path(path).open(newline='') as f:
        reader = csv.DictReader(f)
        names = reader.fieldnames
        if not names or len(set(names)) != len(names):
            raise ValueError(f'{path}: missing or duplicate columns')
        if fields is not None and set(names) != set(fields):
            raise ValueError(f'{path}: expected columns {fields}, got {names}')
        rows = list(reader)
        if not rows or any(None in r or any(v is None for v in r.values()) for r in rows):
            raise ValueError(f'{path}: empty or ragged table')
        return rows


def number(value):
    x = float(value)
    if not math.isfinite(x) or x < 0:
        raise ValueError(f'Expected finite nonnegative number, got {value!r}')
    return x


def flag(value):
    if value not in ('True', 'False'):
        raise ValueError(f'Invalid boolean {value!r}')
    return value == 'True'


def load(tables):
    tasks = table(tables / 'evaluation_tasks.csv')
    if [int(t['task_id']) for t in tasks] != list(range(24)) or len({t['name'] for t in tasks}) != 24:
        raise ValueError('Expected the 24 distinct published fixtures in task-ID order')
    for t in tasks:
        t['height'] = number(t['height'])
        t['command'] = json.loads(t['command'])
        if len(t['command']) != 3 or any(type(x) not in (int, float) or not math.isfinite(x) for x in t['command']):
            raise ValueError('Invalid signed velocity command')
    records = table(tables / 'first_episode_records.csv', RECORD_FIELDS)
    seen = set()
    for r in records:
        for k in ('evaluation_seed', 'env_id', 'task', 'outcome', 'reason'):
            r[k] = int(r[k])
        if r['policy'] not in POLICIES or r['suite'] not in SUITES or r['evaluation_seed'] not in EVALUATION_SEEDS:
            raise ValueError('Unknown policy, suite or evaluation seed')
        key = (r['policy'], r['suite'], r['evaluation_seed'], r['env_id'])
        if key in seen or not 0 <= r['env_id'] < 384 or r['task'] != r['env_id'] % 24:
            raise ValueError('Duplicate/missing first-episode identity or task allocation error')
        seen.add(key)
        if r['task_name'] != tasks[r['task']]['name']:
            raise ValueError('Task name/index mismatch')
        for k in ('attempted', 'hind_complete'):
            r[k] = flag(r[k])
        for k in ('payout', 'dwell_s', 'seconds', 'tracking', 'effort', 'smoothness'):
            r[k] = number(r[k])
        r['tracking_axes'] = json.loads(r['tracking_axes'])
        if len(r['tracking_axes']) != 3:
            raise ValueError('Expected three axis errors')
        r['tracking_axes'] = [number(x) for x in r['tracking_axes']]
        if r['seconds'] <= 0 or r['payout'] > 1 + 1e-8:
            raise ValueError('Invalid duration or payout')
        # Codes are terminal labels, not a reconstruction of physical contact.
        ordinary = tasks[r['task']]['family'] == 'ordinary'
        if r['outcome'] not in ((2, 7) if ordinary else (1, 2, 6)):
            raise ValueError('Invalid/unresolved terminal label for fixture family')
        if r['outcome'] == 1 and not (r['reason'] == 10 and r['attempted'] and r['hind_complete'] and r['dwell_s'] >= .3 - 1e-6 and abs(r['payout'] - 1) < 1e-6):
            raise ValueError('Completion label contradicts stored milestone summary')
        if r['outcome'] == 2 and r['reason'] not in (6, 7, 8, 9, 11, 15):
            raise ValueError('Unknown hard-failure reason')
        if r['outcome'] in (6, 7) and r['reason'] != {6: 13, 7: 14}[r['outcome']]:
            raise ValueError('Terminal outcome/reason mismatch')
    if len(seen) != 3 * 3 * 2 * 384:
        raise ValueError(f'Incomplete first-episode bank: {len(seen)} / 6912')
    return tasks, records


def cohorts(task):
    keys = ['all', 'family/' + task['family'], 'task/' + task['name']]
    if task['family'] in ('isolated', 'staircase'):
        keys.append(f"height/{round(task['height'] * 100):02d}")
        if task['height'] in (.16, .18):
            keys.append('high_16_18')
    if task['family'] in ('descent', 'native_descent'):
        keys.append('descent')
    if task['family'] == 'ordinary':
        vx, vy, yaw = task['command']
        direction = 'forward' if vx > 0 else 'backward' if vx < 0 else 'left' if vy > 0 else 'right' if vy < 0 else 'yaw_positive' if yaw > 0 else 'yaw_negative' if yaw < 0 else 'stand'
        keys.append('ordinary_direction/' + direction)
    return keys


def summarize(rows):
    n = len(rows)
    result = dict(zip(COUNTS, (n, sum(r['outcome'] == 1 for r in rows), sum(r['outcome'] == 2 for r in rows), sum(r['outcome'] == 6 for r in rows), sum(r['outcome'] == 7 for r in rows))))
    for key in ('tracking', 'effort', 'smoothness'):
        result[key] = math.fsum(r[key] for r in rows) / n
    for i, key in enumerate(('vx_mae', 'vy_mae', 'yaw_mae')):
        result[key] = math.fsum(r['tracking_axes'][i] for r in rows) / n
    return result


def reduce(tables):
    tasks, records = load(tables)
    groups = defaultdict(list)
    seeds = defaultdict(list)
    for r in records:
        for key in cohorts(tasks[r['task']]):
            groups[r['policy'], r['suite'], key].append(r)
        if 'high_16_18' in cohorts(tasks[r['task']]):
            seeds[r['policy'], r['suite'], r['evaluation_seed']].append(r)
    endpoint = [dict(policy=p, suite=s, cohort=k, **summarize(rows)) for (p, s, k), rows in sorted(groups.items())]
    failures = []
    for (p, s, k), rows in sorted(groups.items()):
        if k != 'high_16_18':
            continue
        reasons = Counter(r['reason'] for r in rows if r['outcome'] == 2)
        if set(reasons) - {6, 7, 8, 11}:
            raise ValueError('Published high-failure table cannot encode every observed reason')
        failures.append(dict(policy=p, suite=s, n=len(rows), detector_defined_completion=sum(r['outcome'] == 1 for r in rows), stuck=reasons[11], corridor_or_tile=reasons[8], collision=reasons[7], fall=reasons[6], timeout=sum(r['outcome'] == 6 for r in rows)))
    return {'endpoint_cohorts.csv': endpoint,
            'per_fixture.csv': [r for r in endpoint if r['cohort'].startswith('task/')],
            'high_failure_reasons.csv': failures,
            'high_by_evaluation_seed.csv': [dict(policy=p, suite=s, evaluation_seed=seed, n=len(rows), detector_defined_completion=sum(r['outcome'] == 1 for r in rows)) for (p, s, seed), rows in sorted(seeds.items())]}


def compare(tables):
    reconstructed = reduce(tables)
    checks = {}
    for filename, rows in reconstructed.items():
        public = table(tables / filename)
        # Provenance strings identify original collection, not newly computed metrics.
        key = lambda r: tuple(str(r[k]) for k in ('policy', 'suite', 'cohort', 'evaluation_seed') if k in r)
        indexed = {key(r): r for r in public}
        if len(indexed) != len(public) or set(indexed) != {key(r) for r in rows}:
            raise ValueError(f'{filename}: missing, duplicate or unexpected summary cells')
        maximum = 0.0
        for row in rows:
            actual = indexed[key(row)]
            if set(actual) != set(row) | {'source'}:
                raise ValueError(f'{filename}: summary schema mismatch')
            for field, value in row.items():
                if isinstance(value, str):
                    if actual[field] != value:
                        raise ValueError(f'{filename}: label mismatch')
                elif isinstance(value, int):
                    if int(actual[field]) != value:
                        raise ValueError(f'{filename}: {key(row)} {field}: expected {value}, published {actual[field]}')
                else:
                    delta = abs(float(actual[field]) - value)
                    maximum = max(maximum, delta)
                    if not math.isclose(float(actual[field]), value, rel_tol=1e-12, abs_tol=1e-12):
                        raise ValueError(f'{filename}: {key(row)} {field} differs by {delta}')
        checks[filename] = dict(rows=len(rows), max_absolute_continuous_error=maximum, integer_counts_exact=True)
    return dict(status='PUBLIC_LABEL_AGGREGATION_VERIFIED', first_episode_records=6912, training_seeds_per_continuation=1, evaluation_seeds=list(EVALUATION_SEEDS), units=UNITS, comparisons=checks, physical_contact_revalidated=False, native_executed=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tables', type=Path, default=Path(__file__).resolve().parents[1] / 'tables')
    args = parser.parse_args()
    print(json.dumps(compare(args.tables), indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
