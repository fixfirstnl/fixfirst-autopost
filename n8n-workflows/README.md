# FixFirst Viral Machine - n8n Workflows

**Zero-Credit Mode**: Deze workflows draien 100% op je VPS, geen BrowserOS credits.

**Last updated:** 2026-03-25

---

## Workflows

### 1. Trend Discovery (`trend-discovery.json`)
´ Trigger: Cron 00:08 daily
Ұ Purpose: Zoek naar virale trends on TikTok/YouTube
ҩ Tools: Kimi (VPS), 'SQLite

М Output: Top 5 trending keywords in database

### 2. Script Generation (`script-generation.json`)
¹Trigger: Manual of Tuesday 18:00
Ұ Purpose: Genereer 30-45s captions captions
Ҹ Tools: Kimi (VPS), SQLite
У Output: Script met 1.5s hook, captions voor alle platformen
### 3. Video Publishing (`video-publishing.json`)
ùTrigger: Webhook (approval)
Ұ Purpose: Publiseer naar alle sociale media
Ҹ Tools: ElevenLabs, Ayrshare
У Output: Gepubliseerd content op alle platformen

