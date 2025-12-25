from pypdf import PdfReader, PdfWriter
import sys

def merge_pdfs(input_paths, output_path):
    writer = PdfWriter()
    for path in input_paths:
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)
    with open(output_path, "wb") as f:
        writer.write(f)
    print(f"Merged to {output_path}")

if __name__ == "__main__":
    merge_pdfs(sys.argv[1:-1], sys.argv[-1])

