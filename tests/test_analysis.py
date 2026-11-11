"""Public-bank integration tests and explicitly synthetic corruptions. No inference."""
import csv
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import reduce_records as reducer
import verify_current


class PublicAnalysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = reducer.reduce(ROOT / 'tables')

    def test_every_published_summary_cell(self):
        report = reducer.compare(ROOT / 'tables')
        self.assertEqual(sum(x['rows'] for x in report['comparisons'].values()), 639)
        self.assertTrue(all(x['integer_counts_exact'] for x in report['comparisons'].values()))

    def test_headline_is_sum_of_fixtures_and_seeds(self):
        for policy in reducer.POLICIES:
            high = next(r for r in self.result['endpoint_cohorts.csv'] if r['policy'] == policy and r['suite'] == 'nominal' and r['cohort'] == 'high_16_18')
            fixtures = [r for r in self.result['per_fixture.csv'] if r['policy'] == policy and r['suite'] == 'nominal' and r['cohort'] in ('task/heldout_isolated_16', 'task/heldout_isolated_18', 'task/heldout_staircase_16', 'task/heldout_staircase_18')]
            seeds = [r for r in self.result['high_by_evaluation_seed.csv'] if r['policy'] == policy and r['suite'] == 'nominal']
            self.assertEqual(high['success'], sum(r['success'] for r in fixtures))
            self.assertEqual(high['success'], sum(r['detector_defined_completion'] for r in seeds))
            self.assertEqual(high['n'], sum(r['n'] for r in fixtures))
            self.assertEqual(high['n'], sum(r['n'] for r in seeds))
            self.assertEqual(high['n'], sum(high[k] for k in ('success', 'failure', 'timeout', 'retention_horizon')))

    def test_training_evaluation_seed_distinction(self):
        budget = {r['parameter']: r['value'] for r in reducer.table(ROOT / 'tables/method_budget.csv')}
        report = reducer.compare(ROOT / 'tables')
        self.assertNotIn(int(budget['seed']), report['evaluation_seeds'])
        self.assertEqual(len(report['evaluation_seeds']), 2)
        self.assertEqual(report['training_seeds_per_continuation'], 1)

    def test_units_in_reader_documentation(self):
        doc = (ROOT / 'docs/REPRODUCIBILITY.md').read_text()
        for unit in set(reducer.UNITS.values()) - {'s'}:
            self.assertIn(unit, doc)
        self.assertIn('equal episode', doc)
        self.assertIn('not physical-contact', doc)

    def test_frozen_scientific_hashes(self):
        self.assertEqual(verify_current.verify(ROOT)['status'], 'PASS')

    def corrupt(self, edit):
        with tempfile.TemporaryDirectory() as d:
            tables = Path(d) / 'tables'
            shutil.copytree(ROOT / 'tables', tables)
            p = tables / 'first_episode_records.csv'
            rows = reducer.table(p)
            edit(rows)
            with p.open('w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
            with self.assertRaises((ValueError, KeyError)):
                reducer.compare(tables)

    def test_synthetic_schema_error(self):
        self.corrupt(lambda rows: [r.pop('attempted') for r in rows])

    def test_synthetic_nonfinite(self):
        self.corrupt(lambda rows: rows[0].update(effort='nan'))

    def test_synthetic_duplicate_identity(self):
        self.corrupt(lambda rows: rows.__setitem__(1, dict(rows[0])))

    def test_synthetic_incomplete_bank(self):
        self.corrupt(lambda rows: rows.pop())

    def test_synthetic_axis_shape(self):
        self.corrupt(lambda rows: rows[0].update(tracking_axes='[1, 2]'))

    def test_synthetic_unsupported_success(self):
        self.corrupt(lambda rows: rows[0].update(outcome='1', reason='10', hind_complete='False'))

    def test_synthetic_missing_and_corrupt_assets(self):
        for mode in ('missing', 'corrupt'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as d:
                dest = Path(d) / 'root'
                shutil.copytree(ROOT, dest, ignore=shutil.ignore_patterns('.git', '__pycache__', '.venv'))
                p = dest / 'tables/endpoint_cohorts.csv'
                if mode == 'missing':
                    p.unlink()
                else:
                    p.write_bytes(p.read_bytes() + b'corrupt')
                result = verify_current.verify(dest)
                self.assertEqual(result['status'], 'FAIL')
                self.assertEqual(result['discrepancies'][0]['file'], 'tables/endpoint_cohorts.csv')

    def test_synthetic_summary_count_corruption(self):
        with tempfile.TemporaryDirectory() as d:
            tables = Path(d) / 'tables'; shutil.copytree(ROOT / 'tables', tables)
            p = tables / 'high_by_evaluation_seed.csv'
            text = p.read_text(); p.write_text(text.replace(',64,1,', ',64,2,', 1))
            with self.assertRaisesRegex(ValueError, 'detector_defined_completion'):
                reducer.compare(tables)

    def test_figure_generation_cpu_smoke(self):
        with tempfile.TemporaryDirectory() as d:
            output = Path(d) / 'figures'
            env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', MPLBACKEND='Agg')
            subprocess.run([sys.executable, '-B', str(ROOT / 'scripts/render_figures.py'), '--output', str(output)], env=env, check=True, timeout=90, capture_output=True)
            self.assertEqual(len(list(output.glob('*.svg'))), 6)
            self.assertEqual(len(list(output.glob('*.png'))), 6)
            receipt = json.loads((output / 'render_receipt.json').read_text())
            self.assertFalse(receipt['native_executed']); self.assertEqual(receipt['forbidden_imports'], [])
            svg = (output / '01_high_completion.svg').read_text()
            self.assertIn('Detector-defined completion (%)', svg)
            self.assertIn('117/128', svg)
            with self.assertRaises(subprocess.CalledProcessError):
                subprocess.run([sys.executable, '-B', str(ROOT / 'scripts/render_figures.py'), '--output', str(output)], check=True, capture_output=True, timeout=20)


if __name__ == '__main__':
    unittest.main()
