#!/usr/bin/env python3
"""Validate a branded-reel subtitle timeline JSON without rendering media."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('timeline', type=Path)
    ap.add_argument('--fps', type=float)
    ap.add_argument('--assets', type=Path, help='Optional folder containing NN-subXX.png assets')
    ap.add_argument('--prefix', help='Required asset filename prefix such as 08')
    args = ap.parse_args()
    try:
        data = json.loads(args.timeline.read_text(encoding='utf-8-sig'))
    except Exception as exc:
        fail(f'cannot read timeline: {exc}')
    cues = data.get('cues') if isinstance(data, dict) else data
    if not isinstance(cues, list) or not cues:
        fail('timeline needs a nonempty cues list')
    fps = args.fps or (data.get('fps') if isinstance(data, dict) else None)
    duration = data.get('duration') if isinstance(data, dict) else None
    previous_end = -1.0
    for index, cue in enumerate(cues, 1):
        if not isinstance(cue, dict): fail(f'cue {index} is not an object')
        try: start, end = float(cue['start']), float(cue['end'])
        except (KeyError, TypeError, ValueError): fail(f'cue {index} needs numeric start/end')
        text = cue.get('text')
        if not isinstance(text, str) or not text.strip(): fail(f'cue {index} needs nonblank text')
        if start < 0 or end <= start: fail(f'cue {index} has invalid range {start}-{end}')
        if start < previous_end - 1e-6: fail(f'cue {index} overlaps prior cue')
        if duration is not None and end > float(duration) + 1e-6: fail(f'cue {index} exceeds timeline duration')
        if fps and round((end-start)*fps) < 1: fail(f'cue {index} is shorter than one frame')
        previous_end = end
        if args.assets and args.prefix:
            asset = args.assets / f'{args.prefix}-sub{index:02d}.png'
            if not asset.is_file(): fail(f'missing subtitle asset: {asset}')
    print(f'OK: {len(cues)} ordered, non-overlapping cues' + (f' at {fps:g} fps' if fps else ''))
if __name__ == '__main__': main()
