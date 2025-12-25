#!/usr/bin/env python3
# ULTIMATE_SUPERLUMINAL_MATRIX v2.0 - glaciereq Case Matrix + FILEBOSS Integration
# Features: Exhibit correlation + Timeline analysis + Case graphing + Auto-chaining

import json, os, hashlib, argparse, networkx as nx
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from typing import Dict, List, Any

class UltimateCaseMatrix:
    def __init__(self, exhibits_dir="organized", case_id="DEFAULT"):
        self.exhibits_dir = Path(exhibits_dir)
        self.case_id = case_id
        self.matrix = defaultdict(list)
        self.graph = nx.DiGraph()
        self.timeline = []
        self.entities = Counter()
        
    def load_fileboss_inventory(self):
        """Load FILEBOSS output"""
        inv_path = self.exhibits_dir / "FILEBOSS_INVENTORY.json"
        if not inv_path.exists():
            raise FileNotFoundError(f"Run FILEBOSS first: python3 ULTIMATE_FILEBOSS.py")
        
        with open(inv_path) as f:
            data = json.load(f)
        
        self.exhibits = data['exhibits']
        self.duplicates = data.get('duplicates', {})
        
        print(f"✅ Loaded {len(self.exhibits)} exhibits from FILEBOSS")
        return data
    
    def extract_entities(self, text: str) -> List[str]:
        """Simple entity extraction (names, dates, amounts)"""
        entities = []
        # Names (capitalized words)
        entities.extend([w for w in text.split() if w[0].isupper() and len(w) > 2])
        # Dates (patterns)
        import re
        dates = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', text)
        entities.extend(dates)
        # Amounts
        amounts = re.findall(r'\$\d+(?:,\d{3})*(?:\.\d{2})?', text)
        entities.extend(amounts)
        return entities
    
    def build_correlation_graph(self):
        """Create exhibit relationship graph"""
        self.graph = nx.DiGraph()
        
        # Add exhibits as nodes
        for exh in self.exhibits:
            self.graph.add_node(exh['path'], type='exhibit', category=exh['category'])
        
        # Extract entities and link overlapping exhibits
        entity_exhibits = defaultdict(list)
        for exh in self.exhibits:
            if 'content_hash' in exh:  # Assume extracted
                entities = self.extract_entities(exh.get('preview', ''))
                for entity in entities[:5]:  # Top 5 entities per exhibit
                    entity_exhibits[entity].append(exh['path'])
        
        # Link exhibits sharing entities
        for entity, exhibits in entity_exhibits.items():
            if len(exhibits) > 1:
                for i in range(len(exhibits)):
                    for j in range(i+1, len(exhibits)):
                        self.graph.add_edge(exhibits[i], exhibits[j], entity=entity, weight=1.0)
        
        print(f"📊 Built graph: {self.graph.number_of_nodes()} nodes, {self.graph.number_of_edges()} edges")
    
    def generate_timeline(self):
        """Create chronological exhibit timeline"""
        timeline = []
        for exh in self.exhibits:
            mod_time = datetime.fromtimestamp(Path(exh['path']).stat().st_mtime)
            timeline.append({
                'exhibit': exh['path'],
                'category': exh['category'],
                'timestamp': mod_time.isoformat(),
                'size': Path(exh['path']).stat().st_size
            })
        self.timeline = sorted(timeline, key=lambda x: x['timestamp'])
        return self.timeline
    
    def generate_case_matrix(self):
        """Main matrix generation"""
        print("🔗 Building SUPERLUMINAL CASE MATRIX...")
        
        # Load FILEBOSS data
        data = self.load_fileboss_inventory()
        
        # Build graph + timeline
        self.build_correlation_graph()
        self.generate_timeline()
        
        # Generate matrix views
        matrix = {
            'case_id': self.case_id,
            'summary': {
                'total_exhibits': len(self.exhibits),
                'duplicate_sets': len(self.duplicates),
                'unique_entities': len(self.entities),
                'timeline_length': len(self.timeline),
                'graph_edges': self.graph.number_of_edges()
            },
            'views': {
                'timeline': self.timeline[:50],  # Top 50
                'clusters': self._get_clusters(),
                'chains': self._get_evidence_chains(),
                'stats': self._get_category_stats()
            },
            'graph': nx.readwrite.json_graph.node_link_data(self.graph)
        }
        
        output_path = self.exhibits_dir / f"CASE_MATRIX_{self.case_id}.json"
        with open(output_path, 'w') as f:
            json.dump(matrix, f, indent=2)
        
        # Markdown summary
        self._generate_markdown_report(output_path)
        
        print(f"✅ CASE MATRIX generated: {output_path}")
        return matrix
    
    def _get_clusters(self):
        """Identify exhibit clusters"""
        try:
            clusters = list(nx.connected_components(self.graph))
            return [{'size': len(c), 'exhibits': list(c)[:5]} for c in clusters if len(c) > 1]
        except:
            return []
    
    def _get_evidence_chains(self):
        """Find evidence chains"""
        try:
            paths = list(nx.all_simple_paths(self.graph, 
                source=list(self.graph.nodes)[0], 
                target=list(self.graph.nodes)[-1], cutoff=5))
            return [path[:5] for path in paths[:3]]
        except:
            return []
    
    def _get_category_stats(self):
        """Category breakdown"""
        cats = Counter(e['category'] for e in self.exhibits)
        return dict(cats)
    
    def _generate_markdown_report(self, json_path):
        """Human-readable report"""
        report_path = self.exhibits_dir / f"CASE_MATRIX_{self.case_id}.md"
        with open(report_path, 'w') as f:
            f.write(f"# SUPERLUMINAL CASE MATRIX - {self.case_id}\\n\\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
            f.write(f"**Exhibits**: {len(self.exhibits)} | **Connections**: {self.graph.number_of_edges()}\\n\\n")
            
            f.write("## 📊 Executive Summary\\n")
            f.write(f"- **{len(self._get_clusters())} evidence clusters** detected\\n")
            f.write(f"- **{len(self.duplicates)} duplicate sets** eliminated\\n")
            f.write(f"- **{len(self.timeline)} item timeline** reconstructed\\n\\n")
            
            f.write("## 🔗 Key Connections\\n```json\\n")
            f.write(json.dumps(self._get_evidence_chains(), indent=2)[:500] + "\\n```\\n")

def main():
    parser = argparse.ArgumentParser(description='ULTIMATE_SUPERLUMINAL_MATRIX')
    parser.add_argument('--case', default='AUTO', help='Case ID')
    parser.add_argument('--exhibits', default='organized', help='FILEBOSS output dir')
    parser.add_argument('--view', choices=['matrix', 'graph', 'timeline'], default='matrix')
    
    args = parser.parse_args()
    
    matrix = UltimateCaseMatrix(args.exhibits, args.case)
    matrix.generate_case_matrix()
    
    print("🚀 PIPELINE COMPLETE:")
    print("1. FILEBOSS → organized/ (dedupe + categorize)")
    print("2. SUPERLUMINAL_MATRIX → CASE_MATRIX_*.json + .md")
    print("3. Ready for deposition/trial")

if __name__ == '__main__':
    main()
