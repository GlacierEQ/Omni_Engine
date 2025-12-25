#!/usr/bin/env python3
# ADVANCED FORENSIC ANALYZER v3.0 - FIXED + PRODUCTION
import hashlib, json, os, argparse, subprocess
from datetime import datetime
from pathlib import Path
import sys

class ForensicAnalyzer:
    def __init__(self):
        self.libs = self._check_libs()
    
    def _check_libs(self):
        libs = {}
        checks = {
            'pdfplumber': ['pdfplumber', '--version'],
            'sleuthkit': ['fls', '-V'], 
            'binwalk': ['binwalk', '--version'],
            'exiftool': ['exiftool', '-ver']
        }
        for lib, cmd in checks.items():
            try: 
                subprocess.run(cmd, capture_output=True, check=True, timeout=5)
                libs[lib] = True
            except: 
                libs[lib] = False
        return libs
    
    def deep_hash(self, path):
        hashes = {}
        for algo in ['sha256', 'sha1', 'md5']:
            try:
                h = hashlib.new(algo)
                with open(path, 'rb') as f: h.update(f.read())
                hashes[algo] = h.hexdigest()
            except: hashes[algo] = 'ERROR'
        return hashes
    
    def analyze(self, path):
        stat = path.stat()
        result = {
            'target': str(path),
            'timestamp': datetime.utcnow().isoformat(),
            'capabilities': self.libs,
            'hashes': self.deep_hash(path),
            'size_bytes': stat.st_size,
            'mode': oct(stat.st_mode),
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
        }
        
        # PDF metadata
        if path.suffix.lower() == '.pdf' and self.libs.get('pdfplumber'):
            try:
                import pdfplumber
                with pdfplumber.open(path) as pdf:
                    result['pdf'] = {
                        'pages': len(pdf.pages),
                        'metadata': dict(pdf.metadata or {})
                    }
            except: pass
        
        return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HYPER FORENSIC INTELLIGENCE')
    parser.add_argument('target', nargs='+')
    args = parser.parse_args()
    
    analyzer = ForensicAnalyzer()
    for target in args.target:
        if os.path.exists(target):
            print(json.dumps(analyzer.analyze(Path(target)), indent=2))
        else:
            print(json.dumps({'error': f'{target} not found'}), indent=2)
