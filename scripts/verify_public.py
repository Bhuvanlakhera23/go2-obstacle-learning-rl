#!/usr/bin/env python3
"""Read-only standard-library check of this public candidate's exact contents."""
import hashlib
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    receipt = json.loads((root / 'VERIFICATION.json').read_text())
    expected = receipt['files_sha256']
    actual = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(root.rglob('*')) if p.is_file() and p != root / 'VERIFICATION.json'}
    if actual != expected:
        raise ValueError('Public payload file set or bytes differ from the recorded candidate')
    if not receipt['public_release_authorized']:
        raise ValueError('RC2 distribution approval missing')
    print(json.dumps(dict(status='PUBLIC_CANDIDATE_HASHES_VERIFIED', files=len(actual),
                          public_release_authorized=True, native_executed=False)))


if __name__ == '__main__':
    main()
