#!/usr/bin/env python3
# MEGA-PDF v1.0 - Exhibit Compilation + Bates + Annotations
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import json, os, argparse
from pathlib import Path

class MegaPDF:
    def __init__(self, exhibits_dir):
        self.exhibits_dir = Path(exhibits_dir)
    
    def create_index(self, exhibits, output='exhibits/case_index.pdf'):
        c = canvas.Canvas(output, pagesize=letter)
        y = 750
        c.drawString(100, y, "📋 EXHIBIT INDEX - OFFICIAL")
        y -= 40
        c.drawString(100, y, f"Generated: {datetime.now().isoformat()}")
        y -= 60
        
        for i, exh in enumerate(exhibits, 1):
            c.drawString(100, y, f"{i:03d}. {exh['bates_id']} ({exh['size']/1024:.1f}KB)")
            y -= 25
            if y < 100: 
                c.showPage()
                y = 750
        c.save()
        return output
    
    def compile_master(self, exhibits, output='exhibits/MASTER_EXHIBIT_FILE.pdf'):
        writer = PdfWriter()
        for exh in exhibits:
            reader = PdfReader(self.exhibits_dir / exh['bates_id'])
            for page in reader.pages:
                writer.add_page(page)
        with open(output, 'wb') as f:
            writer.write(f)
        return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', action='store_true')
    parser.add_argument('--master', action='store_true')
    args = parser.parse_args()
    
    with open('exhibits/processed/EXHIBIT_INVENTORY.json') as f:
        exhibits = json.load(f)['exhibits']
    
    mp = MegaPDF('exhibits/processed')
    if args.index: mp.create_index(exhibits)
    if args.master: mp.compile_master(exhibits)
    print("✅ MEGA-PDF: Index/Master compiled")
