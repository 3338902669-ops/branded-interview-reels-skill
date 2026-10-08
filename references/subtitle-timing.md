# Subtitle timing contract

Store one timeline JSON per edit. It is the source of truth for subtitle changes, not an incidental list inside a renderer.

```json
{
  "fps": 24,
  "duration": 44.0,
  "cues": [
    {
      "start": 5.20,
      "end": 12.82,
      "text": "減息應該支持經濟，但一次未必夠",
      "source": "en 5.20-12.82"
    }
  ]
}
```

## Rules

- `start` and `end` are seconds on the source/final-edit timeline before any end card.
- A cue has `end > start`, nonblank `text`, and optional `source` evidence.
- Cues must be ordered and must not overlap. Gaps are allowed for silence, a shot change, or deliberate no-subtitle moments.
- A cue starts no more than 150 ms before its mapped spoken phrase unless a documented creative exception applies.
- A cue ends at its phrase end and no later than the following phrase start. Never keep old text on screen while a new semantic phrase is already audible.
- Reused images are allowed only when their timing changes in the manifest; changing a PNG name does not prove an animated subtitle track.

## Validation

Run:

```powershell
py scripts/validate_subtitle_timeline.py timeline.json --fps 24 --assets assets
```

The script validates ordering, duration, and optional numbered `NN-subXX.png` assets. It does not assess spoken-language accuracy; that requires listening review.
