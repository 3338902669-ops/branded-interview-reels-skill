# Find footage（找影片 / 找采访素材）

## What "find" means

| Allowed | Not allowed |
|---------|-------------|
| Search public catalogs; list candidate URLs + titles | Pirating, DRM strip, paywall bypass |
| Ask user/boss which candidates are authorized | Treating a public URL as automatic license |
| Download/cache **after** explicit OK into project `source/` | Scraping private WeChat/Drive media without permission |
| Use files the user already placed on disk / Drive | Claiming "found" when you only edited a given file and never searched |

Boss complaint to avoid: *AI cannot find films via the current skill* — because the old skill started at "edit given footage." Step A is mandatory when no usable local source is named.

---

## Decision tree (no local file yet)

```
Start: user asks for a branded interview reel
│
├─ User/boss already gave a local path or Drive file?
│    └─ YES → probe it, record sha256, skip search (still run authorization checklist)
│
├─ User/boss gave a URL only?
│    └─ Run authorization checklist → if OK, download/cache → probe
│
├─ Only a person/topic ("马斯克访谈", "CZ谈教育")?
│    └─ Search platforms below → present candidate table → WAIT for authorize
│         ├─ Authorized → download/cache → continue pipeline B
│         └─ Denied / unclear → STOP; do not invent footage or use random reposts
│
└─ Search returns nothing usable?
     └─ STOP with: queries tried, platforms tried, nearest misses.
        Ask for a link, a Drive path, or a different person/topic.
```

Never silently proceed to layout/subtitles without a real authorized media file.

---

## Search queries (patterns)

Build 3–8 queries per person/topic. Prefer **primary interviews** over highlight reels.

Examples:

- `"{姓名}" 专访` / `"{姓名}" 访谈` / `"{Name}" interview`
- `"{姓名}" 演讲` / `"{Name}" keynote` / `"{Name}" commencement`
- `"{姓名}" 创业` / `退学` / `成长` (only if growth-line is the brief)
- `"{姓名}" site:youtube.com` / B站：`"{姓名}" 采访`
- Channel-first: known long-form hosts, university channels, official corp channels
- Exclude (usually): `全集电影`, `抢先版`, `生肉搬运`, reaction-only, AI voiceover clones

Record for each hit: title, URL, platform, channel, duration, date, language, why it fits the brief, risk notes (repost? watermark? music bed?).

---

## Platform notes

### 视频号 (WeChat Channels)

- Discovery is often via WeChat search / shares in work chats — not a clean public search API.
- If the boss **sent a 视频号 link or video in WeChat**, treat that as the candidate seed: ask to confirm authorization and obtain a local export (user saves → uploads to Drive/box, or points to an existing cache).
- Do not claim you "watched 视频号" unless you actually have playable local media or an opened share the user provided.
- Metadata to capture: account name, share timestamp (Asia/Shanghai), topic, approximate duration.

### YouTube

- Search: interview / podcast / talk + person name; prefer official or first-party uploads.
- Note: `youtube.com/watch?v=…` or `youtu.be/…`, channel, duration, license/Description rights language if any.
- Download **only** after authorization, using whatever sanctioned downloader the environment already allows for that user. If download tools are blocked or unavailable, stop and ask the user to place the file in `source/`.

### B站 (bilibili)

- Search: `专访` / `访谈` / `演讲` + name; prefer UP 主 original or authorized reposts with clear source credit.
- Capture BV/av id, UP name, duration, whether the upload is a cut of a longer talk.
- Same rule: authorize → then cache; else ask user to supply the file.

### Other

- Official site / press kits / conference VOD: often clearest rights path — still need user/boss OK.
- Douyin/快手: usable for short bites; watch for heavy platform UI (harder clean crop). Prefer longer YouTube/B站 masters when the brief is interview-line.

Cross-skill downloaders (account / B站 / 抖音) may exist in the agent's workflow library — use them only as **mechanics after authorization**, never as a substitute for the checklist.

---

## Metadata to capture (per candidate)

```json
{
  "title": "",
  "url": "",
  "platform": "youtube|bilibili|shipinhao|local|other",
  "channel_or_account": "",
  "duration_s": null,
  "published_or_shared_at": "",
  "language": "",
  "speaker": "",
  "topic_fit": "",
  "authorization": "pending|user_claimed|documented",
  "local_path": null,
  "sha256": null,
  "notes": ""
}
```

Present a markdown table to the user/boss before downloading more than a tiny preview frame (if even that is allowed).

---

## Authorization checklist (before cache)

- [ ] User/boss **named** this URL or file as OK to use for this brand edit.
- [ ] Intended output route known (视频号 / 小红书 / internal only).
- [ ] Likeness / interview context acceptable for the brand (user claim recorded).
- [ ] Not substituting a random repost when a primary was requested.
- [ ] If music-bed heavy or third-party commentary dominates, flag and prefer a cleaner master.
- [ ] Record: who authorized, when (Asia/Shanghai), and the exact URL/path.

Public availability ≠ permission. Record authorization as a user claim unless proof was checked.

---

## Download / cache paths

Suggested layout (adapt to project root):

```
project/
  source/
    candidates.md          # search table + decisions
    auth-log.md            # who/when/what authorized
    YYYYMMDD_slug/
      original.mp4         # or .mkv
      original.ffprobe.json
      original.sha256
      poster.jpg           # optional
  work/                    # derived plates / wav only
```

Commands after a file lands:

```bash
ffprobe -v error -show_format -show_streams -of json source/.../original.mp4 \
  > source/.../original.ffprobe.json
sha256sum source/.../original.mp4 | tee source/.../original.sha256
```

Do not overwrite an approved original; add `..._v2` or a new dated folder.

---

## When the boss already sent footage on WeChat

1. Locate the share (group/private) — note sender, time UTC+8, caption.
2. If local export exists on the user's machine or prior box cache, use that path.
3. If missing ("we missed it"), ask the user to re-export/forward the media into an accessible folder — do not stall forever inventing alternate illegal copies.
4. Once playable locally → resume at pipeline **B**.
