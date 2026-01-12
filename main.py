import fitz  # PyMuPDF
import os
import json

DATA_DIR = "data"
OUTPUT_DIR = "output"
IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")

os.makedirs(IMAGE_DIR, exist_ok=True)


def extract_images_and_captions(pdf_name):
    pdf_path = os.path.join(DATA_DIR, pdf_name)
    doc = fitz.open(pdf_path)

    extracted = []

    for page_num in range(len(doc)):
        page = doc[page_num]

        image_entries = []
        for img in page.get_images(full=True):
            xref = img[0]
            try:
                bbox = page.get_image_bbox(img)
                image_entries.append((xref, bbox))
            except:
                continue 

        if not image_entries:
            continue

        text_blocks = page.get_text("blocks")
        captions = [
            block for block in text_blocks
            if block[4].strip().lower().startswith("fig.")
        ]

        for cap_idx, cap in enumerate(captions):
            cap_top = cap[1] 
            related_images = []

            for xref, bbox in image_entries:
                vertical_gap = cap_top - bbox.y1

                if 0 < vertical_gap < 25:
                    pix = fitz.Pixmap(doc, xref)

                    pix_rgb = fitz.Pixmap(fitz.csRGB, pix)

                    img_name = (
                        f"{os.path.splitext(pdf_name)[0]}"
                        f"_p{page_num+1}_fig{cap_idx}_{len(related_images)}.png"
                    )
                    img_path = os.path.join(IMAGE_DIR, img_name)

                    pix_rgb.save(img_path)

                    pix = None
                    pix_rgb = None

                    related_images.append(img_name)

            if related_images:
                extracted.append({
                    "page": page_num + 1,
                    "caption": cap[4].strip(),
                    "images": related_images
                })

                print(
                    f"Page {page_num+1}, caption '{cap[4].strip()}' "
                    f"→ {len(related_images)} image(s) saved."
                )

    return extracted


def main():
    all_results = []

    for pdf in os.listdir(DATA_DIR):
        if pdf.lower().endswith(".pdf"):
            all_results.extend(extract_images_and_captions(pdf))

    # Save metadata for verification
    meta_path = os.path.join(OUTPUT_DIR, "extracted_data.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)

    print("\nExtraction complete.")
    print(f"Images saved in: {IMAGE_DIR}")
    print(f"Metadata saved in: {meta_path}")


if __name__ == "__main__":
    main()
