#!/usr/bin/env python3
"""Read-only exact inventory check; preserve the frozen report and explicit media delta."""
import hashlib
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    layout_path = root / 'provenance/LAYOUT_VERIFICATION_V1.json'
    if layout_path.exists():
        layout = json.loads(layout_path.read_text())
        for name, value in layout['historical_receipts_sha256'].items():
            if hashlib.sha256((root / name).read_bytes()).hexdigest() != value:
                raise ValueError('Historical verification record changed')
        actual = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in sorted(root.rglob('*')) if p.is_file()
                  and '.git' not in p.relative_to(root).parts and p != layout_path}
        if actual != layout['files_sha256']:
            raise ValueError('Current layout inventory or hashes differ from its receipt')
        print(json.dumps(dict(status='PRESENTATION_LAYOUT_HASHES_VERIFIED',
                              files=len(actual), original_release_tag=layout['original_release_tag'],
                              scientific_assets_unchanged=True, native_executed=False)))
        return
    receipt = json.loads((root / 'VERIFICATION.json').read_text())
    expected = dict(receipt['files_sha256'])
    media_path = root / 'MEDIA_UPDATE.json'
    if media_path.exists():
        media = json.loads(media_path.read_text())
        if hashlib.sha256((root / 'VERIFICATION.json').read_bytes()).hexdigest() != media['base_verification_sha256']:
            raise ValueError('Frozen report verification receipt changed')
        if media['base_tag'] != 'v1.1.0' or media['base_commit'] != '60ddb4a57325650add5f28d4a5be6d52ef415b7a':
            raise ValueError('Unexpected media supplement base')
        if set(media['overrides']) != {'README.md', 'scripts/verify_public.py'}:
            raise ValueError('Media supplement may change only README and its inventory checker')
        for name, change in media['overrides'].items():
            if expected.get(name) != change['base_sha256']:
                raise ValueError('Media override does not match frozen base')
            expected[name] = change['sha256']
        for name, value in media['added_files'].items():
            path = Path(name)
            if name in expected or path.is_absolute() or '..' in path.parts or not name.startswith('media/'):
                raise ValueError('Unexpected media supplement path')
            expected[name] = value
    actual = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(root.rglob('*')) if p.is_file() and '.git' not in p.relative_to(root).parts
              and p not in (root / 'VERIFICATION.json', media_path)}
    if actual != expected:
        raise ValueError('Public payload file set or bytes differ from the recorded candidate')
    if not receipt['public_release_authorized']:
        raise ValueError('RC2 distribution approval missing')
    print(json.dumps(dict(status='PUBLIC_CANDIDATE_HASHES_VERIFIED', files=len(actual),
                          public_release_authorized=True, native_executed=False)))


if __name__ == '__main__':
    main()
