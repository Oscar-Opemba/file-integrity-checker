import argparse
import hashlib
import json
import re
from common import serve
from security_utils import read_local_file

def digests(path):
    data=read_local_file(path,max_bytes=512*1024*1024); return hashlib.sha256(data).hexdigest(),hashlib.sha512(data).hexdigest(),len(data)
def analyze(values):
    path=values.get('path','').strip()
    if not path: return {'error':'enter a local file path'}
    try: sha256,sha512,size=digests(path)
    except (OSError,ValueError) as exc: return {'error':str(exc)}
    expected=values.get('expected','').strip().lower(); result={'file_name':path,'size_bytes':size,'sha256':sha256,'sha512':sha512}
    if expected:
        if not re.fullmatch(r'[0-9a-f]{64}',expected): return {'error':'expected SHA-256 must be exactly 64 hexadecimal characters'}
        result.update({'expected_sha256':expected,'matches_expected':expected==sha256})
    return result
def main():
    parser=argparse.ArgumentParser(description='Hash a local file; no file is uploaded.')
    parser.add_argument('path',nargs='?'); parser.add_argument('--expected'); parser.add_argument('--web',action='store_true'); parser.add_argument('--port',type=int,default=8087)
    args=parser.parse_args()
    if args.web: serve('File Integrity Checker',[('path','Local file path','text','/path/to/file'),('expected','Expected SHA-256 (optional)','text','Leave blank to calculate only')],analyze,args.port)
    elif args.path: print(json.dumps(analyze({'path':args.path,'expected':args.expected or ''}),indent=2))
    else: parser.print_help()
if __name__=='__main__': main()
