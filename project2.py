from pathlib import Path  # Work with file and folder paths.

from pypdf import PdfReader  # Read PDF pages and extract text.
from pypdf.errors import PyPdfError  # Catch PDF reading errors.

content = Path(__file__).resolve().parent / "content"  # Find content next to this script.

if not content.is_dir():
    raise SystemExit(f"Content folder is missing: {content}")

for name in ("One", "Two", "Three"):  # Outer loop: pick one folder.
    folder = content / name

    if not folder.is_dir():
        print(f"Folder is missing: {folder}")
        continue  # Move on to the next folder.

    pdf_files = sorted(folder.glob("*.pdf"))  # Find PDFs in filename order.

    if not pdf_files:
        print(f"No PDFs found in {folder}")
        continue

    sections = []  # Start a fresh list for this folder.

    for pdf_path in pdf_files:  # Inner loop: read each PDF in this folder.
        try:
            with pdf_path.open("rb") as source:
                reader = PdfReader(source)
                pages = [page.extract_text() or "" for page in reader.pages]
        except (OSError, PyPdfError) as error:
            print(f"Could not read {pdf_path}: {error}")
            continue  # Try the next PDF.

        if any(page.strip() for page in pages):
            text = "\n".join(pages)
            sections.append(f"--- {pdf_path.name} ---\n{text}")
        else:
            print(f"No selectable text in {pdf_path}")

    if not sections:
        continue  # Keep any existing output if no PDF yielded text.

    output_path = folder / "output.txt"
    try:
        # This line is outside the PDF loop. It writes once per folder.
        output_path.write_text("\n\n".join(sections) + "\n", encoding="utf-8")
        print(f"Saved {output_path}")
    except OSError as error:
        print(f"Could not write {output_path}: {error}")