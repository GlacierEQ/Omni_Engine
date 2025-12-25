#!/usr/bin/env python3
# ULTIMATE_FILEBOSS v2.0 - Merges glaciereq FILEBOSS + Workspace Organizer
# Features: Deduplication + Bates stamping + Intelligent categorization + Workspace cleanup

import os, sys, hashlib, shutil, json, argparse
from pathlib import Path
from datetime import datetime
import mimetypes

class UltimateFileBoss:
    def __init__(self, input_dir, output_dir=None, mode='organize'):
        self.input = Path(input_dir).resolve()
        self.mode = mode
        if output_dir:
            self.output = Path(output_dir).resolve()
            self.output.mkdir(exist_ok=True)
        self.exhibits = []
        self.duplicates = {}
        self.categories = {
            'docs': ['.md', '.txt', '.pdf', '.docx'],
            'scripts': ['.sh', '.py', '.js'],
            'configs': ['.json', '.yaml', '.yml', '.env'],
            'evidence': ['.jpg', '.png', '.pdf', '.wav', '.mp4']
        }
        
    def hash_file(self, path):
        h = hashlib.sha256()
        try:
            with open(path, 'rb') as f: 
                for chunk in iter(lambda: f.read(4096), b''):
                    h.update(chunk)
            return h.hexdigest()
        except:
            return None
    
    def categorize_file(self, path):
        ext = path.suffix.lower()
        for cat, exts in self.categories.items():
            if ext in exts:
                return cat
        return 'other'
    
    def bates_stamp(self, filename, index, category=''):
        timestamp = datetime.now().strftime('%Y%m%d')
        safe_name = Path(filename).stem[:30].replace(' ', '_')
        return f"{category.upper()}-{index:04d}-{timestamp}-{safe_name}{Path(filename).suffix}"
    
    def find_duplicates(self):
        """Find true duplicates across workspace"""
        hashes = {}
        for file in self.input.rglob('*'):
            if file.is_file() and file.stat().st_size > 1024:
                h = self.hash_file(file)
                if h:
                    if h not in hashes:
                        hashes[h] = []
                    hashes[h].append(str(file))
        
        duplicates = {h: files for h, files in hashes.items() if len(files) > 1}
        self.duplicates = duplicates
        return duplicates
    
    def organize_workspace(self):
        """Apply FILEBOSS logic to workspace organization"""
        print("🚀 ULTIMATE_FILEBOSS: Workspace Organization + Deduplication")
        
        # Create organized structure
        for cat in self.categories:
            (self.output / cat).mkdir(exist_ok=True)
        
        # Find and handle duplicates first
        dups = self.find_duplicates()
        if dups:
            print(f"⚠️  Found {len(dups)} duplicate sets")
            for h, files in dups.items():
                keep = files[0]  # Keep first occurrence
                for dupe in files[1:]:
                    shutil.move(dupe, self.output / 'archive' / f"DUPE-{Path(dupe).name}")
        
        # Categorize and move files
        moved = 0
        for file in self.input.rglob('*'):
            if file.is_file() and file.name not in ['ULTIMATE_FILEBOSS.py', 'workspace_organization_report.md']:
                cat = self.categorize_file(file)
                cat_dir = self.output / cat
                cat_dir.mkdir(exist_ok=True)
                
                new_name = self.bates_stamp(file.name, moved+1, cat)
                dest = cat_dir / new_name
                
                if not dest.exists():
                    shutil.move(str(file), str(dest))
                    self.exhibits.append({
                        'path': str(dest),
                        'original': str(file),
                        'category': cat,
                        'hash': self.hash_file(file)
                    })
                    moved += 1
        
        print(f"✅ Organized {moved} files into categories")
        self.save_inventory()
    
    def save_inventory(self):
        inventory = {
            'summary': {
                'total_files': len(self.exhibits),
                'duplicates_found': len(self.duplicates),
                'categories': {cat: len([e for e in self.exhibits if e['category']==cat]) 
                              for cat in self.categories}
            },
            'exhibits': self.exhibits,
            'duplicates': self.duplicates
        }
        with open(self.output / 'FILEBOSS_INVENTORY.json', 'w') as f:
            json.dump(inventory, f, indent=2)
        print(f"📊 Inventory saved: {self.output}/FILEBOSS_INVENTORY.json")

def main():
    parser = argparse.ArgumentParser(description='ULTIMATE_FILEBOSS - Workspace + Exhibits')
    parser.add_argument('input', nargs='?', default='/home/user', help='Input directory')
    parser.add_argument('-o', '--output', default='/home/user/organized', help='Output directory')
    parser.add_argument('--dry-run', action='store_true', help='Preview only')
    parser.add_argument('--dedupe-only', action='store_true', help='Duplicates only')
    
    args = parser.parse_args()
    
    boss = UltimateFileBoss(args.input, args.output)
    
    if args.dry_run:
        print("🐱 PREVIEW MODE")
        dups = boss.find_duplicates()
        print(f"Found {len(dups)} duplicate sets")
        return
    
    if args.dedupe_only:
        boss.find_duplicates()
        print("Duplicates identified - review FILEBOSS_INVENTORY.json")
        return
    
    boss.organize_workspace()

if __name__ == '__main__':
    main()
