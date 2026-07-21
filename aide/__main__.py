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

    p = sub.add_parser("render", help="render a .pxg source to a 1x PNG (alpha-bled)")
    p.add_argument("src")
    p.add_argument("-o", "--out", help="output PNG (default: alongside src)")
    p.add_argument("--no-bleed", action="store_true", help="skip alpha-bleed of transparent pixels")

    p = sub.add_parser("bleed", help="alpha-bleed transparent pixels of an existing PNG (mipmap fix)")
    p.add_argument("src")
    p.add_argument("-o", "--out", help="output PNG (default: overwrite src)")

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

    p = sub.add_parser("block", help="isometric block preview from face textures")
    p.add_argument("side", help=".pxg or .png used for the sides (and top unless --top)")
    p.add_argument("--top", help="texture for the top face")
    p.add_argument("--right", help="texture for the right face (default: same as side)")
    p.add_argument("--scale", type=int, default=8)
    p.add_argument("-o", "--out", required=True)

    p = sub.add_parser("model", help="render a Minecraft model (any shape); auto-textures if no texture given")
    p.add_argument("model", help="path to a model .json")
    p.add_argument("--single", help="apply one texture (.pxg/.png) to every face")
    p.add_argument("--tex", action="append", default=[], metavar="KEY=PATH",
                   help="map a texture key to a file (repeatable)")
    p.add_argument("--texdir", help="textures root; resolves the model's namespaced texture paths")
    p.add_argument("--tint", action="append", default=[], metavar="IDX=RRGGBB",
                   help="tint color for a tintindex (repeatable)")
    p.add_argument("--ramp", default="8A6BB5", help="base hex for the auto-texture ramp")
    p.add_argument("--scale", type=int, default=140)
    p.add_argument("-o", "--out", required=True)

    p = sub.add_parser("lift", help="lift a 2D silhouette (.pxg/.png) into a 3D voxel model")
    p.add_argument("src", help="silhouette source; opaque pixels are the shape")
    p.add_argument("--mode", choices=["revolve", "blade"], default="revolve",
                   help="revolve = lathe about the long axis (round); blade = flat, edge-tapered")
    p.add_argument("--thickness", type=int, default=6, help="blade mode: max Z thickness in voxels")
    p.add_argument("--color", default="8A6BB6", help="flat material hex for previews/viewer")
    p.add_argument("--obj", help="write a Wavefront .obj here")
    p.add_argument("--iso", help="write a flat-shaded iso preview PNG here")
    p.add_argument("--html", help="write a self-contained rotatable WebGL viewer here")

    p = sub.add_parser("autotex", help="generate a starter texture laid out for a model's UVs")
    p.add_argument("model", help="path to a model .json")
    p.add_argument("--base", default="8A6BB5", help="base hex for the ramp")
    p.add_argument("--no-frame", action="store_true", help="skip the per-face panel frame")
    p.add_argument("-o", "--out", required=True)

    args = ap.parse_args(argv)

    from aide import analyze as an
    from aide import compare as cmp
    from aide import styles as st
    from aide.grid import from_image, load_pxg, load_texture, save_texture, to_image, to_text
    from aide.render import preview_sheet
    from PIL import Image

    if args.cmd == "render":
        out = Path(args.out) if args.out else Path(args.src).with_suffix(".png")
        save_texture(to_image(load_pxg(args.src)), out, bleed=not args.no_bleed)
        print(out)

    elif args.cmd == "bleed":
        from aide.bleed import alpha_bleed

        out = Path(args.out) if args.out else Path(args.src)
        alpha_bleed(load_texture(args.src)).save(out)
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

    elif args.cmd == "block":
        from aide.blockrender import iso_block

        side = load_texture(args.side)
        top = load_texture(args.top) if args.top else side
        right = load_texture(args.right) if args.right else side
        iso_block(top, side, right, scale=args.scale).save(args.out)
        print(args.out)

    elif args.cmd == "lift":
        from aide.grid import parse_color
        from aide.lift import exposed_faces, lift, to_obj
        from aide.liftviewer import build_payloads, render_iso, viewer_html

        name = Path(args.src).stem
        vol = lift(args.src, mode=args.mode, thickness=args.thickness)
        faces = exposed_faces(vol)
        col = parse_color(args.color)[:3]
        made = []
        if not (args.obj or args.iso or args.html):  # sensible default outputs
            args.obj = str(Path(args.src).with_suffix(".obj"))
            args.iso = str(Path(args.src).with_suffix(".iso.png"))
        if args.obj:
            Path(args.obj).write_text(to_obj(faces, name)); made.append(args.obj)
        if args.iso:
            render_iso(faces, color=col).save(args.iso); made.append(args.iso)
        if args.html:
            payloads = build_payloads({name: (vol, args.mode)})
            html = viewer_html(payloads, {name: f"#{args.color.lstrip('#')}"})
            Path(args.html).write_text(html); made.append(args.html)
        print(f"{name}: {args.mode}, {vol.nx}x{vol.ny}x{vol.nz} voxels, {len(faces)} faces")
        for m in made:
            print(" ", m)

    elif args.cmd == "autotex":
        from aide.model import load_model
        from aide.autotex import autotexture, default_ramp

        tex, warns = autotexture(load_model(args.model), default_ramp(args.base),
                                 frame=not args.no_frame)
        save_texture(tex, args.out, bleed=False)
        print(args.out)
        for w in warns:
            print("  warning:", w, file=sys.stderr)

    elif args.cmd == "model":
        from aide.model import load_model
        from aide.modelrender import render_model
        from aide.autotex import autotexture, default_ramp

        model = load_model(args.model)
        imgs: dict = {}
        if args.single:
            imgs["__single__"] = load_texture(args.single)
        for pair in args.tex:
            key, path = pair.split("=", 1)
            imgs[key] = load_texture(path)
        if args.texdir:
            for key, ref in model.textures.items():
                path = model.resolve_texture("#" + key)
                if path and not path.startswith("#"):
                    rel = path.split(":", 1)[-1]  # namespace:block/foo -> block/foo
                    fp = Path(args.texdir) / f"{rel}.png"
                    if fp.exists():
                        imgs[path] = load_texture(fp)
        if not imgs:  # nothing supplied -> read shape, auto-texture, render
            tex, _ = autotexture(model, default_ramp(args.ramp))
            imgs["__single__"] = tex
        tints = {}
        for pair in args.tint:
            idx, hexv = pair.split("=", 1)
            from aide.grid import parse_color
            tints[int(idx)] = parse_color(hexv)
        render_model(model, imgs, scale=args.scale, tints=tints or None).save(args.out)
        print(args.out)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
