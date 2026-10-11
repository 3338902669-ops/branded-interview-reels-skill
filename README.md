# Branded Interview Reels

Reusable skill for an **end-to-end** branded vertical reel from authorized interview/speech footage:

1. **Find footage** (找影片 / 找采访素材) — candidates + authorization, not piracy
2. **Select excerpt** — speaker, topic, start/end, single narrative line
3. **Crop / reframe** — 9:16-safe face plate
4. **Layout** — MOSI-style upper/lower bars, large title, brand colors
5. **Subtitles** — ASR draft → phrase timing → Chinese → validate
6. **Export + QA** — mp4, contact sheet, ffprobe, sha256 (no publish without separate OK)

The non-obvious quality failure mode remains: subtitle timing must change with the speaker's semantic phrases. A portable JSON timeline validator catches missing assets, invalid ranges, overlaps, and non-advancing cues before render.

## Prerequisites

| Dependency | Required | Notes |
|------------|----------|-------|
| `ffmpeg` + `ffprobe` | **Yes** | Crop, probe, encode, contact-sheet frames |
| `python3` (≥3.9) | **Yes** | Validators + helpers |
| Pillow (`pip install pillow`) | **Yes** for layout/sheet helpers | `compose_template_b.py`, `make_contact_sheet.py` |
| CJK-capable font | Recommended | Noto Sans CJK / NotoSansSC-VF / 微软雅黑 — compositor falls back to default if missing |
| Local ASR (faster-whisper / whisper.cpp / whisper) | Optional | Subtitle **draft** only; timings must be listen-reviewed |

```bash
# Sanity
ffmpeg -version | head -1
ffprobe -version | head -1
python3 -c "from PIL import Image; print('pillow ok')"
```

## Install

Copy this folder into your skills / workflows directory, for example:

```powershell
Copy-Item -Recurse . "$env:USERPROFILE\.codex\skills\branded-interview-reels"
```

Or sync into the agent's workflow path used by Grok Bot / Codex.

Invoke when the task mentions 找影片, 找采访素材, 裁剪排版字幕, or branded interview reels.

## Dry-run: find-footage checklist (no download)

Use this when verifying Step A without caching media:

1. Write 3–8 search queries for the person/topic (see `references/find-footage.md`).
2. Fill a candidate table: title, URL/platform, channel, duration, why it fits, risk notes.
3. Run the **authorization checklist** on paper / in `source/auth-log.md` — mark `pending` for every row.
4. **Stop.** Do not download until the user/boss names an authorized URL or local path.
5. If nothing is authorized: record queries tried + nearest misses; do not invent footage.

## Helper scripts

```bash
# Subtitle timeline gate
python3 scripts/validate_subtitle_timeline.py path/to/timeline.json --fps 24 --assets path/to/assets --prefix 08

# Template B layout stub (1080x1920 png or short mp4)
python3 scripts/compose_template_b.py --plate work/plate.png --title '钩子' --name '姓名' --out work/layout_stub.png

# Contact sheet
python3 scripts/make_contact_sheet.py OUT.mp4 OUT-sheet.jpg --times 0.5,3.8,8.0,15.5
```

## Scope

Workflow instructions + lightweight helpers/validator only. No source videos, brand binaries, credentials, or publish automation ship in this repo. Copyright / likeness / platform approval are **not** verified by the skill.

See `references/find-footage.md`, `references/layout-templates.md`, `references/subtitle-timing.md`, and `references/qa.md`.

## License

MIT. See [LICENSE](LICENSE).
