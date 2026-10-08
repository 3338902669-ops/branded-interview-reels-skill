# Branded Interview Reels

Reusable Codex skill for editing authorized interview or speech source footage into branded vertical social reels.

It focuses on the non-obvious failure mode that breaks perceived quality: subtitle timing must change with the source speaker's semantic phrases. It ships a portable JSON timeline validator that catches missing assets, invalid ranges, overlaps, and non-advancing subtitle cues before render.

## Install

Copy this folder into your Codex skills directory, for example:

```powershell
Copy-Item -Recurse . "$env:USERPROFILE\.codex\skills\branded-interview-reels"
```

Then invoke `$branded-interview-reels` when editing an authorized source-footage reel.

## Scope

This repository contains workflow instructions and a lightweight timing validator only. It contains no source videos, brand assets, credentials, third-party footage, or publish automation. It does not verify copyright, likeness/publicity rights, factual claims, or platform approval.

## Validate a subtitle timeline

```powershell
py scripts\validate_subtitle_timeline.py path\to\timeline.json --fps 24 --assets path\to\assets --prefix 08
```

See `references/subtitle-timing.md` for the JSON contract and `references/qa.md` for the local delivery checklist.

## License

MIT. See [LICENSE](LICENSE).
