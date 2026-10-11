# Branded Interview Reels

Reusable skill for an **end-to-end** branded vertical reel from authorized interview/speech footage:

1. **Find footage** (找影片 / 找采访素材) — candidates + authorization, not piracy
2. **Select excerpt** — speaker, topic, start/end, single narrative line
3. **Crop / reframe** — 9:16-safe face plate
4. **Layout** — MOSI-style upper/lower bars, large title, brand colors
5. **Subtitles** — ASR draft → phrase timing → Chinese → validate
6. **Export + QA** — mp4, contact sheet, ffprobe, sha256 (no publish without separate OK)

The non-obvious quality failure mode remains: subtitle timing must change with the speaker's semantic phrases. A portable JSON timeline validator catches missing assets, invalid ranges, overlaps, and non-advancing cues before render.

## Install

Copy this folder into your skills / workflows directory, for example:

```powershell
Copy-Item -Recurse . "$env:USERPROFILE\.codex\skills\branded-interview-reels"
```

Or sync into the agent's workflow path used by Grok Bot / Codex.

Invoke when the task mentions 找影片, 找采访素材, 裁剪排版字幕, or branded interview reels.

## Scope

Workflow instructions + lightweight timing validator only. No source videos, brand binaries, credentials, or publish automation ship in this repo. Copyright / likeness / platform approval are **not** verified by the skill.

## Validate a subtitle timeline

```bash
python3 scripts/validate_subtitle_timeline.py path/to/timeline.json --fps 24 --assets path/to/assets --prefix 08
```

See `references/find-footage.md`, `references/layout-templates.md`, `references/subtitle-timing.md`, and `references/qa.md`.

## License

MIT. See [LICENSE](LICENSE).
