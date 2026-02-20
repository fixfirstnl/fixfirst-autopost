# fixfirst-autopost

Automated video uploader for TikTok, YouTube Shorts, and Instagram Reels – VPS pipeline for FixFirst content.

## Project Structure

```
fixfirst-autopost/
├── upload.py                   # Main CLI entry point
├── uploaders/
│   ├── __init__.py
│   ├── tiktok_uploader.py      # Selenium-based TikTok upload
│   ├── youtube_uploader.py     # YouTube Data API v3 upload
│   └── instagram_uploader.py   # instagrapi Instagram Reels upload
├── utils/
│   ├── __init__.py
│   ├── logger.py               # Dated rotating log files
│   └── manifest_parser.py      # Manifest loader + upload history tracker
├── config/
│   └── .env.example            # Template for environment variables
├── logs/                       # Auto-created log files (gitignored)
├── manifest.json.example       # Example batch manifest
├── requirements.txt
└── README.md
```

## Prerequisites

- Ubuntu 22.04+ VPS (or any Linux system)
- Python 3.11+
- Google Chrome (for TikTok Selenium uploader)
- A Google Cloud project with the YouTube Data API v3 enabled

---

## Setup

### 1. Clone & install Python dependencies

```bash
git clone https://github.com/fixfirstnl/fixfirst-autopost.git
cd fixfirst-autopost
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Install Google Chrome (Ubuntu)

```bash
wget -qO- https://dl.google.com/linux/linux_signing_key.pub \
  | sudo gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
  | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt-get update && sudo apt-get install -y google-chrome-stable
```

ChromeDriver is managed automatically by `webdriver-manager`.

### 3. Configure environment variables

```bash
cp config/.env.example .env
nano .env   # fill in your credentials
```

| Variable                     | Description                                           |
|------------------------------|-------------------------------------------------------|
| `TIKTOK_SESSION_ID`          | TikTok `sessionid` cookie value                       |
| `YOUTUBE_CLIENT_SECRET_FILE` | Path to your Google OAuth2 client-secret JSON         |
| `IG_USERNAME`                | Instagram username                                    |
| `IG_PASSWORD`                | Instagram password                                    |
| `VIDEO_DIR`                  | Base directory for video files (optional reference)   |
| `LOG_LEVEL`                  | Python log level (`DEBUG`, `INFO`, `WARNING`, …)      |

> **Security note:** Never commit `.env` to version control. It is already in `.gitignore`.

### 4. Set up YouTube OAuth2

1. Go to [Google Cloud Console](https://console.cloud.google.com/) → **APIs & Services** → **Credentials**.
2. Create an **OAuth 2.0 Client ID** (type: *Desktop app*).
3. Download the JSON as `client_secret.json` and place it in the project root (or update `YOUTUBE_CLIENT_SECRET_FILE` in `.env`).
4. The first run will open a browser to authorise access; subsequent runs reuse `youtube_token.json`.

### 5. Get your TikTok session ID

1. Open TikTok in a browser and log in.
2. Open DevTools → **Application** → **Cookies** → `https://www.tiktok.com`.
3. Copy the value of the `sessionid` cookie and set it as `TIKTOK_SESSION_ID` in `.env`.

---

## Creating a manifest

Copy and edit the example:

```bash
cp manifest.json.example manifest.json
```

Format:

```json
[
  {
    "video_path": "/home/fixfirst/videos/kraan-reparatie.mp4",
    "title": "Kraan repareren - Stap voor stap",
    "caption": "Zo repareer je een lekkende kraan! #diy #fixfirst",
    "hashtags": ["diy", "fixfirst", "klussentips"],
    "platforms": ["tiktok", "youtube", "instagram"]
  }
]
```

| Field            | Required | Description                                                      |
|------------------|----------|------------------------------------------------------------------|
| `video_path`     | ✅       | Absolute or relative path to the video file                      |
| `title`          | ✅       | Video title (used for YouTube; `#Shorts` added automatically)    |
| `caption`        | ✅       | Caption / description (used for TikTok & Instagram)              |
| `hashtags`       |          | List of hashtag strings **without** the `#` prefix               |
| `platforms`      |          | Restrict entry to specific platforms; omit to match CLI selection |
| `description`    |          | Long description (YouTube only)                                  |
| `privacy_status` |          | `public` (default), `private`, or `unlisted` (YouTube only)      |

---

## Usage

```bash
# Upload to a single platform
python upload.py --platform tiktok    --batch manifest.json
python upload.py --platform youtube   --batch manifest.json
python upload.py --platform instagram --batch manifest.json

# Upload to all platforms
python upload.py --all --batch manifest.json

# Dry-run (validate without uploading)
python upload.py --all --batch manifest.json --dry-run
```

### Flags

| Flag         | Description                                             |
|--------------|---------------------------------------------------------|
| `--platform` | Target platform (`tiktok`, `youtube`, `instagram`)      |
| `--all`      | Upload to all three platforms                           |
| `--batch`    | Path to the manifest JSON file (required)               |
| `--dry-run`  | Log what would happen without performing uploads        |

---

## Error handling & retries

- Each upload is attempted up to **3 times** with exponential back-off (2 s, 4 s, 8 s).
- Already-uploaded videos are **skipped** (tracked in `uploads_history.json`).
- A summary report is printed/logged after each batch:

```
=== Batch complete: 3 total | 2 success | 0 skipped | 1 failed ===
```

- Exit code `1` is returned if any upload failed.

---

## Logs

Log files are written to `logs/upload_YYYY-MM-DD.log` (one file per day).  
Set `LOG_LEVEL=DEBUG` in `.env` for verbose output.

---

## Running on a schedule (cron)

```cron
# Every day at 09:00
0 9 * * * cd /home/fixfirst/fixfirst-autopost && /home/fixfirst/fixfirst-autopost/.venv/bin/python upload.py --all --batch manifest.json >> /home/fixfirst/fixfirst-autopost/logs/cron.log 2>&1
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes
4. Open a pull request

---

## License

MIT
