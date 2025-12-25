#!/usr/bin/env python3
"""Standalone Gemini client - no CLI dependency"""
import google.generativeai as genai
import os
import sys
import argparse

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro-latest')

parser = argparse.ArgumentParser()
parser.add_argument("prompt", help="Prompt for Gemini")
parser.add_argument("--model", default="gemini-1.5-pro-latest")
args = parser.parse_args()

try:
    response = model.generate_content(args.prompt)
    print(response.text)
except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)
