#!/usr/bin/env python3
"""Extract original PDF artwork or a faithful page crop, with source provenance.

Optional dependency: uv run --with pymupdf python extract_paper_figure.py ...
Inspect the page inventory before choosing an image/clip; no caption-to-image guessing.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse


def require(ok, message):
    if not ok:
        raise ValueError(message)


def extract(args):
    import pymupdf
    require(args.pdf.is_file(), "PDF does not exist")
    require(urlparse(args.source_url).scheme in {"http", "https"}, "Supply a versioned HTTP(S) source URL")
    with pymupdf.open(args.pdf) as doc:
        require(1 <= args.page <= len(doc), "Page is outside PDF (use 1-based PDF page index)")
        page = doc[args.page - 1]
        blocks = page.get_text("dict")["blocks"]
        images = [b for b in blocks if b["type"] == 1]
        caption_hits = page.search_for(args.caption_text) if args.caption_text else []
        def block_text(block):
            return " ".join("".join(span["text"] for span in line["spans"]) for line in block["lines"])
        caption_blocks = [b for b in blocks if b["type"] == 0 and any(pymupdf.Rect(b["bbox"]).intersects(hit) for hit in caption_hits)]
        # Mentions elsewhere on the page are not the caption. Prefer a block
        # starting with the requested Figure/Table label, allowing PDF spacing.
        prefix = " ".join(args.caption_text.split()).rstrip(":.")
        anchored = [b for b in caption_blocks if re.match(re.escape(prefix) + r"\s*[:.]", " ".join(block_text(b).split()), re.I)] if prefix else []
        if anchored:
            caption_blocks = anchored
        caption_text = "\n".join(" ".join("".join(span["text"] for span in line["spans"]) for line in block["lines"]) for block in caption_blocks)
        caption_box = None
        for block in caption_blocks:
            caption_box = pymupdf.Rect(block["bbox"]) if caption_box is None else caption_box | pymupdf.Rect(block["bbox"])
        inventory = {"pdf_page": args.page, "page_rect": list(page.rect), "images": [{"index": i, "bbox": list(b["bbox"]), "width": b["width"], "height": b["height"], "format": b.get("ext")} for i,b in enumerate(images)], "caption_matches": [list(r) for r in caption_hits], "original_caption": caption_text, "caption_bbox_pdf_points": list(caption_box) if caption_box else None}
        if args.inspect:
            return inventory
        require(args.bundle_root is not None and args.output is not None, "Extraction needs --bundle-root and --output")
        require(bool(args.locator) and bool(args.alt) and bool(args.caption), "Extraction needs --locator, --alt and --caption")
        root = args.bundle_root.resolve()
        require(root.is_dir(), "Bundle root must already exist")
        destination = args.output.resolve()
        require(destination.is_relative_to(root) and destination.suffix.lower() == ".png", "Output must be a PNG inside the bundle root")
        require(destination.parent.is_dir(), "Create/verify the output parent before extracting")
        require(not destination.exists() or args.overwrite, "Output exists; explicitly pass --overwrite")
        require(not destination.with_suffix(".source.json").exists() or args.overwrite, "Provenance exists; explicitly pass --overwrite")
        require(not args.caption_text or bool(inventory["caption_matches"]), "Caption text not found on selected page; inspect the version/page before extracting")
        requested_clip = list(args.clip) if args.clip is not None else None
        bbox = list(page.rect)
        if args.mode == "embedded":
            require(args.image_index is not None and 0 <= args.image_index < len(images), "Choose an image index from --inspect")
            block = images[args.image_index]
            pix = pymupdf.Pixmap(block["image"])
            # PDF soft masks carry transparency separately from RGB artwork.
            # Dropping them makes black labels disappear into a black background.
            if block.get("mask"):
                pix = pymupdf.Pixmap(pix, pymupdf.Pixmap(block["mask"]))
            if pix.colorspace is None or pix.colorspace.n != 3:
                pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
            if pix.alpha:
                # Pixmap alpha samples are premultiplied; composite onto white.
                rgb = bytearray(pix.width * pix.height * 3)
                samples = pix.samples
                for pixel in range(pix.width * pix.height):
                    offset = pixel * 4
                    white = 255 - samples[offset + 3]
                    for channel in range(3):
                        rgb[pixel * 3 + channel] = min(255, samples[offset + channel] + white)
                pix = pymupdf.Pixmap(pymupdf.csRGB, pix.width, pix.height, bytes(rgb), False)
            bbox = list(block["bbox"])
            method = "original-embedded-image"
        else:
            require(72 <= args.dpi <= 600, "DPI must be between 72 and 600")
            if args.mode == "crop":
                require(args.clip is not None, "Crop mode requires --clip x0 y0 x1 y1 in PDF points")
                box = pymupdf.Rect(args.clip)
                require(not box.is_empty and page.rect.contains(box), "Crop must be inside the page, with positive dimensions")
                # For optional archival copies, include the full caption text block.
                # Normal slide crops keep the graphic and caption separate.
                if caption_box is not None and getattr(args, "include_caption", False):
                    box = (box | caption_box) + (-3, -3, 3, 3)
                    box = box & page.rect
                bbox = list(box)
            else:
                require(args.clip is None, "Use crop mode for --clip")
            pix = page.get_pixmap(matrix=pymupdf.Matrix(args.dpi / 72, args.dpi / 72), clip=pymupdf.Rect(bbox), alpha=False)
            method = "pdf-page-crop" if args.mode == "crop" else "pdf-full-page"
        require(pix.width >= 1 and pix.height >= 1, "Empty extracted image")
        png = pix.tobytes("png")
        figure = {"src": destination.relative_to(root).as_posix(), "alt": args.alt, "caption": args.caption, "source_url": args.source_url, "locator": args.locator, "original_caption": caption_text}
        provenance = {"figure": figure, "method": method, "background": "#ffffff", "pdf_soft_mask_present": bool(images[args.image_index].get("mask")) if args.mode == "embedded" else None, "pdf_name": args.pdf.name, "pdf_sha256": hashlib.sha256(args.pdf.read_bytes()).hexdigest(), "pdf_page": args.page, "bbox_pdf_points": bbox, "requested_clip_pdf_points": requested_clip, "caption_bbox_pdf_points": list(caption_box) if caption_box else None, "original_caption": caption_text, "caption_placement": "image" if getattr(args, "include_caption", False) else "text", "caption_fully_in_image": bool(caption_box and pymupdf.Rect(bbox).contains(caption_box)) if args.mode != "embedded" else False, "image_index": args.image_index if args.mode == "embedded" else None, "dpi": args.dpi if args.mode != "embedded" else None, "width": pix.width, "height": pix.height, "asset_sha256": hashlib.sha256(png).hexdigest(), "caption_search": args.caption_text, "caption_matches": inventory["caption_matches"], "review_status": "extracted; inspect image visually before publishing"}
        destination.write_bytes(png)
        destination.with_suffix(".source.json").write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+"\n")
        return provenance


def main():
    parser = argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pdf",type=Path)
    parser.add_argument("--source-url",required=True)
    parser.add_argument("--page",type=int,required=True,help="1-based physical PDF page, not printed article page")
    parser.add_argument("--inspect",action="store_true",help="List image bboxes and optional caption hits; write nothing")
    parser.add_argument("--caption-text",default="",help="Exact PDF caption fragment; preserve complete text as metadata")
    parser.add_argument("--include-caption",action="store_true",help="Optional archival crop including caption; not the default slide image")
    parser.add_argument("--mode",choices=["embedded","crop","page"],default="embedded")
    parser.add_argument("--image-index",type=int)
    parser.add_argument("--clip",type=float,nargs=4)
    parser.add_argument("--dpi",type=int,default=200)
    parser.add_argument("--bundle-root",type=Path)
    parser.add_argument("--output",type=Path)
    parser.add_argument("--locator")
    parser.add_argument("--alt")
    parser.add_argument("--caption")
    parser.add_argument("--overwrite",action="store_true")
    args=parser.parse_args()
    try:
        print(json.dumps(extract(args),ensure_ascii=False,indent=2))
    except ImportError:
        parser.exit(1,"PyMuPDF unavailable; use uv run --with pymupdf or an existing PDF screenshot tool.\n")
    except (ValueError,OSError) as exc:
        parser.exit(1,str(exc)+"\n")

if __name__ == "__main__":
    main()
