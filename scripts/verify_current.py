#!/usr/bin/env python3
"""Supported current integrity and public-label check; no experiment execution."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

from reduce_records import compare


def verify(root):
    inventory = json.loads((root / 'provenance/scientific_assets_v4.json').read_text())
    errors = []
    for name, expected in inventory['files_sha256'].items():
        p = root / name
        if p.is_symlink() or not p.is_file():
            errors.append({'file': name, 'problem': 'missing file or symlink'})
        elif hashlib.sha256(p.read_bytes()).hexdigest() != expected:
            errors.append({'file': name, 'problem': 'SHA256 mismatch'})
    scientific = {str(p.relative_to(root)) for folder in ('tables', 'figures') for p in (root / folder).rglob('*') if p.is_file()}
    expected = {p for p in inventory['files_sha256'] if p.startswith(('tables/', 'figures/'))}
    for name in sorted(scientific - expected):
        errors.append({'file': name, 'problem': 'unexpected scientific asset'})
    if errors:
        return dict(status='FAIL', discrepancies=errors, native_executed=False)
    return dict(status='PASS', scientific_and_historical_files=len(inventory['files_sha256']), aggregation=compare(root / 'tables'), native_executed=False, training_reproduced=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        result = verify(args.root)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        result = dict(status='FAIL', error=f'{type(exc).__name__}: {exc}', native_executed=False)
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
