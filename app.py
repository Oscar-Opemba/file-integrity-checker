import argparse
import hashlib
import json
from common import serve

def digests(path):
    sha256 = hashlib.sha256(); sha512 = hashlib.sha512()
    with open(path, 'rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            sha256.update(chunk); sha512.update(chunk)
    return sha256.hexdigest(), sha512.hexdigest()

def analyze(values):
    path = values.get('path', '').strip()
    if not path: return {'error': 'Enter a local file path.'}
    try: sha256, sha512 = digests(path)
    except (OSError, ValueError) as exc: return {'error': f'Unable to read file: {exc}'}
    expected = values.get('expected', '').strip().lower()
    result = {'path': path, 'sha256': sha256, 'sha512': sha512}
    if expected: result.update({'expected_sha256': expected, 'matches_expected': expected == sha256})
    return result

def main():
    parser = argparse.ArgumentParser(description='Hash a local file; no file is uploaded.')
    parser.add_argument('path', nargs='?'); parser.add_argument('--expected'); parser.add_argument('--web', action='store_true'); parser.add_argument('--port', type=int, default=8087)
    args = parser.parse_args()
    if args.web: serve('File Integrity Checker', [('path','Local file path','text','/path/to/file'),('expected','Expected SHA-256 (optional)','text','Leave blank to calculate only')], analyze, args.port)
    elif args.path: print(json.dumps(analyze({'path':args.path,'expected':args.expected or ''}), indent=2))
    else: parser.print_help()

if __name__ == '__main__': main()
