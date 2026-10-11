---
name: branded-interview-reels
description: >-
  End-to-end branded vertical interview/speech reels: find authorized footage
  (找影片/找采访素材), select excerpts, 9:16 face crop, MOSI-style layout bars,
  Chinese subtitles with timing QA, export + contact sheet + sha256. Use when
  the task is 找影片, 找采访素材, 裁剪排版字幕, 视频号/小红书人物观察片, or
  re-editing authorized interview/speech source — not AI talking-head generation.
---

# Branded Interview Reels

Turn an **authorized** interview, lecture, or speech into a branded 9:16 social video. An agent following **only this skill** must be able to run the full pipeline — including **finding** candidate footage — not only edit a file the user already handed over.

Preserve the source speaker and usable original audio. Make composition, headline, hierarchy, subtitles, and end card brand-owned. Do not make it look like a raw repost.

## Pipeline overview (do in order)

| Step | Goal | Gate before next |
|------|------|------------------|
| **A. Find footage** | Candidate URLs + local paths the user/boss authorize | Authorization checklist signed off; at least one usable local file **or** explicit stop |
| **B. Select excerpt** | Speaker, topic, start/end, narrative line | One narrative line chosen (film **or** growth — never mixed) |
| **C. Crop / reframe** | Face-safe plate for the mid window | Face complete; source UI cropped out where feasible |
| **D. Layout / brand** | Upper/lower bars, large title, brand colors | Hierarchy: hook → speaker → subtitle |
| **E. Subtitles** | ASR → phrase timing → Chinese lines → validate | Timeline JSON passes validator + listen review |
| **F. Export + QA** | mp4 + contact sheet + ffprobe + sha256 | QA checklist green; **no publish** without separate OK |

Details for A → [references/find-footage.md](references/find-footage.md).  
Details for D → [references/layout-templates.md](references/layout-templates.md).  
Subtitle contract → [references/subtitle-timing.md](references/subtitle-timing.md).  
Release gate → [references/qa.md](references/qa.md).

---

## A) Find footage（找影片 / 找采访素材）

**Meaning of "find":** gather **candidate URLs and/or local files** that the user or boss can authorize — then download/cache only after clearance. It does **not** mean pirate, strip DRM, bypass paywalls, or scrape private chats for media without permission.

1. Clarify target: person, topic, language, platform preference (视频号 / YouTube / B站 / other), max duration, and whether audio must be original interview speech.
2. Search and list **candidates** (title, URL, platform, duration, upload/channel, why relevant). Prefer primary interviews over reaction/repost cuts.
3. Capture metadata for each candidate (see find-footage.md). Present a short table; ask which ones are authorized to use locally.
4. Run the **authorization checklist** before any download into the project cache.
5. If no local file yet, follow the decision tree in find-footage.md (stop vs wait vs use provided path).
6. After OK: download/cache under a project `source/` tree; record sha256 and probe JSON beside the file. Never overwrite an approved source — version it.

Platform search notes, query patterns, cache paths, and the no-local-file tree: **[references/find-footage.md](references/find-footage.md)**.

---

## B) Select excerpt

Before designing chrome:

1. Identify **speaker**, **topic**, and exact **start/end** (source timeline seconds). Prefer one continuous thought arc (≈20–90s for interview-line cuts).
2. Choose **one narrative line** and stick to it:
   - **Film / interview line**: original speech slices only + short on-screen hooks.
   - **Growth / résumé line**: timeline pops + photo/nodes — do **not** also stack long interview exposition.
   Mixing both on one screen is a known reject pattern.
3. Note shot changes, burned-in captions, logos, and areas that must stay unmasked.
4. Write an edit list: `SEGS=[(start,end), ...]` on the **source** clock, plus optional mild zoom per segment.
5. Confirm language convention (e.g. Hong Kong-facing → Traditional Chinese; Mainland 视频号 → follow brand brief). If copy is paraphrase, do not present it as a verbatim quote.

---

## C) Crop / reframe (9:16-safe face plate)

Goal: a clean mid-window plate of the speaker — face complete at the crop edge — that drops into the brand template. Never create a cramped crop just to erase every source marker.

Concrete FFmpeg pattern (adjust `w:h:x:y` after inspecting frames):

```bash
# Inspect
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,duration \
  -of json SOURCE.mp4 > SOURCE.ffprobe.json

# Sample frames around the excerpt for face framing — open this before locking crop
ffmpeg -v error -ss START -i SOURCE.mp4 -frames:v 1 -y /tmp/crop_check.png

# Extract a face-favoring plate (crop then scale into template mid-window 1000x540)
ffmpeg -v error -ss START -to END -i SOURCE.mp4 \
  -vf "crop=W:H:X:Y,hqdn3d=1.5:1.5:3:3,scale=1000:540:flags=lanczos,setsar=1" \
  -c:a copy -y work/plate.mp4
```

### Numeric starting points (always verify on `crop_check.png`)

Template mid-window is **1000×540**. Pick a source crop with the **same aspect (~16:9)** then let `scale=1000:540` fit it.

| Source size | Starting `crop=W:H:X:Y` | Intent |
|-------------|-------------------------|--------|
| **1920×1080** landscape interview | `crop=1000:540:460:200` | ~center face; X=(1920−1000)/2≈460, Y≈200 leaves headroom |
| **1920×1080**, face a bit left | `crop=1000:540:360:180` | nudge X down; re-check chin/forehead |
| **1920×1080**, tighter punch-in (mild zoom) | `crop=934:504:493:220` | ≈1.07× tighter; keep face inside |
| **1280×720** | `crop=1000:540:140:90` | same window math scaled to 720p |
| **1080×1920** already vertical | `crop=1000:540:40:600` | take mid band; adjust Y to eyes |

**How to estimate after `crop_check.png`:**

1. Note face center `(fx, fy)` in source pixels (eye midpoint is enough).
2. Choose `W,H` with `W/H ≈ 1000/540` (e.g. 1000×540 on 1080p).
3. `X ≈ fx - W/2`, `Y ≈ fy - H/2.5` (slightly more room above the head than below).
4. Clamp: `0 ≤ X ≤ src_w−W`, `0 ≤ Y ≤ src_h−H`.
5. Re-export `crop_check` **after** crop (or render one plate frame) and confirm eyes/forehead/chin are inside — **do not ship the table values blindly**.

Rules:

- Keep eyes/forehead/chin inside the crop; leave headroom.
- Prefer center-weighted face; nudge `x,y` per shot if the speaker drifts.
- If original burned-in captions must remain visible, crop so they stay inside the footage window and place **new** subtitles below that window.
- Mild per-segment zoom (`z≈1.0–1.07`) is OK for pacing; do not punch in so hard the face clips.
- Source identifiers: keep honestly when requested; a watermark is not a license.

---

## D) Layout / brand template

Use one brand-owned template with four zones: **headline stage**, **footage window**, **subtitle safe zone**, **brand / nameplate / end card**. Do **not** slap generic colored bars on unmodified full-frame source.

Default MOSI-style **Template B** (上下栏) — see **[references/layout-templates.md](references/layout-templates.md)**:

- Canvas **1080×1920**, black base, accent brand blue `#2484FC` (or black-only if brief says so).
- **Top bar**: series label (e.g. `MOSI｜成长观察` + ep) + **huge** multi-color hook (title size is the product — not the background color).
- **Mid**: bordered landscape-ish interview window; no foreign platform UI chrome.
- **Subs**: one clean Chinese line **under** the window.
- **Bottom bar**: name + role + one theme line; optional short popping list for growth-line cuts only.
- Avoid iPhone Dynamic Island / notch collision for critical text.
- Hand-edit hooks; do not ship stock AI filler copy.

### Minimal compositor (shipped)

Use `scripts/compose_template_b.py` to drop a plate into Template B and emit a **1080×1920** PNG or a short MP4 stub (layout proof before a full timed render):

```bash
# Still from a plate image
python3 scripts/compose_template_b.py \
  --plate work/plate_frame.png \
  --bg '#000000' \
  --series 'MOSI｜成长观察' --ep '01' \
  --title '离开斯坦福那天' --title2 '教授只说了一句话' \
  --name '埃隆·马斯克' --topic 'Zip2 / PayPal 共同创始人' \
  --subtitle '我在斯坦福办了休学' \
  --out work/layout_stub.png

# Short mp4 stub from plate video (holds composed still; optional plate audio)
python3 scripts/compose_template_b.py \
  --plate work/plate.mp4 --plate-at 0.5 \
  --title '钩子一行' --name '姓名' --topic '身份' \
  --out work/layout_stub.mp4 --seconds 3
```

Full motion + per-cue subtitle animation can still use a project renderer; this script is the **minimum layout entry** so step D is not invent-your-own.

---

## E) Subtitles (release gate)

Subtitle animation must follow speech **meaning**, not equal time slices. A line that stays after the next thought starts is a defect; a layer that never changes is a defect.

1. Extract the **same** audio used in the final edit:

```bash
ffmpeg -v error -i work/edit_audio.wav -ac 1 -ar 16000 -y work/asr.wav
# or trim from source:
ffmpeg -v error -ss START -to END -i SOURCE.mp4 -vn -ac 1 -ar 16000 -y work/asr.wav
```

2. Run **local ASR** for a word-level draft (faster-whisper / whisper.cpp / other local model — whatever is installed). Treat output as draft only.
3. Manually review each phrase boundary against audible speech. Do not trust ASR punctuation or auto-translation as final timing.
4. Translate/adapt phrase by phrase into on-screen Chinese (≤~14 chars/line when possible; 书面语 per brand).
5. Timing: in-point 0–150 ms before phrase onset; out-point at phrase end and **never** later than next phrase onset. Preserve intentional pauses.
6. Write a timeline JSON (`start`, `end`, `text`, optional `source`). Validate:

```bash
python3 scripts/validate_subtitle_timeline.py work/timeline.json --fps 30 --assets work/subs --prefix 01
```

7. Render a contact-sheet / timestamp review of every cue transition at full resolution.

Full contract: [references/subtitle-timing.md](references/subtitle-timing.md).

---

## F) Export + QA

Prefer deterministic local tools: FFmpeg for decode/crop/encode; a renderer that consumes one explicit subtitle timeline. For a layout proof before full timing, re-run `scripts/compose_template_b.py` from step D.

```bash
# Stream facts
ffprobe -v error -show_format -show_streams -of json OUT.mp4 > OUT.ffprobe.json

# Full decode sanity
ffmpeg -v error -i OUT.mp4 -f null - ; echo exit:$?

# Contact sheet (shipped helper)
python3 scripts/make_contact_sheet.py OUT.mp4 OUT-sheet.jpg \
  --times 0.5,3.8,8.0,15.5,23.0,34.0

# Equivalent pure-ffmpeg tile (optional; unlabeled)
# ffmpeg -v error -i OUT.mp4 -vf "select='eq(n,0)+eq(n,90)',scale=360:640,tile=3x2" -frames:v 1 -y OUT-sheet.jpg

# Integrity
sha256sum OUT.mp4 OUT-sheet.jpg | tee OUT.sha256
```

Delivery folder layout (keep separate; never overwrite approved):

```
project/
  source/          # authorized originals + .ffprobe.json + .sha256
  work/            # plates, wav, timeline.json, sub PNGs
  deliver/vNN/     # final mp4, sheet, probe, sha256, notes
```

Complete [references/qa.md](references/qa.md) before calling a local cut "ready".  
**Do not** upload, post, publish, or send externally without separately explicit authorization.

---

## Boundaries

- This skill does not verify copyright, likeness/publicity rights, factual claims, or platform policy. Record authorization as a **user/boss claim** unless documentary proof was actually checked.
- "Find footage" stops at candidates + authorized local cache. No piracy, no credential stuffing, no undocumented third-party bypass.
- Keep source logos/watermarks only where requested or where removal would be misleading.
- Timing validator: `scripts/validate_subtitle_timeline.py`.
- Layout stub: `scripts/compose_template_b.py`. Contact sheet: `scripts/make_contact_sheet.py`.
