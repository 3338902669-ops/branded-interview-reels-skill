#!/usr/bin/env python3
"""Build a labeled contact sheet from video timestamps.

Example:
  python3 scripts/make_contact_sheet.py OUT.mp4 OUT-sheet.jpg \\
    --times 0.5,3.8,8.0,15.5,23.0,34.0
"""
from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def _font(size: int = 28) -> ImageFont.ImageFont:
    for path in (
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"),
        Path("/workspace/fonts/NotoSansSC-VF.ttf"),
        Path("C:/Windows/Fonts/msyh.ttc"),
    ):
        if path.is_file():
            try:
                if path.suffix.lower() == ".ttc":
                    return ImageFont.truetype(str(path), size=size, index=0)
                return ImageFont.truetype(str(path), size=size)
            except Exception:
                continue
    return ImageFont.load_default()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("video", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--times", required=True, help="Comma-separated seconds, e.g. 0.5,3.8,8.0")
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--thumb-w", type=int, default=360)
    ap.add_argument("--thumb-h", type=int, default=640)
    args = ap.parse_args()

    if not args.video.is_file():
        raise SystemExit(f"missing video: {args.video}")
    times = [float(x.strip()) for x in args.times.split(",") if x.strip()]
    if not times:
        raise SystemExit("need at least one timestamp in --times")

    cols = max(1, args.cols)
    w, h = args.thumb_w, args.thumb_h
    rows = (len(times) + cols - 1) // cols
    pad = 16
    sheet = Image.new(
        "RGB",
        (cols * w + (cols + 1) * pad, rows * (h + 50) + pad),
        (230, 232, 236),
    )
    draw = ImageDraw.Draw(sheet)
    font = _font(28)

    with tempfile.TemporaryDirectory() as td:
        tdir = Path(td)
        for i, t in enumerate(times):
            frame = tdir / f"f{i:02d}.png"
            subprocess.run(
                ["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(args.video),
                 "-frames:v", "1", "-y", str(frame)],
                check=True,
            )
            im = Image.open(frame).convert("RGB").resize((w, h), Image.Resampling.LANCZOS)
            x = pad + (i % cols) * (w + pad)
            y = pad + (i // cols) * (h + 50)
            sheet.paste(im, (x, y))
            draw.text((x, y + h + 6), f"{t:.1f}s", font=font, fill=(20, 20, 20))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.out, quality=90)
    print(f"OK: {args.out} size={sheet.size} frames={len(times)}")


if __name__ == "__main__":
    main()
