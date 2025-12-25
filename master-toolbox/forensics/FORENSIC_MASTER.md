# 🚨 FORENSIC INVESTIGATION MASTER TOOLBOX

## Core Pipeline (Execute in order)
```bash
# 1. Hash chain of custody
sha256sum -b evidence/* > chain_of_custody.txt

# 2. Bulk metadata extraction  
find evidence/ -type f \\( -name "*.pdf" -o -name "*.doc*" -o -name "*.jpg" \\) -exec /home/user/skills/forensics/tools/metadata_extractor.sh {} \\;

# 3. PDF deep analysis
find evidence/ -name "*.pdf" -exec python3 /home/user/skills/forensics/tools/pdf_analyzer.py {} \\; > pdf_report.json

# 4. Timeline reconstruction
fls -r -m / evidence.img | egrep -i "Jan|Feb|Mar" > timeline.txt  # Sleuthkit

# 5. Carve deleted files
foremost -i evidence.img -o recovered/
```

## MCP Integration Status
- [ ] File Extractor MCP (connect via UI Apps)
- [x] Local exiftool/pdfplumber (active)
- [ ] Autopsy GUI (`autopsy evidence.img`)

## Quick Commands
**/forensics/quick/pdf_all** - Analyze all PDFs
**/forensics/timeline** - Build timeline.txt
**/forensics/recover** - Carve deleted files

