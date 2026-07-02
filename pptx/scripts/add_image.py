"""Add an image to a slide in an unpacked PPTX directory.

Usage:
    # Replace an existing image placeholder by index
    python add_image.py <unpacked_dir> <slide> <image> --replace-idx <idx>

    # Add a new image at specific coordinates (inches)
    python add_image.py <unpacked_dir> <slide> <image> --x <x> --y <y> --w <w> --h <h>

Examples:
    python add_image.py unpacked/ slide9.xml photo.jpg --replace-idx 6
    python add_image.py unpacked/ slide20.xml screenshot.png --x 1.0 --y 1.5 --w 6.0 --h 3.5

Replace mode: finds the <p:pic> element whose <p:ph idx="N"> matches --replace-idx,
              then swaps its <a:blip r:embed> to point at the new image file.

Add mode:     appends a new <p:pic> element to the slide's <p:spTree> at the given
              position and dimensions.

Both modes:
  1. Copy image to ppt/media/imageN.{ext} (next available number)
  2. Add <Default Extension> to [Content_Types].xml if needed
  3. Add <Relationship> to the slide's .rels file (next available rId)
  4. Update the slide XML
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

import defusedxml.minidom


# EMU = English Metric Units. 1 inch = 914400 EMU.
EMU_PER_INCH = 914400

MIME_MAP = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".bmp": "image/bmp",
    ".tiff": "image/tiff",
    ".tif": "image/tiff",
    ".wmf": "image/x-wmf",
    ".emf": "image/x-emf",
    ".svg": "image/svg+xml",
}

NS_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
NS_IMAGE_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"


def inches_to_emu(inches: float) -> int:
    return int(round(inches * EMU_PER_INCH))


def copy_image_to_media(unpacked_dir: Path, image_path: Path) -> tuple[str, str]:
    """Copy image into ppt/media/ with next available number. Returns (media_filename, extension)."""
    media_dir = unpacked_dir / "ppt" / "media"
    media_dir.mkdir(parents=True, exist_ok=True)

    ext = image_path.suffix.lower()
    if ext not in MIME_MAP:
        print(f"Error: unsupported image format '{ext}'", file=sys.stderr)
        sys.exit(1)

    existing_nums = []
    for f in media_dir.iterdir():
        m = re.match(r"image(\d+)\.", f.name)
        if m:
            existing_nums.append(int(m.group(1)))
    next_num = max(existing_nums) + 1 if existing_nums else 1

    dest_name = f"image{next_num}{ext}"
    shutil.copy2(image_path, media_dir / dest_name)
    return dest_name, ext


def ensure_content_type(unpacked_dir: Path, ext: str) -> None:
    """Add <Default Extension> to [Content_Types].xml if not already present."""
    ct_path = unpacked_dir / "[Content_Types].xml"
    dom = defusedxml.minidom.parse(str(ct_path))

    ext_no_dot = ext.lstrip(".")
    for default in dom.getElementsByTagName("Default"):
        if default.getAttribute("Extension").lower() == ext_no_dot.lower():
            return  # already registered

    mime = MIME_MAP.get(ext, f"image/{ext_no_dot}")
    types_el = dom.documentElement
    new_default = dom.createElement("Default")
    new_default.setAttribute("Extension", ext_no_dot)
    new_default.setAttribute("ContentType", mime)

    # Insert before first child to keep it near the top
    if types_el.firstChild:
        types_el.insertBefore(new_default, types_el.firstChild)
        # Add a newline text node for readability
        types_el.insertBefore(dom.createTextNode("\n"), new_default.nextSibling)
    else:
        types_el.appendChild(new_default)

    with open(ct_path, "wb") as f:
        f.write(dom.toxml(encoding="utf-8"))


def add_image_relationship(unpacked_dir: Path, slide_name: str, media_filename: str) -> str:
    """Add a Relationship entry to the slide's .rels file. Returns the new rId."""
    rels_dir = unpacked_dir / "ppt" / "slides" / "_rels"
    rels_dir.mkdir(parents=True, exist_ok=True)
    rels_path = rels_dir / f"{slide_name}.rels"

    if rels_path.exists():
        dom = defusedxml.minidom.parse(str(rels_path))
    else:
        dom = defusedxml.minidom.parseString(
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<Relationships xmlns="{NS_REL}"/>'
        )

    root = dom.documentElement

    # Find next available rId
    existing_rids = []
    for rel in dom.getElementsByTagName("Relationship"):
        m = re.match(r"rId(\d+)", rel.getAttribute("Id"))
        if m:
            existing_rids.append(int(m.group(1)))
    next_rid_num = max(existing_rids) + 1 if existing_rids else 1
    rid = f"rId{next_rid_num}"

    new_rel = dom.createElement("Relationship")
    new_rel.setAttribute("Id", rid)
    new_rel.setAttribute("Type", NS_IMAGE_REL)
    new_rel.setAttribute("Target", f"../media/{media_filename}")
    root.appendChild(new_rel)
    root.appendChild(dom.createTextNode("\n"))

    with open(rels_path, "wb") as f:
        f.write(dom.toxml(encoding="utf-8"))

    return rid


def replace_placeholder_image(unpacked_dir: Path, slide_name: str, rid: str, ph_idx: int) -> None:
    """Replace an existing <p:pic> placeholder's blip reference."""
    slide_path = unpacked_dir / "ppt" / "slides" / slide_name
    dom = defusedxml.minidom.parse(str(slide_path))

    # Find <p:pic> with matching <p:ph idx="N">
    found = False
    for pic in dom.getElementsByTagNameNS(NS_P, "pic"):
        # Look for <p:nvPicPr> → <p:nvPr> → <p:ph idx="N">
        for nv_pic_pr in pic.getElementsByTagNameNS(NS_P, "nvPicPr"):
            for nv_pr in nv_pic_pr.getElementsByTagNameNS(NS_P, "nvPr"):
                for ph in nv_pr.getElementsByTagNameNS(NS_P, "ph"):
                    idx_attr = ph.getAttribute("idx")
                    if idx_attr and int(idx_attr) == ph_idx:
                        # Found it — update the blip reference
                        for blip_fill in pic.getElementsByTagNameNS(NS_P, "blipFill"):
                            for blip in blip_fill.getElementsByTagNameNS(NS_A, "blip"):
                                blip.setAttributeNS(NS_R, "r:embed", rid)
                                found = True

    if not found:
        # Also try <p:pic> elements where the cNvPr id or name contains the idx,
        # or where the pic element has a blipFill but uses a non-namespaced ph
        for pic in dom.getElementsByTagNameNS(NS_P, "pic"):
            for ph in pic.getElementsByTagName("p:ph"):
                idx_attr = ph.getAttribute("idx")
                if idx_attr and int(idx_attr) == ph_idx:
                    for blip in pic.getElementsByTagName("a:blip"):
                        blip.setAttribute("r:embed", rid)
                        found = True

    if not found:
        print(f"Error: no <p:pic> placeholder with idx={ph_idx} found in {slide_name}", file=sys.stderr)
        sys.exit(1)

    with open(slide_path, "wb") as f:
        f.write(dom.toxml(encoding="utf-8"))

    print(f"Replaced placeholder idx={ph_idx} in {slide_name} → r:embed=\"{rid}\"")


def get_next_cNvPr_id(dom) -> int:
    """Find the next available id for <p:cNvPr> across all elements."""
    max_id = 0
    # Check all elements with an "id" attribute that look like cNvPr
    for tag in ("p:cNvPr", "cNvPr"):
        for el in dom.getElementsByTagName(tag):
            try:
                max_id = max(max_id, int(el.getAttribute("id")))
            except (ValueError, TypeError):
                pass
    # Also check namespace-aware
    for el in dom.getElementsByTagNameNS(NS_P, "cNvPr"):
        try:
            max_id = max(max_id, int(el.getAttribute("id")))
        except (ValueError, TypeError):
            pass
    return max_id + 1


def add_new_image(unpacked_dir: Path, slide_name: str, rid: str,
                  x: float, y: float, w: float, h: float) -> None:
    """Add a new <p:pic> element to the slide's <p:spTree>."""
    slide_path = unpacked_dir / "ppt" / "slides" / slide_name
    dom = defusedxml.minidom.parse(str(slide_path))

    next_id = get_next_cNvPr_id(dom)

    cx = inches_to_emu(w)
    cy = inches_to_emu(h)
    off_x = inches_to_emu(x)
    off_y = inches_to_emu(y)

    pic_xml = f'''<p:pic xmlns:a="{NS_A}" xmlns:r="{NS_R}" xmlns:p="{NS_P}">
  <p:nvPicPr>
    <p:cNvPr id="{next_id}" name="Image {next_id}"/>
    <p:cNvPicPr>
      <a:picLocks noGrp="1"/>
    </p:cNvPicPr>
    <p:nvPr/>
  </p:nvPicPr>
  <p:blipFill rotWithShape="1">
    <a:blip r:embed="{rid}"/>
    <a:stretch>
      <a:fillRect/>
    </a:stretch>
  </p:blipFill>
  <p:spPr>
    <a:xfrm>
      <a:off x="{off_x}" y="{off_y}"/>
      <a:ext cx="{cx}" cy="{cy}"/>
    </a:xfrm>
    <a:prstGeom prst="rect">
      <a:avLst/>
    </a:prstGeom>
  </p:spPr>
</p:pic>'''

    pic_dom = defusedxml.minidom.parseString(pic_xml)
    pic_el = pic_dom.documentElement

    # Find <p:spTree> and append
    sp_trees = dom.getElementsByTagNameNS(NS_P, "spTree")
    if not sp_trees:
        sp_trees = dom.getElementsByTagName("p:spTree")
    if not sp_trees:
        print(f"Error: no <p:spTree> found in {slide_name}", file=sys.stderr)
        sys.exit(1)

    sp_tree = sp_trees[0]

    # Import the node into this document before appending
    imported = dom.importNode(pic_el, deep=True)
    sp_tree.appendChild(imported)

    with open(slide_path, "wb") as f:
        f.write(dom.toxml(encoding="utf-8"))

    print(f"Added image at ({x}\", {y}\") {w}\"x{h}\" in {slide_name} → r:embed=\"{rid}\"")


def main():
    parser = argparse.ArgumentParser(
        description="Add an image to a slide in an unpacked PPTX directory."
    )
    parser.add_argument("unpacked_dir", type=Path, help="Path to unpacked PPTX directory")
    parser.add_argument("slide", help="Slide filename (e.g., slide9.xml)")
    parser.add_argument("image", type=Path, help="Path to image file")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--replace-idx", type=int, metavar="IDX",
                       help="Replace existing placeholder by <p:ph idx> value")
    group.add_argument("--x", type=float, metavar="X",
                       help="X position in inches (requires --y, --w, --h)")

    parser.add_argument("--y", type=float, metavar="Y", help="Y position in inches")
    parser.add_argument("--w", type=float, metavar="W", help="Width in inches")
    parser.add_argument("--h", type=float, metavar="H", help="Height in inches")

    args = parser.parse_args()

    if not args.unpacked_dir.exists():
        print(f"Error: {args.unpacked_dir} not found", file=sys.stderr)
        sys.exit(1)

    slide_path = args.unpacked_dir / "ppt" / "slides" / args.slide
    if not slide_path.exists():
        print(f"Error: {slide_path} not found", file=sys.stderr)
        sys.exit(1)

    if not args.image.exists():
        print(f"Error: {args.image} not found", file=sys.stderr)
        sys.exit(1)

    # Validate add mode has all coordinates
    if args.x is not None:
        missing = []
        if args.y is None:
            missing.append("--y")
        if args.w is None:
            missing.append("--w")
        if args.h is None:
            missing.append("--h")
        if missing:
            print(f"Error: --x requires {', '.join(missing)}", file=sys.stderr)
            sys.exit(1)

    # 1. Copy image to media
    media_filename, ext = copy_image_to_media(args.unpacked_dir, args.image)

    # 2. Ensure content type
    ensure_content_type(args.unpacked_dir, ext)

    # 3. Add relationship
    rid = add_image_relationship(args.unpacked_dir, args.slide, media_filename)

    # 4. Update slide XML
    if args.replace_idx is not None:
        replace_placeholder_image(args.unpacked_dir, args.slide, rid, args.replace_idx)
    else:
        add_new_image(args.unpacked_dir, args.slide, rid, args.x, args.y, args.w, args.h)


if __name__ == "__main__":
    main()
