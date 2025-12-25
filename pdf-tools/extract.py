import pdfplumber
import pandas as pd
import os

def extract_pdf_content(pdf_path, output_dir="extracted"):
    os.makedirs(output_dir, exist_ok=True)
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                with open(f"{output_dir}/page_{i+1}_text.txt", "w") as f:
                    f.write(text)
            tables = page.extract_tables()
            for j, table in enumerate(tables):
                if table and len(table) > 1:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    df.to_csv(f"{output_dir}/page_{i+1}_table_{j+1}.csv", index=False)
    print(f"Extracted to {output_dir}/")

# Usage
# extract_pdf_content("input.pdf")

