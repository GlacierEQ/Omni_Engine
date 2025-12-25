#!/usr/bin/env python3
import hashlib, json, os, sys
from datetime import datetime
path = sys.argv[1] if len(sys.argv)>1 else 'test.txt'
h = hashlib.sha256(open(path,'rb').read()).hexdigest()
print(json.dumps({
    'file': path,
    'sha256': h,
    'size': os.path.getsize(path),
    'timestamp': datetime.utcnow().isoformat()
}, indent=2))
