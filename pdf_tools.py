"""Utility toolkit for programmatic PDF manipulation.

Features:
- Extract text per page to .txt
- Extract tables per page to JSON (via pdfplumber)
- Split PDFs into page ranges
- Merge multiple PDFs
- Inspect basic info and form fields
- Fill simple AcroForm fields (via pypdf)
- Create a demo PDF from scratch (via reportlab)

Usage examples:
  python pdf_tools.py extract-text input.pdf output.txt
  python pdf_tools.py extract-tables input.pdf output.json
  python pdf_tools.py split input.pdf out_dir 1-3 4-5
  python pdf_tools.py merge output.pdf input1.pdf input2.pdf
  python pdf_tools.py info input.pdf
  python pdf_tools.py list-fields input.pdf
  python pdf_tools.py fill-form template.pdf data.json filled.pdf
  python pdf_tools.py create-demo output.pdf
"""

import json
import sys
from pathlib import Path

import pdfplumber
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def extract_text(pdf_path: Path, out_path: Path) -> None:
    with pdfplumber.open(pdf_path) as pdf:
        parts = []
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            parts.append(f"=== Page {i} ===\n{text}\n\n")
    out_path.write_text("".join(parts), encoding="utf-8")


def extract_tables(pdf_path: Path, out_path: Path) -> None:
    all_tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables() or []
            for idx, table in enumerate(tables, start=1):
                all_tables.append({
                    "page": page_num,
                    "table_index": idx,
                    "rows": table,
                })
    out_path.write_text(json.dumps(all_tables, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_range(spec: str) -> range:
    if "-" in spec:
        start, end = spec.split("-", 1)
        return range(int(start), int(end) + 1)
    n = int(spec)
    return range(n, n + 1)


def split_pdf(pdf_path: Path, out_dir: Path, *ranges: str) -> None:
    reader = PdfReader(str(pdf_path))
    out_dir.mkdir(parents=True, exist_ok=True)

    if not ranges:
        ranges = ["1-%d" % len(reader.pages)]

    for spec in ranges:
        pages = list(parse_range(spec))
        writer = PdfWriter()
        for p in pages:
            if 1 <= p <= len(reader.pages):
                writer.add_page(reader.pages[p - 1])
        out_file = out_dir / f"{pdf_path.stem}_pages_{spec}.pdf"
        with out_file.open("wb") as f:
            writer.write(f)
        print(f"WROTE {out_file}")


def merge_pdfs(out_path: Path, inputs: list[Path]) -> None:
    writer = PdfWriter()
    for p in inputs:
        reader = PdfReader(str(p))
        for page in reader.pages:
            writer.add_page(page)
    with out_path.open("wb") as f:
        writer.write(f)


def pdf_info(pdf_path: Path) -> None:
    reader = PdfReader(str(pdf_path))
    num_pages = len(reader.pages)
    has_forms = bool(reader.get_fields())
    info = {
        "file": str(pdf_path),
        "pages": num_pages,
        "has_forms": has_forms,
    }
    print(json.dumps(info, indent=2))


def list_form_fields(pdf_path: Path) -> None:
    reader = PdfReader(str(pdf_path))
    fields = reader.get_fields() or {}
    simple = {}
    for name, field in fields.items():
        simple[name] = {
            "name": name,
            "type": str(getattr(field, "field_type", "")),
            "value": field.value if hasattr(field, "value") else None,
        }
    print(json.dumps(simple, indent=2))


def fill_form(pdf_path: Path, data: dict, out_path: Path) -> None:
    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()
    writer.append(reader)
    # Apply values to all pages that have forms
    for page in writer.pages:
        writer.update_page_form_field_values(page, data)
    with out_path.open("wb") as f:
        writer.write(f)


def create_demo_pdf(out_path: Path) -> None:
    c = canvas.Canvas(str(out_path), pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 18)
    c.drawString(72, height - 72, "Demo PDF Generated Programmatically")

    c.setFont("Helvetica", 11)
    body = (
        "This PDF was generated automatically using reportlab.\n\n"
        "It demonstrates programmatic document creation independent of any input template.\n"
        "You can modify pdf_tools.py -> create_demo_pdf() to customize layout, logos,\n"
        "headers/footers, page numbers, and dynamic content from your own data."
    )

    text_obj = c.beginText(72, height - 110)
    for line in body.splitlines():
        text_obj.textLine(line)
    c.drawText(text_obj)

    c.showPage()
    c.save()


def main(argv: list[str]) -> None:
    if len(argv) < 2:
        print("Usage: python pdf_tools.py <command> ...", file=sys.stderr)
        return

    cmd = argv[1]

    if cmd == "extract-text" and len(argv) == 4:
        extract_text(Path(argv[2]), Path(argv[3]))
    elif cmd == "extract-tables" and len(argv) == 4:
        extract_tables(Path(argv[2]), Path(argv[3]))
    elif cmd == "split" and len(argv) >= 4:
        split_pdf(Path(argv[2]), Path(argv[3]), *argv[4:])
    elif cmd == "merge" and len(argv) >= 5:
        merge_pdfs(Path(argv[2]), [Path(p) for p in argv[3:]])
    elif cmd == "info" and len(argv) == 3:
        pdf_info(Path(argv[2]))
    elif cmd == "list-fields" and len(argv) == 3:
        list_form_fields(Path(argv[2]))
    elif cmd == "fill-form" and len(argv) == 5:
        data = json.loads(Path(argv[3]).read_text(encoding="utf-8"))
        fill_form(Path(argv[2]), data, Path(argv[4]))
    elif cmd == "create-demo" and len(argv) == 3:
        create_demo_pdf(Path(argv[2]))
    else:
        print("Invalid command or arguments", file=sys.stderr)
        return


if __name__ == "__main__":
    main(sys.argv)
