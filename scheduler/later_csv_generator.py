#!/usr/bin/env python3
"""Generate a Later.com-compatible bulk-upload CSV from a video manifest.

Usage
-----
python scheduler/later_csv_generator.py \\
    --manifest scripts/video_shorts/manifest.json \\
    --start-date 2026-03-01 \\
    --posts-per-day 3 \\
    --platforms instagram tiktok pinterest \\
    --output output/later_schedule.csv
"""

import argparse
import csv
import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Repo-relative defaults
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = REPO_ROOT / "scripts" / "video_shorts" / "manifest.json"
DEFAULT_OUTPUT = REPO_ROOT / "output" / "later_schedule.csv"
STRATEGY_FILE = Path(__file__).resolve().parent / "posting_strategy.json"

SUPPORTED_PLATFORMS = ("instagram", "tiktok", "pinterest")

# Later.com CSV columns
CSV_COLUMNS = ["Date", "Time", "Caption", "Hashtags", "Media URL", "Platform"]


def _load_strategy() -> dict:
    """Load posting_strategy.json for optimal times and CTA rotation."""
    if STRATEGY_FILE.exists():
        with open(STRATEGY_FILE, encoding="utf-8") as fh:
            return json.load(fh)
    return {}


def _posting_times(strategy: dict, platform: str, posts_per_day: int) -> list[str]:
    """Return a list of HH:MM posting times for the given platform."""
    platform_data = strategy.get("platforms", {}).get(platform, {})
    nl_data = platform_data.get("nl_audience", {})
    weekday_times: list[str] = nl_data.get("weekdays", ["09:00", "13:00", "19:00"])
    return weekday_times[:posts_per_day]


def _cta_for_day(strategy: dict, day_name: str, platform: str) -> str:
    """Return the CTA string for a given weekday and platform."""
    schedule = strategy.get("cta_rotation", {}).get("weekly_schedule", {})
    cta_type = schedule.get(day_name.lower(), "link_in_bio")
    ctas = strategy.get("cta_rotation", {}).get("ctas", [])
    for cta in ctas:
        if cta["type"] == cta_type and platform in cta.get("use_on", []):
            return cta.get("nl", cta.get("en", ""))
    # Fallback
    for cta in ctas:
        if cta["type"] == cta_type:
            return cta.get("nl", cta.get("en", ""))
    return "📎 Link in bio"


def _hashtags_for_entry(strategy: dict, entry: dict, set_index: int, platform: str) -> str:
    """Pick a rotating hashtag set and return a space-separated string."""
    sets = strategy.get("hashtag_rotation", {}).get("sets", {})
    set_key = ["set_a", "set_b", "set_c"][set_index % 3]
    chosen_set = sets.get(set_key, {})

    # Guess content category from entry hashtags or title
    entry_hashtags = [h.lower() for h in entry.get("hashtags", [])]
    title_lower = entry.get("title", "").lower()

    if any(k in entry_hashtags or k in title_lower for k in ("budget", "bespaar", "financien", "geld")):
        tag_list = chosen_set.get("budget", [])
    elif any(k in entry_hashtags or k in title_lower for k in ("survival", "nood", "prepper")):
        tag_list = chosen_set.get("survival", [])
    else:
        tag_list = chosen_set.get("diy", [])

    max_tags = strategy.get("hashtag_rotation", {}).get("max_hashtags_per_post", {}).get(platform, 20)
    return " ".join(tag_list[:max_tags])


def _build_caption(entry: dict, platform: str, cta: str) -> str:
    """Build a platform-appropriate caption from the manifest entry."""
    caption = entry.get("caption", entry.get("title", ""))
    if platform == "tiktok":
        # Short hook – keep it under ~150 chars, CTA inline
        short = caption[:120].rstrip()
        return f"{short}\n\n{cta}"
    else:
        # Instagram / Pinterest – fuller caption
        return f"{caption}\n\n{cta}"


def generate_csv(
    manifest_path: Path,
    start_date: date,
    posts_per_day: int,
    platforms: list[str],
    output_path: Path,
) -> None:
    """Core CSV generation logic."""
    # Load manifest
    if not manifest_path.exists():
        print(f"Manifest not found: {manifest_path}", file=sys.stderr)
        sys.exit(1)

    with open(manifest_path, encoding="utf-8") as fh:
        entries: list[dict] = json.load(fh)

    if not isinstance(entries, list):
        print("Manifest must be a JSON array.", file=sys.stderr)
        sys.exit(1)

    strategy = _load_strategy()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    current_date = start_date
    entry_index = 0
    hashtag_set_index = 0

    while entry_index < len(entries):
        day_name = current_date.strftime("%A")
        date_str = current_date.strftime("%Y-%m-%d")

        for platform in platforms:
            times = _posting_times(strategy, platform, posts_per_day)
            for time_str in times:
                if entry_index >= len(entries):
                    break
                entry = entries[entry_index]

                # Skip entries restricted to other platforms
                entry_platforms = entry.get("platforms", list(platforms))
                if platform not in entry_platforms:
                    continue

                cta = _cta_for_day(strategy, day_name, platform)
                caption = _build_caption(entry, platform, cta)
                hashtags = _hashtags_for_entry(strategy, entry, hashtag_set_index, platform)
                media_url = entry.get("media_url", entry.get("video_path", ""))

                rows.append({
                    "Date": date_str,
                    "Time": time_str,
                    "Caption": caption,
                    "Hashtags": hashtags,
                    "Media URL": media_url,
                    "Platform": platform.capitalize(),
                })

                entry_index += 1
                hashtag_set_index += 1

        current_date += timedelta(days=1)

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓  {len(rows)} row(s) written to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a Later.com bulk-upload CSV from a video manifest."
    )
    parser.add_argument(
        "--manifest",
        default=str(DEFAULT_MANIFEST),
        help=f"Path to the video shorts manifest JSON (default: {DEFAULT_MANIFEST})",
    )
    parser.add_argument(
        "--start-date",
        default=str(date.today()),
        help="First posting date in YYYY-MM-DD format (default: today)",
    )
    parser.add_argument(
        "--posts-per-day",
        type=int,
        default=3,
        help="Number of posts per platform per day (default: 3)",
    )
    parser.add_argument(
        "--platforms",
        nargs="+",
        choices=SUPPORTED_PLATFORMS,
        default=list(SUPPORTED_PLATFORMS),
        help="Platforms to schedule (default: instagram tiktok pinterest)",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help=f"Output CSV path (default: {DEFAULT_OUTPUT})",
    )

    args = parser.parse_args()

    try:
        start_date = date.fromisoformat(args.start_date)
    except ValueError:
        print(f"Invalid start-date: '{args.start_date}' – use YYYY-MM-DD format.", file=sys.stderr)
        sys.exit(1)

    generate_csv(
        manifest_path=Path(args.manifest),
        start_date=start_date,
        posts_per_day=args.posts_per_day,
        platforms=args.platforms,
        output_path=Path(args.output),
    )


if __name__ == "__main__":
    main()
