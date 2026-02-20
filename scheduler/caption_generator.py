#!/usr/bin/env python3
"""Generate platform-specific captions from video scripts in a manifest.

Supported platforms
-------------------
- instagram  : longer caption + separate first-comment hashtag block
- tiktok     : short hook (≤150 chars) + inline hashtags
- youtube    : SEO title + description + tags

Output formats: csv, json

Usage
-----
python scheduler/caption_generator.py \\
    --script-dir scripts/video_shorts \\
    --platform instagram \\
    --output-format csv \\
    --output output/captions_instagram.csv

python scheduler/caption_generator.py \\
    --script-dir scripts/video_shorts \\
    --platform youtube \\
    --output-format json \\
    --output output/captions_youtube.json
"""

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SCRIPT_DIR = REPO_ROOT / "scripts" / "video_shorts"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "output"
STRATEGY_FILE = Path(__file__).resolve().parent / "posting_strategy.json"

SUPPORTED_PLATFORMS = ("instagram", "tiktok", "youtube")
SUPPORTED_FORMATS = ("csv", "json")

# ---------------------------------------------------------------------------
# Caption generation helpers
# ---------------------------------------------------------------------------

def _load_strategy() -> dict:
    if STRATEGY_FILE.exists():
        with open(STRATEGY_FILE, encoding="utf-8") as fh:
            return json.load(fh)
    return {}


def _hashtag_string(tags: list[str], prefix: bool = True) -> str:
    """Return space-separated hashtags, adding # if prefix is True."""
    if prefix:
        return " ".join(f"#{t.lstrip('#')}" for t in tags)
    return " ".join(t.lstrip("#") for t in tags)


def _seo_title(title: str) -> str:
    """Ensure YouTube title ends with #Shorts if it's a Short."""
    if "#shorts" not in title.lower() and "#short" not in title.lower():
        return f"{title} #Shorts"
    return title


def _youtube_description(entry: dict) -> str:
    """Build a YouTube SEO description from an entry."""
    caption = entry.get("caption", "")
    description = entry.get("description", "")
    tags = entry.get("hashtags", entry.get("tags", []))
    product_url = entry.get("product_url", "https://fixfirst.nl")

    parts: list[str] = []
    if caption:
        parts.append(caption)
    if description:
        parts.append(description)
    parts.append("\n👇 Meer tips & gratis gidsen:")
    parts.append(product_url)
    if tags:
        parts.append("\n" + _hashtag_string(tags))
    return "\n\n".join(parts)


def _instagram_caption(entry: dict) -> tuple[str, str]:
    """Return (caption_body, first_comment_hashtags)."""
    caption = entry.get("caption", entry.get("title", ""))
    tags = entry.get("hashtags", [])
    product_url = entry.get("product_url", "")

    body_parts = [caption]
    if product_url:
        body_parts.append(f"📎 {product_url}")
    else:
        body_parts.append("📎 Link in bio voor de volledige gids")

    body = "\n\n".join(body_parts)
    first_comment = _hashtag_string(tags) if tags else ""
    return body, first_comment


def _tiktok_caption(entry: dict) -> str:
    """Return short hook caption ≤150 chars + inline hashtags."""
    caption = entry.get("caption", entry.get("title", ""))
    tags = entry.get("hashtags", [])

    # Truncate caption to 120 chars to leave room for hashtags
    short = caption[:120].rstrip()
    if len(caption) > 120:
        short = short.rstrip(".,!?") + "…"

    tag_str = _hashtag_string(tags[:5])  # TikTok: max 5 tags recommended
    return f"{short} {tag_str}".strip()


def generate_captions(
    entries: list[dict],
    platform: str,
    output_format: str,
    output_path: Path,
) -> None:
    """Generate captions for all entries and write to output file."""
    results: list[dict] = []

    for entry in entries:
        video_path = entry.get("video_path", "")
        title = entry.get("title", "")
        tags = entry.get("hashtags", entry.get("tags", []))

        if platform == "instagram":
            caption_body, first_comment = _instagram_caption(entry)
            results.append({
                "video_path": video_path,
                "title": title,
                "platform": "instagram",
                "caption": caption_body,
                "first_comment_hashtags": first_comment,
            })

        elif platform == "tiktok":
            caption = _tiktok_caption(entry)
            results.append({
                "video_path": video_path,
                "title": title,
                "platform": "tiktok",
                "caption": caption,
            })

        elif platform == "youtube":
            yt_title = _seo_title(title)
            description = _youtube_description(entry)
            results.append({
                "video_path": video_path,
                "title": yt_title,
                "platform": "youtube",
                "description": description,
                "tags": _hashtag_string(tags, prefix=False),
            })

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_format == "json":
        with open(output_path, "w", encoding="utf-8") as fh:
            json.dump(results, fh, ensure_ascii=False, indent=2)
    else:
        # CSV – determine columns from first result
        if not results:
            columns = ["video_path", "title", "platform", "caption"]
        else:
            columns = list(results[0].keys())
        with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(results)

    print(f"✓  {len(results)} caption(s) written to {output_path}")


def _load_entries_from_dir(script_dir: Path) -> list[dict]:
    """Load entries from manifest.json in the given directory."""
    manifest = script_dir / "manifest.json"
    if manifest.exists():
        with open(manifest, encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, list):
            return data
    # Fallback: look for individual JSON files
    entries = []
    for json_file in sorted(script_dir.glob("*.json")):
        if json_file.name == "manifest.json":
            continue
        try:
            with open(json_file, encoding="utf-8") as fh:
                obj = json.load(fh)
            if isinstance(obj, dict):
                entries.append(obj)
            elif isinstance(obj, list):
                entries.extend(obj)
        except json.JSONDecodeError:
            pass
    return entries


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate platform-specific captions from video scripts."
    )
    parser.add_argument(
        "--script-dir",
        default=str(DEFAULT_SCRIPT_DIR),
        help=f"Directory containing manifest.json or individual script JSON files (default: {DEFAULT_SCRIPT_DIR})",
    )
    parser.add_argument(
        "--platform",
        choices=SUPPORTED_PLATFORMS,
        required=True,
        help="Target platform for caption style",
    )
    parser.add_argument(
        "--output-format",
        choices=SUPPORTED_FORMATS,
        default="csv",
        help="Output format: csv or json (default: csv)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help=(
            "Output file path. Defaults to output/captions_<platform>.<format> "
            "relative to the repo root."
        ),
    )

    args = parser.parse_args()

    script_dir = Path(args.script_dir)
    if not script_dir.exists():
        print(f"Script directory not found: {script_dir}", file=sys.stderr)
        sys.exit(1)

    entries = _load_entries_from_dir(script_dir)
    if not entries:
        print(f"No entries found in {script_dir}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        output_path = Path(args.output)
    else:
        ext = args.output_format
        output_path = DEFAULT_OUTPUT_DIR / f"captions_{args.platform}.{ext}"

    generate_captions(
        entries=entries,
        platform=args.platform,
        output_format=args.output_format,
        output_path=output_path,
    )


if __name__ == "__main__":
    main()
