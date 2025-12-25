#!/usr/bin/env python3
# FILEBOSS v1.0 - Exhibit Intelligence + Deduplication + Bates Stamping
import hashlib, os, json, shutil, argparse
from pathlib import Path
from datetime import datetime

class FileBoss:
    def __init__(self, input_dir, output_dir):
        self.input = Path(input_dir)
        self.output = Path(output_dir)
        self.output.mkdir(exist_ok=True)
        self.exhibits = []
    
    def hash_file(self, path):
        h = hashlib.sha256()
        with open(path, 'rb') as f: h.update(f.read())
        return h.hexdigest()
    
    def bates_stamp(self, filename, index):
        return f"EXH-{index:04d}-{datetime.now().strftime('%Y%m%d')}-{Path(filename).stem[:20]}.pdf"
    
    def organize(self):
        hashes = {}
        for i, file in enumerate(self.input.rglob('*'), 1):
            if file.suffix.lower() in {'.pdf', '.docx', '.jpg', '.png', '.wav', '.mp4'}:
                h = self.hash_file(file)
                if h in hashes:
                    shutil.copy2(file, self.output / f"DUPE-{hashes[h]}_vs_{file.name}")
                else:
                    bates_name = self.bates_stamp(file.name, i)
                    shutil.copy2(file, self.output / bates_name)
                    hashes[h] = bates_name
                    self.exhibits.append({
                        'bates_id': bates_name,
                        'original': str(file),
                        'hash': h,
                        'size': file.stat().st_size
                    })
        return self.exhibits
    
    def report(self):
        return {'exhibits': self.exhibits, 'total': len(self.exhibits), 'duplicates': len(hashes)-len(self.exhibits)}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FILEBOSS - Exhibit Master')
    parser.add_argument('input', default='evidence')
    parser.add_argument('-o', '--output', default='exhibits/processed')
    args = parser.parse_args()
    
    boss = FileBoss(args.input, args.output)
    exhibits = boss.organize()
    with open(args.output + '/EXHIBIT_INVENTORY.json', 'w') as f:
        json.dump(boss.report(), f, indent=2)
    print(f"✅ FILEBOSS: {len(exhibits)} exhibits organized → {args.output}")
