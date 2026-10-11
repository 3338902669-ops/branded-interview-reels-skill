# Layout templates (MOSI-style / Template B)

Brand-owned chrome turns authorized interview plates into a product — not a repost. Prefer **one** template per series and 1:1 imitate settled refs.

## Canvas

| Spec | Value |
|------|-------|
| Size | **1080×1920** (9:16) |
| Base | Black `#0E1014`–`#000` |
| Accent | MOSI brand blue **`#2484FC`** (RGB 36,132,252); black-only OK if brief prefers |
| Secondary | Soft cyan/white for hierarchy only — do not rainbow-noise the frame |
| Safe | Keep critical title clear of notch / Dynamic Island; margins ≥24–40 px |

## Template B — 上下栏（interview / 观察室）

Settled pattern from MOSI-CZ「AI成长观察」上下版式 + black-bar follow-ups (Susie: 1:1 imitate; boss: title must be large; blue = brand color).

```
┌─────────────────────────────┐  ← Top MOSI bar (~y 0–560)
│  MOSI｜成长观察   ep 01     │     logo + series + episode
│  超大钩子行 1（白/品牌蓝）   │     hook ≈ dominant; multi-color OK
│  超大钩子行 2               │     title size > background color
│  斜向副钩 / 短说明          │     optional slant chip
├─────────────────────────────┤
│     ┌─────────────────┐     │  ← Mid window (e.g. 1000×540 at y≈600)
│     │  interview plate │     │     light blue border ~3px
│     │  face-safe crop  │     │     no foreign app UI chrome
│     └─────────────────┘     │
│        中文书面语字幕一行      │  ← Subtitle safe zone under window
├─────────────────────────────┤  ← Bottom MOSI bar
│  姓名 · 身份                 │
│  一句主题                    │
│  (optional) 短弹出要点 1–4   │  ← growth-line only; not with long film expo
└─────────────────────────────┘
```

### Hierarchy (one priority at a time)

1. **Hook / title** — largest type; readable at phone-arm length.
2. **Speaker face** — complete in the mid window.
3. **Subtitle** — high contrast, one phrase; does not cover required burned-in source captions.
4. **Brand / nameplate** — restrained; never competes with the hook.

### Do / Don't

| Do | Don't |
|----|-------|
| Own top+bottom bars + cropped interview only | Full-frame source with thin tinted letterbox ("一看就是搬的") |
| Huge title; brand blue accents | Tiny title on a fancy gradient |
| Single narrative line | Filmography + growth timeline + long opinion dump same screen |
| Hand-edited 书面语 hooks | Stock AI filler / dense PPT walls |
| Progress ticks / short pops if growth-line | Empty pre-drawn slots that never animate |

## Narrative modes (pick one)

- **A — 集中影片 (interview line):** mid window = speech; subs track speech; bottom = name/role/theme. No long résumé ladder.
- **B — 集中成长经历 (growth line):** photo/nodes or short pops "一个一个跳出来"; if a video window exists it is secondary. Do not also run dense interview exposition + long subs.

Boss reject pattern: mixing film narrative and growth résumé until "看不懂."

## Type & copy

- Chinese headline: large, high contrast; 2 short lines beat 1 paragraph.
- Subtitles: 书面语; ≈≤14 chars/line when possible; map 1:1 to audible phrases ([subtitle-timing.md](subtitle-timing.md)).
- Hong Kong-facing: Traditional Chinese + accurate proper names when that is the brief.
- Series chip examples: `MOSI｜成长观察`, `MOSI｜观察室` — match the series the boss named.

## Color tokens

| Token | Hex | Use |
|-------|-----|-----|
| Brand blue | `#2484FC` | Hook emphasis, border, ticks |
| Ink | `#0E1014` | Text on light chips |
| White | `#FAFBFD` | Primary hook on black |
| Muted | `#8C929E` | Meta / secondary |
| Slant chip bg | `#F5F6F8` | Optional sub-hook plate |

## Implementation notes (tool-agnostic)

- Compose bars in any renderer (Pillow/HTML/AE); feed the **cropped plate** into the mid window via FFmpeg or frame pipe.
- Keep fps fixed (24 or 30) from plate through mux; loudnorm audio after concat if segments are joined.
- End card optional; still no publish without separate authorization.
- When a reference contact sheet or boss template frames folder exists for the series, match bar heights and title scale 1:1 before inventing a new look.

## QA glances for layout

- [ ] Hook readable in first 1–2 seconds
- [ ] Face not clipped; window border consistent
- [ ] Subtitle clear of face and of required source captions
- [ ] Top/bottom clearly brand-owned (not source app UI)
- [ ] Only one narrative line on screen
