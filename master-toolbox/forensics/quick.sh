#!/bin/bash
case "${1:-help}" in
  pdf_all) find . -name "*.pdf" -exec python3 /home/user/skills/forensics/tools/pdf_analyzer.py {} \; ;;
  timeline) fls -r -m / evidence.img 2>/dev/null | head -50 ;;
  recover) foremost -i evidence.img -o recovered/ 2>/dev/null || echo "No disk image found" ;;
  hash_all) find evidence/ -type f -exec sha256sum {} \; ;;
  *) echo "forensics: pdf_all | timeline | recover | hash_all" ;;
esac
