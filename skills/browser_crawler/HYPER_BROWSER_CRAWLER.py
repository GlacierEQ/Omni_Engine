#!/usr/bin/env python3
# HYPER-BROWSER CRAWLER v1.0 - Sequential Case Crawling + PDF Intelligence
from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup
import re, json, os, time
from pathlib import Path
from urllib.parse import urljoin, urlparse
from datetime import datetime
import hashlib

class HyperCrawler:
    def __init__(self, output_dir="browser_crawler"):
        self.output = Path(output_dir)
        self.output.mkdir(exist_ok=True)
        self.cases = []
        self.pdfs = []
    
    def sequential_case_crawl(self, start_url, case_pattern="case|docket|filing"):
        """Sequential case crawling with chronological intelligence"""
        print(f"🔍 Sequential crawling: {start_url}")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(start_url)
            
            # Extract case links chronologically
            links = page.query_selector_all("a[href*='case'], a[href*='docket'], a[href*='pdf']")
            case_urls = []
            
            for link in links:
                href = link.get_attribute("href")
                text = link.inner_text().lower()
                if re.search(case_pattern, text) or href.endswith('.pdf'):
                    full_url = urljoin(start_url, href)
                    date_match = re.search(r'(\d{4}-\d{2}-\d{2})|(\d{1,2}/\d{1,2}/\d{4})', text)
                    case_urls.append({
                        'url': full_url,
                        'text': text,
                        'date': date_match.group(0) if date_match else 'unknown',
                        'priority': 1 if href.endswith('.pdf') else 0
                    })
            
            case_urls.sort(key=lambda x: (x['priority'], x['date']))
            
            # Crawl each case sequentially
            for i, case in enumerate(case_urls[:20]):  # Limit to 20 cases
                print(f"📄 Case {i+1}: {case['url']}")
                try:
                    page.goto(case['url'], wait_until='networkidle')
                    self._extract_case_intelligence(page, case, i+1)
                    time.sleep(2)  # Respectful delay
                except: continue
            
            browser.close()
    
    def _extract_case_intelligence(self, page, case_info, case_num):
        """Extract PDFs + metadata from case page"""
        pdf_links = page.query_selector_all("a[href$='.pdf'], a[href*='document']")
        
        for link in pdf_links[:5]:  # Max 5 PDFs per case
            href = link.get_attribute("href")
            if href:
                full_url = urljoin(case_info['url'], href)
                filename = f"CASE-{case_num:03d}-{self._sanitize_filename(link.inner_text())[:30]}.pdf"
                
                # Download PDF
                pdf_data = requests.get(full_url, timeout=30).content
                hash_val = hashlib.sha256(pdf_data).hexdigest()
                
                pdf_path = self.output / "pdfs" / filename
                pdf_path.parent.mkdir(exist_ok=True)
                with open(pdf_path, 'wb') as f:
                    f.write(pdf_data)
                
                self.pdfs.append({
                    'case_num': case_num,
                    'case_url': case_info['url'],
                    'filename': str(pdf_path),
                    'url': full_url,
                    'hash': hash_val[:16],
                    'size': len(pdf_data),
                    'download_date': datetime.utcnow().isoformat()
                })
    
    def _sanitize_filename(self, text):
        return re.sub(r'[^\w\s-]', '', text).strip().replace(' ', '_')
    
    def organize_chronologically(self):
        """Organize PDFs by case sequence + chronology"""
        self.output / "organized" / "by_case".mkdir(exist_ok=True, parents=True)
        self.output / "organized" / "by_date".mkdir(exist_ok=True, parents=True)
        
        for pdf in self.pdfs:
            case_dir = self.output / "organized" / "by_case" / f"CASE-{pdf['case_num']:03d}"
            case_dir.mkdir(exist_ok=True)
            shutil.copy2(pdf['filename'], case_dir / Path(pdf['filename']).name)
        
        # Generate master inventory
        inventory = {
            'timestamp': datetime.utcnow().isoformat(),
            'total_cases': len(set(p['case_num'] for p in self.pdfs)),
            'total_pdfs': len(self.pdfs),
            'cases': self.cases,
            'pdfs': self.pdfs
        }
        
        with open(self.output / "CASE_INVENTORY_MASTER.json", 'w') as f:
            json.dump(inventory, f, indent=2)
        
        return inventory

if __name__ == '__main__':
    import sys
    crawler = HyperCrawler()
    if len(sys.argv) > 1:
        crawler.sequential_case_crawl(sys.argv[1])
    else:
        print("Usage: python3 HYPER_BROWSER_CRAWLER.py https://courtwebsite.com/cases")
    crawler.organize_chronologically()
    print(f"✅ HYPER-CRAWLER COMPLETE: {len(crawler.pdfs)} PDFs organized")
