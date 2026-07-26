"""
CKAD Slide Deduplication Agent
================================
Finds and removes visually identical image slides (same MD5 hash of image bytes).
Keeps the FIRST occurrence of each image; removes all later duplicates.

Usage:
    python dedupe_ckad.py <input.pptx> [output.pptx]
    (if output omitted, overwrites input)

Exit 0 = clean (or fixed). Prints a JSON summary to stdout.
"""
import sys, hashlib, json
sys.stdout.reconfigure(encoding='utf-8')
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE


def is_fullslide_image(slide, prs):
    for sh in slide.shapes:
        if sh.shape_type == MSO_SHAPE_TYPE.PICTURE:
            if sh.width > int(prs.slide_width * 0.85):
                return True
    return False


def img_hash(slide):
    for sh in slide.shapes:
        if sh.shape_type == MSO_SHAPE_TYPE.PICTURE:
            return hashlib.md5(sh.image.blob).hexdigest()
    return None


def dedupe(input_path, output_path=None):
    if output_path is None:
        output_path = input_path

    prs = Presentation(input_path)
    slides = list(prs.slides)

    seen_hashes = {}   # hash → first slide number (1-indexed)
    remove_idx  = set()

    for i, slide in enumerate(slides):
        if not is_fullslide_image(slide, prs):
            continue
        h = img_hash(slide)
        if h is None:
            continue
        if h in seen_hashes:
            remove_idx.add(i)
        else:
            seen_hashes[h] = i + 1

    duplicates = [
        {"removed_slide": i + 1}
        for i in sorted(remove_idx)
    ]

    if remove_idx:
        sp = prs.slides._sldIdLst
        all_ids = list(sp)
        kept = [el for j, el in enumerate(all_ids) if j not in remove_idx]
        for el in list(sp):
            sp.remove(el)
        for el in kept:
            sp.append(el)
        prs.save(output_path)

    result = {
        "input":      input_path,
        "output":     output_path,
        "total_in":   len(slides),
        "total_out":  len(slides) - len(remove_idx),
        "duplicates_removed": len(remove_idx),
        "removed_slides": [d["removed_slide"] for d in duplicates],
        "clean": len(remove_idx) == 0,
    }
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python dedupe_ckad.py <input.pptx> [output.pptx]")
        sys.exit(2)

    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else inp
    result = dedupe(inp, out)
    print(json.dumps(result, indent=2))

    if result["clean"]:
        print(f"\nDEDUPE PASS — no duplicates found", file=sys.stderr)
    else:
        print(f"\nDEDUPE FIX — removed {result['duplicates_removed']} duplicate slides "
              f"(slides {result['removed_slides']})", file=sys.stderr)
    sys.exit(0)
