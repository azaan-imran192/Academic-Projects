"""Verify upstream LFS content before copying it into ignored local folders."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil


def verified_path(source, item):
    path = (source / item['path']).resolve()
    if not path.is_relative_to(source.resolve()):
        raise ValueError('Resource path leaves source directory')
    if not path.is_file() or path.stat().st_size != item['size']:
        raise ValueError(f"Missing, incomplete or pointer-only resource: {item['path']}")
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    if digest.hexdigest() != item['oid']:
        raise ValueError(f"SHA-256 mismatch: {item['path']}")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--training-data', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    items = json.loads((root / 'lfs-resources.json').read_text(encoding='utf-8'))
    selected = [x for x in items if args.training_data or
                x['path'].startswith('models/mbert_toxic_final/') or
                x['path'] == 'data/ruhsold/hate_words_roman_urdu.txt']
    # Validate the complete selection before writing any resource.
    sources = [(verified_path(args.source, item), item) for item in selected]
    for source, item in sources:
        target = (root / item['path']).resolve()
        if not target.is_relative_to(root):
            raise ValueError('Resource path leaves project directory')
        if target.exists():
            verified_path(root, item)  # Never silently replace different local data.
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    print(f'Verified {len(selected)} resources; local assets remain Git-ignored.')


if __name__ == '__main__':
    main()
