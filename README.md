# Image–Caption Extraction from NCERT PDFs

## Overview
This project extracts images from NCERT Class 9 Science PDFs and maps each image to its corresponding caption.  
The focus is on **layout-aware extraction**, using PDF structural information without OCR or paid tools.

Chapters used for demonstration:
- Chapter 1 (Matter in Our Surroundings)
- Chapter 6 (Tissues)

---

## Features
- Automatically extracts images from selected PDF chapters.
- Maps each image (or multiple images) to its caption using spatial proximity.
- Excludes exercises sections to avoid unlabeled or irrelevant figures.
- Outputs:
  - Extracted images saved as PNG files.
  - Structured metadata in JSON containing:
    - Chapter name
    - Page number
    - Caption text
    - Associated image filenames

---

## Project Structure

image_caption_extractor/
├── extract.py # Main extraction script
├── requirements.txt # Dependencies
├── README.md # This documentation
├── data/ # Input PDFs (ignored in git)
│ ├── ch1.pdf
│ └── ch6.pdf
└── output/ # Generated output (ignored in git)
├── images/ # Extracted PNG images
└── metadata.json # Captions + image mapping


---

## Approach

1. **PDF Parsing**  
   Uses PyMuPDF (`fitz`) to access pages, images, and text blocks with positional data.

2. **Exercises Exclusion**  
   Pages containing "Exercises" are skipped to avoid diagrams without captions.

3. **Caption Detection**  
   Captions are identified using text blocks starting with `Fig.` or `Figure`.

4. **Image–Caption Mapping**  
   Images whose bottom edge is **just above a detected caption** are linked to that caption.  
   - Supports multiple images per caption.
   - Tolerance is applied to handle small spacing differences.

5. **Output Generation**  
   Images are saved as PNG files and metadata is exported as `metadata.json` for easy verification.

---

## Requirements

- Python 3.8+
- [PyMuPDF](https://pypi.org/project/PyMuPDF/)

Install dependencies:

```bash
pip install -r requirements.txt