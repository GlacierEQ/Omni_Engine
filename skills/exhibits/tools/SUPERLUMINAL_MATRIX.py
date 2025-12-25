#!/usr/bin/env python3
# SUPERLUMINAL_CASE_MATRIX v1.0 - Master Exhibit Correlation Engine
import json, os, hashlib, argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class CaseMatrix:
    def __init__(self, exhibits_dir="exhibits/processed"):
        self.exhibits_dir = Path(exhibits_dir)
        self.matrix = defaultdict(list)
    
    def load_exhibits(self):
        inventory = json.loads(Path('exhibits/processed/EXHIBIT_INVENTORY.json').read_text())
        transcripts = {}
        for tx_file in self.exhibits_dir.glob("TX-*.json"):
            transcripts[tx_file.stem] = json.loads(tx_file.read_text())
        
        for exh in inventory['exhibits']:
            exh['type'] = 'document'
            self.matrix['all'].append(exh)
            
            if exh['bates_id'] in transcripts:
                exh['transcript'] = transcripts[exh['bates_id']]
                self.matrix['transcribed'].append(exh)
    
    def generate_matrix(self):
        self.load_exhibits()
        matrix = {
            'case_matrix': {
                'generated': datetime.utcnow().isoformat(),
                'total_exhibits': len(self.matrix['all']),
                'categories': dict(self.matrix),
                'cross_references': self._build_xrefs()
            }
        }
        with open('exhibits/case_matrix/CASE_MATRIX_MASTER.json', 'w') as f:
            json.dump(matrix, f, indent=2)
        return matrix
    
    def _build_xrefs(self):
        xrefs = defaultdict(list)
        for exh in self.matrix['all']:
            h = exh['hash'][:8]
            xrefs[h].append(exh['bates_id'])
        return dict(xrefs)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--generate', action='store_true')
    args = parser.parse_args()
    
    matrix = CaseMatrix()
    if args.generate:
        result = matrix.generate_matrix()
        print(f"✅ SUPERLUMINAL_MATRIX: {result['case_matrix']['total_exhibits']} exhibits correlated")
