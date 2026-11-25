# Project 1 · Read a PDF and write a text file

The `content` folder includes the supplied Chemistry Questions PDF and the output generated from it. Use Python 3.10 or later.

From the extracted `project1` directory, run:

```bash
python -m pip install -r requirements.txt
python project1.py --content content
```

The script defaults to the absolute path `/content`. If you are using Colab and have copied the PDF into `/content`, run `python project1.py`.

1. Check that the content folder exists.
2. Find `Chemistry Questions.pdf` in that folder.
3. Read each page with `PdfReader` and extract its selectable text.
4. Write the text in UTF-8 to `output.txt` in the same folder.

| Condition | Program behavior |
| --- | --- |
| Content folder is missing | Prints a clear error and exits with status 1. |
| PDF is missing | Prints the expected PDF path and exits with status 1. |
| `output.txt` is missing | Creates it. |
| `output.txt` already exists | Replaces it after the new output has been written successfully. |
| Output cannot be written | Prints the output path and exits with status 1. |

The output contains selectable text from the PDF. Image-only scans require OCR.
