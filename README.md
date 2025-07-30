# Omni_Engine

This repository contains utilities and scripts for experimenting with local AI workflows.

## Scripts

- **modules/filegpt/main.py** – Summarizes text, PDF, or DOCX files using the OpenAI API.
- **scripts/memory_builder.py** – Reads `memory_constellation.json` and creates the listed directories.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the memory builder to prepare directories:
   ```bash
   python scripts/memory_builder.py
   ```
3. Summarize a file:
   ```bash
   python modules/filegpt/main.py <path-to-file> --debug
   ```

This project is a work in progress. Some described features (e.g., quantum memory or autonomous initialization) are beyond the scope of this repository and are not implemented.
