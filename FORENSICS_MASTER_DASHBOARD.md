# 🚨 FORENSIC TOOLBOX ✅ DEPLOYED

## Status: LIVE ✅
```
pdfplumber ✓ PyPDF2 ✓ exifread ✓ 
Hash chain ✓ Bulk analysis ✓ File carving ✓
```

## 🔥 QUICK LAUNCH COMMANDS

**/forensics analyze_all evidence/**  
`bash /home/user/master-toolbox/forensics/analyze_all.sh evidence`

**/forensics pdf_all**  
`find evidence/ -name "*.pdf" -exec python3 /skills/forensics/tools/pdf_analyzer.py {} \\;`

**/forensics hash_chain**  
`find evidence/ -type f -exec sha256sum {} \\; > chain_of_custody.txt`

**/forensics timeline**  
`fls -r -m / evidence.img 2>/dev/null | head -50`

## 📁 STRUCTURE
```
/skills/forensics/tools/
├── pdf_analyzer.py     # Universal PDF/metadata
├── metadata_extractor.sh # EXIF bulk
└── SKILL.md

/master-toolbox/forensics/
├── analyze_all.sh      # Pipeline master
├── quick.sh           # One-liners
└── FORENSIC_MASTER.md
```

## 🛡️ BEST PRACTICES APPLIED
- Chain of custody (SHA256)
- Fallback analysis (pdfplumber/PyPDF2)
- Bulk processing ready
- Production-grade error handling
- JSON structured output

**READY FOR EVIDENCE PROCESSING**
