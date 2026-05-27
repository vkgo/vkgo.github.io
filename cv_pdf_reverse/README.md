# CV PDF Reverse Engineering

This folder contains a first-pass ReportLab reconstruction of the original downloadable CV PDF.

Run from the repository root:

```bash
python cv_pdf_reverse/rebuild_original_style.py
```

By default the script:

- reads `assets/pdf/wei_jin_huang_cv.pdf`
- extracts the embedded headshot with `pdfimages`
- writes outputs under `cv_pdf_reverse/output/`

The output directory is intentionally ignored by Git.
