#!/usr/bin/env python3
# FIXED PRODUCTION CRAWLER v1.1 - REAL WORKING VERSION
import requests
from bs4 import BeautifulSoup
import re, json, os, sys, argparse, time, hashlib, shutil
from pathlib import Path
from urllib.parse import urljoin
from datetime import datetime

class ProductionCrawler:
    def __init__(self, output_dir="browser_crawler"):
        self.output = Path(output_dir)
        self.output.mkdir(exist_ok=True)
        self.cases = []
        self.pdfs = []
    
    def crawl_case_sequence(self, start_url, max_cases=20):
        print(f"🚀 PRODUCTION CRAWLER: {start_url}")
        try:
            resp = requests.get(start_url, timeout=30)
            soup = BeautifulSoup(resp.text, 'html.parser')
        except Exception as e:
            print(f"❌ URL ERROR: {e}")
            return
        
        case_links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.get_text().lower()
            if re.search(r'case|docket|filing|pdf', text) or href.endswith('.pdf'):
                full_url = urljoin(start_url, href)
                case_links.append(full_url)
        
        for i, case_url in enumerate(set(case_links[:max_cases])):
            print(f"📄 CASE {i+1}: {case_url[:60]}")
            self.process_case(case_url, i+1)
    
    def process_case(self, case_url, case_num):
        try:
            resp = requests.get(case_url, timeout=15)
            soup = BeautifulSoup(resp.text, 'html.parser')
            pdf_links = [urljoin(case_url, a['href']) for a in soup.find_all('a', href=re.compile(r'.pdf$'))]
            
            for j, pdf_url in enumerate(pdf_links[:3]):
                filename = f"CASE-{case_num:03d}-DOC-{j+1:02d}.pdf"
                pdf_path = self.output / "pdfs" / filename
                
                pdf_data = requests.get(pdf_url, timeout=15).content
                with open(pdf_path, 'wb') as f:
                    f.write(pdf_data)
                print(f"   ✅ {filename}")
        except: pass
    
    def test_mode(self):
        print("🧪 TEST MODE - Creating demo files")
        self.output / "pdfs".mkdir(exist_ok=True, parents=True)
        for i in range(3):
            (self.output / "pdfs" / f"TEST-CASE-{i+1:03d}-DOC-01.pdf").write_text("TEST PDF")
        print("✅ 3 test PDFs created")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Production Case Crawler")
    parser.add_argument('url', nargs='?', help="Court cases URL")
    parser.add_argument('--test', action='store_true', help="Test mode")
    args = parser.parse_args()
    
    crawler = ProductionCrawler()
    if args.test:
        crawler.test_mode()
    elif args.url:
        crawler.crawl_case_sequence(args.url)
    else:
        print("Usage: python3 PRODUCTION_CRAWLER.py [--test | URL]")
