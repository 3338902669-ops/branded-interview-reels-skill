# Local QA checklist

## Before edit (footage gate)

- [ ] Candidates were searched or a user-supplied path/URL was recorded (找影片 step done — not skipped).
- [ ] Authorization checklist completed for the chosen source (user/boss claim logged).
- [ ] Local file probed (`ffprobe`) and hashed (`sha256`) under `source/`.

## Before render

- [ ] The source clip and exact excerpt have been identified (speaker, topic, start/end).
- [ ] One narrative line chosen (interview **or** growth — not mixed).
- [ ] Crop keeps the speaker's face complete and avoids unintended source UI where feasible.
- [ ] Headline, footage window, subtitle zone, and brand zone have a deliberate hierarchy (Template B / brief).
- [ ] Subtitle timeline was built from the final source audio timeline, not guessed equal intervals.
- [ ] Every subtitle line was listened to against the source language.

## After render

- [ ] All cue transitions were reviewed at full resolution, including the first, middle, and final spoken phrase.
- [ ] No subtitle remains through the start of a following thought.
- [ ] Subtitle assets visibly change when timeline entries change.
- [ ] Original burned-in captions and required source labels remain unobscured.
- [ ] `ffprobe` reports expected dimensions, rate, duration, audio, and frame count.
- [ ] `ffmpeg -v error -i <output> -f null -` returns exit code 0.
- [ ] Final media hashes and a contact sheet are saved with the delivery.
- [ ] No upload/publish/send was performed without separately explicit authorization.

These checks are local production checks. They are not an independent visual acceptance, a source-rights review, or publication approval.
