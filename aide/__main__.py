"""CLI: python3 -m aide <command>. Utilitarian by design — the pixel-artist
skill is the primary interface; these commands are its hands."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="aide", description="Pixel-Art-Aide toolkit")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("render", help="render a .pxg source to a 1x PNG")
    p.add_argument("src")
    p.add_argument("-o", "--out", help="output PNG (default: alongside src)")

    p = sub.add_parser("preview", help="render a review sheet (1x, upscaled, gridded, tiled)")
    p.add_argument("src", help=".pxg or .png")
    p.add_argument("-o", "--out", required=True)
    p.add_argument("--tile", action="store_true", help="include a 3x3 tiling strip")
    p.add_argument("--label", default="")

    p = sub.add_parser("analyze", help="print texture metrics")
    p.add_argument("src", help=".pxg or .png")
    p.add_argument("--tile", action="store_true", help="expect seamless tiling; score the wrap seams")
    p.add_argument("--json", action="store_true", dest="as_json")

    p = sub.add_parser("compare", help="contact sheet of N candidates")
    p.add_argument("srcs", nargs="+", help=".pxg and/or .png files")
    p.add_argument("-o", "--out", required=True)
    p.add_argument("--tile", action="store_true")

    p = sub.add_parser("swatch", help="render a style card's palettes as swatches")
    p.add_argument("style", help="styles/<name>.md")
    p.add_argument("-o", "--out", required=True)

    p = sub.add_parser("import", help="convert a PNG into an editable .pxg")
    p.add_argument("src")
    p.add_argument("-o", "--out", help="output .pxg (default: alongside src)")

    args = ap.parse_args(argv)

    from aide import analyze as an
    from aide import compare as cmp
    from aide import styles as st
    from aide.grid import from_image, load_pxg, load_texture, to_image, to_text
    from aide.render import preview_sheet
    from PIL import Image

    if args.cmd == "render":
        out = Path(args.out) if args.out else Path(args.src).with_suffix(".png")
        to_image(load_pxg(args.src)).save(out)
        print(out)

    elif args.cmd == "preview":
        img = load_texture(args.src)
        label = args.label or Path(args.src).stem
        preview_sheet(img, label=label, tile=args.tile).save(args.out)
        print(args.out)

    elif args.cmd == "analyze":
        m = an.analyze(load_texture(args.src), expect_tiling=args.tile)
        if args.as_json:
            print(json.dumps(m, indent=2))
        else:
            print(f"== {args.src}")
            print(an.report(m, expect_tiling=args.tile))

    elif args.cmd == "compare":
        cmp.contact_sheet(args.srcs, tile=args.tile).save(args.out)
        print(args.out)

    elif args.cmd == "swatch":
        palettes = st.load_style_palettes(args.style)
        if not palettes:
            print(f"no ```palette blocks found in {args.style}", file=sys.stderr)
            return 1
        st.swatch_sheet(palettes).save(args.out)
        print(args.out)

    elif args.cmd == "import":
        out = Path(args.out) if args.out else Path(args.src).with_suffix(".pxg")
        out.write_text(to_text(from_image(Image.open(args.src))))
        print(out)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
