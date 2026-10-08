---
name: branded-interview-reels
description: Create vertical branded short-form videos from authorized interview or speech footage, with readable Chinese subtitles, safe reframing, and a QA gate for subtitle timing. Use for source-footage re-edits, not AI-generated talking-head video.
---

# Branded Interview Reels

Turn an authorized interview, lecture, or speech excerpt into a branded 9:16 social video without making it look like a repost. Preserve the source speaker and usable original audio; make the surrounding composition, headline, text hierarchy, subtitle treatment, and end card clearly brand-owned.

## Before editing

1. Confirm the intended output route, duration, brand, language convention, and whether original burned-in captions, lower-thirds, and source identifiers must remain visible. Do not infer permission from a public URL.
2. Identify the exact usable excerpt before designing: speaker, topic, start/end, shot changes, logos, and areas that must remain unmasked.
3. Choose one brand-owned template with: a strong headline stage, a source-footage window, a subtitle safe zone, and a restrained brand/end-card area. Do not put a generic colored bar above and below unmodified source footage.
4. For Hong Kong-facing Chinese, use Traditional Chinese and retain conventional names/terms accurately. If copy is a translation/paraphrase, do not make it look like an exact quotation.

## Reframing and hierarchy

- Make the face complete at the crop boundary. Never create a cramped crop just to remove every source marker.
- Keep original captions in the footage window if requested. Position new subtitles so they do not cover them.
- Put one clear visual priority at a time: headline first, speaker second, subtitle third. Use large, high-contrast Chinese headline text; brand information must not compete with the hook.
- Use a single controlled grade across top, footage window, and lower band. If a gradient/grid is used, it must support contrast rather than become visual noise.
- Use source identifiers honestly. A source name or watermark is not an endorsement, a license, or a substitute for a usage-right check.

## Subtitle timing is a release gate

Subtitle animation must follow speech meaning, not evenly divided time blocks. A subtitle that stays after the speaker has begun the next thought is a defect; a subtitle layer that does not change is a defect.

1. Generate word-level timestamps from the **same source audio segment** used in the final edit (local ASR is acceptable as a draft).
2. Manually review each phrase boundary against audible speech. Do not trust ASR punctuation or automatic translation as final timing.
3. Translate/adapt phrase by phrase. Each onscreen Chinese line must map to a specific audible source phrase.
4. Set subtitle in-point 0–150 ms before audible phrase onset; set out-point at the phrase end and never later than the next phrase onset. Preserve intentional pauses instead of holding stale text.
5. Build a timeline manifest rather than hard-coding timing in a renderer. Every entry needs `start`, `end`, `text`, and an optional source transcript reference.
6. Assert at render time that each referenced subtitle asset exists and each cue has positive duration. Fail the build for missing assets, overlaps, stale holds, or a cue list that is not advancing.
7. Render a timestamp/contact-sheet review of every cue transition. Inspect it at full resolution; do not use only a static cover image.

Use [references/subtitle-timing.md](references/subtitle-timing.md) for the timing data contract and validation rules. Use [references/qa.md](references/qa.md) before marking a local deliverable ready.

## Production and delivery

- Prefer deterministic local tools: FFmpeg for decode/crop/encode and a renderer that consumes one explicit subtitle timeline manifest.
- Preserve audio sync through a fixed frame rate. Mux audio only after confirming output duration and frame count.
- Keep source, assets, final render, and delivery folder separate. Do not overwrite an approved version; increment the version.
- Produce a contact sheet, stream metadata, full decode result, and SHA-256 per final file. These prove file integrity, not creative approval or legal clearance.
- Do not upload, post, publish, or send externally without separately explicit authorization.

## Boundaries

- This skill does not verify copyright, likeness/publicity rights, factual claims, or platform policy. Record authorization as a user claim unless documentary proof was actually checked.
- Keep source logos/watermarks only where requested or where removal would be misleading; do not claim they were removed if a crop merely hides part of them.
- For the reusable timing validator, see `scripts/validate_subtitle_timeline.py`.
