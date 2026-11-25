"""Extract all pages of Chemistry Questions.pdf to output.txt."""

import argparse
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile

from pypdf import PdfReader
from pypdf.errors import PyPdfError

PDF_NAME = "Chemistry Questions.pdf"


def extract_pdf(folder: Path) -> tuple[Path, int]:
    """Read the PDF and return the output path and number of pages."""
    if not folder.is_dir():
        raise FileNotFoundError(f"Content folder does not exist: {folder}")

    pdf_path = folder / PDF_NAME
    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF file does not exist: {pdf_path}")

    with pdf_path.open("rb") as source:
        pages = [page.extract_text() or "" for page in PdfReader(source).pages]

    if not any(text.strip() for text in pages):
        raise ValueError(f"No selectable text found in {pdf_path}")

    output_path = folder / "output.txt"
    temporary_path = None
    try:
        with NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=folder, delete=False
        ) as output:
            temporary_path = Path(output.name)
            output.write("\n\n".join(text.rstrip() for text in pages) + "\n")
        temporary_path.replace(output_path)
    except OSError as error:
        raise OSError(f"Could not create or replace {output_path}: {error}") from error
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)

    return output_path, len(pages)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--content", type=Path, default=Path("/content"))
    args = parser.parse_args()

    try:
        output_path, page_count = extract_pdf(args.content)
    except (OSError, PyPdfError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Extracted {page_count} pages to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
