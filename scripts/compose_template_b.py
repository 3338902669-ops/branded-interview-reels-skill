#!/usr/bin/env python3
"""Minimal MOSI Template B compositor: 1080x1920 frame or short mp4 stub.

Takes a mid-window plate (image or video), title/hook text, optional lower
name/topic, and paints upper/lower brand bars on a solid background.

Examples:
  python3 scripts/compose_template_b.py \\
    --plate work/plate_frame.png --title '离开斯坦福那天' \\
    --title2 '教授只说了一句话' --name '埃隆·马斯克' \\
    --topic 'Zip2 / PayPal 共同创始人' --out work/layout_stub.png

  python3 scripts/compose_template_b.py \\
    --plate work/plate.mp4 --title '钩子一行' --name '姓名' \\
    --topic '身份' --out work/layout_stub.mp4 --seconds 3
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
VW, VH = 1000, 540
VX, VY = (W - VW) // 2, 600
BORDER = 3
BLUE = (36, 132, 252)  # #2484FC
WHITE = (250, 251, 253)
MUTED = (140, 146, 158)
INK = (14, 16, 20)


def _font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("/workspace/fonts/NotoSansSC-VF.ttf"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/msyhbd.ttc"),
    ]
    for path in candidates:
        if path.is_file():
            try:
                if path.suffix.lower() == ".ttc":
                    return ImageFont.truetype(str(path), size=size, index=0)
                font = ImageFont.truetype(str(path), size=size)
                if hasattr(font, "set_variation_by_axes"):
                    try:
                        font.set_variation_by_axes([700 if bold else 400])
                    except Exception:
                        pass
                return font
            except Exception:
                continue
    return ImageFont.load_default()


def _parse_bg(s: str) -> tuple[int, int, int]:
    s = s.strip().lstrip("#")
    if len(s) == 6:
        return int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)
    raise SystemExit(f"bad --bg color: {s!r} (want #RRGGBB)")


def _load_plate(path: Path, at_s: float = 0.0) -> Image.Image:
    suffix = path.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".webp"}:
        return Image.open(path).convert("RGB")
    # video: grab one frame
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        out = Path(tmp.name)
    cmd = [
        "ffmpeg", "-v", "error", "-ss", str(at_s), "-i", str(path),
        "-frames:v", "1", "-y", str(out),
    ]
    subprocess.run(cmd, check=True)
    im = Image.open(out).convert("RGB")
    out.unlink(missing_ok=True)
    return im


def compose_frame(
    plate: Image.Image,
    *,
    bg: tuple[int, int, int],
    series: str,
    ep: str,
    title: str,
    title2: str,
    name: str,
    topic: str,
    subtitle: str,
) -> Image.Image:
    canvas = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(canvas)

    # Mid window plate
    fitted = plate.resize((VW, VH), Image.Resampling.LANCZOS)
    canvas.paste(fitted, (VX, VY))
    # Border
    draw.rectangle(
        [VX - BORDER, VY - BORDER, VX + VW + BORDER - 1, VY + VH + BORDER - 1],
        outline=BLUE, width=BORDER,
    )

    # Top: series + ep
    f_series = _font(36, bold=True)
    draw.text((48, 72), series, font=f_series, fill=WHITE)
    if ep:
        bb = draw.textbbox((0, 0), series, font=f_series)
        draw.text((48 + (bb[2] - bb[0]) + 16, 72), ep, font=_font(32), fill=BLUE)

    # Huge hooks
    f_title = _font(96, bold=True)
    y = 160
    if title:
        draw.text((48, y), title, font=f_title, fill=WHITE)
        y += 110
    if title2:
        # second line often brand-blue for emphasis
        draw.text((48, y), title2, font=f_title, fill=BLUE)

    # Subtitle under window
    if subtitle:
        f_sub = _font(42, bold=True)
        bb = draw.textbbox((0, 0), subtitle, font=f_sub)
        tw = bb[2] - bb[0]
        draw.text(((W - tw) // 2, VY + VH + 28), subtitle, font=f_sub, fill=WHITE)

    # Bottom nameplate
    f_name = _font(48, bold=True)
    f_topic = _font(34, bold=False)
    by = 1280
    if name:
        draw.text((48, by), name, font=f_name, fill=WHITE)
    if topic:
        draw.text((48, by + 64), topic, font=f_topic, fill=MUTED)

    # Thin brand accent line above bottom zone
    draw.rectangle([48, 1240, W - 48, 1244], fill=BLUE)
    return canvas


def _encode_stub_mp4(frame: Path, plate_video: Path | None, seconds: float, out: Path) -> None:
    """Hold the composed still for --seconds; mux plate audio if plate is video."""
    if plate_video and plate_video.suffix.lower() in {".mp4", ".mov", ".mkv", ".webm"}:
        # silent-ish stub: still image + trimmed plate audio (or silent)
        cmd = [
            "ffmpeg", "-v", "error", "-y",
            "-loop", "1", "-i", str(frame),
            "-i", str(plate_video),
            "-map", "0:v:0", "-map", "1:a:0?",
            "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-shortest", "-t", str(seconds),
            "-movflags", "+faststart", str(out),
        ]
    else:
        cmd = [
            "ffmpeg", "-v", "error", "-y",
            "-loop", "1", "-i", str(frame),
            "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
            "-t", str(seconds), "-movflags", "+faststart", str(out),
        ]
    subprocess.run(cmd, check=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--plate", type=Path, required=True, help="Mid-window image or video plate")
    ap.add_argument("--title", default="", help="Hook line 1 (large)")
    ap.add_argument("--title2", default="", help="Hook line 2 (large, brand blue)")
    ap.add_argument("--series", default="MOSI｜成长观察", help="Top series chip")
    ap.add_argument("--ep", default="", help="Episode label e.g. 01")
    ap.add_argument("--name", default="", help="Lower nameplate name")
    ap.add_argument("--topic", default="", help="Lower nameplate role/topic")
    ap.add_argument("--subtitle", default="", help="Optional one-line Chinese sub under window")
    ap.add_argument("--bg", default="#000000", help="Canvas background #RRGGBB")
    ap.add_argument("--plate-at", type=float, default=0.0, help="Seconds into plate video for still")
    ap.add_argument("--out", type=Path, required=True, help="Output .png/.jpg or .mp4 stub")
    ap.add_argument("--seconds", type=float, default=2.0, help="Duration when --out is .mp4")
    args = ap.parse_args()

    if not args.plate.is_file():
        raise SystemExit(f"missing plate: {args.plate}")

    bg = _parse_bg(args.bg)
    plate = _load_plate(args.plate, args.plate_at)
    frame = compose_frame(
        plate,
        bg=bg,
        series=args.series,
        ep=args.ep,
        title=args.title,
        title2=args.title2,
        name=args.name,
        topic=args.topic,
        subtitle=args.subtitle,
    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    suffix = args.out.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".webp"}:
        frame.save(args.out, quality=95)
        print(f"OK: wrote {args.out} ({W}x{H})")
        return
    if suffix in {".mp4", ".mov"}:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            still = Path(tmp.name)
        frame.save(still)
        try:
            plate_vid = args.plate if args.plate.suffix.lower() in {".mp4", ".mov", ".mkv", ".webm"} else None
            _encode_stub_mp4(still, plate_vid, args.seconds, args.out)
        finally:
            still.unlink(missing_ok=True)
        print(f"OK: wrote {args.out} ({W}x{H}, {args.seconds:g}s stub)")
        return
    raise SystemExit(f"unsupported --out suffix: {suffix}")


if __name__ == "__main__":
    main()
