"""Main CLI entry point for fixfirst-autopost.

Usage examples
--------------
python upload.py --platform tiktok   --batch manifest.json
python upload.py --platform youtube  --batch manifest.json
python upload.py --platform instagram --batch manifest.json
python upload.py --all               --batch manifest.json
python upload.py --all               --batch manifest.json --dry-run
"""

import argparse
import sys
import time
import logging
from typing import Any

from dotenv import load_dotenv

from utils.logger import get_logger
from utils.manifest_parser import (
    load_manifest,
    is_already_uploaded,
    mark_uploaded,
)

load_dotenv()

logger = get_logger()

SUPPORTED_PLATFORMS = ("tiktok", "youtube", "instagram")
MAX_RETRIES = 3
BACKOFF_BASE = 2  # seconds – actual wait = BACKOFF_BASE ** attempt


def _upload_one(platform: str, entry: dict[str, Any], dry_run: bool) -> bool:
    """Dispatch upload for a single manifest entry to the given platform.

    Returns True on success, False on failure.
    """
    video_path: str = entry.get("video_path", "")
    caption: str = entry.get("caption", "")
    title: str = entry.get("title", caption)
    description: str = entry.get("description", "")
    hashtags: list[str] = entry.get("hashtags", [])
    tags: list[str] = entry.get("tags", hashtags)
    privacy_status: str = entry.get("privacy_status", "public")

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            if platform == "tiktok":
                from uploaders.tiktok_uploader import upload_video as tiktok_upload
                tiktok_upload(video_path, caption, hashtags, dry_run=dry_run)

            elif platform == "youtube":
                from uploaders.youtube_uploader import upload_video as youtube_upload
                youtube_upload(
                    video_path, title, description, tags, privacy_status, dry_run=dry_run
                )

            elif platform == "instagram":
                from uploaders.instagram_uploader import upload_video as instagram_upload
                instagram_upload(video_path, caption, hashtags, dry_run=dry_run)

            return True

        except Exception as exc:  # noqa: BLE001
            wait = BACKOFF_BASE ** attempt
            if attempt < MAX_RETRIES:
                logger.warning(
                    "[%s] attempt %d/%d failed for '%s': %s – retrying in %ds …",
                    platform,
                    attempt,
                    MAX_RETRIES,
                    video_path,
                    exc,
                    wait,
                )
                time.sleep(wait)
            else:
                logger.error(
                    "[%s] all %d attempts failed for '%s': %s",
                    platform,
                    MAX_RETRIES,
                    video_path,
                    exc,
                )

    return False


def _run_batch(platforms: list[str], manifest_path: str, dry_run: bool) -> None:
    """Process every entry in the manifest for each requested platform."""
    entries = load_manifest(manifest_path)
    logger.info(
        "Loaded %d entries from '%s'. Platforms: %s",
        len(entries),
        manifest_path,
        ", ".join(platforms),
    )

    total = 0
    success = 0
    skipped = 0
    failed = 0

    for entry in entries:
        video_path: str = entry.get("video_path", "")
        entry_platforms: list[str] = entry.get("platforms", list(platforms))

        for platform in platforms:
            if platform not in entry_platforms:
                continue

            total += 1

            if is_already_uploaded(video_path, platform):
                logger.info("[%s] skipping '%s' – already uploaded", platform, video_path)
                skipped += 1
                continue

            logger.info("[%s] uploading '%s' …", platform, video_path)
            ok = _upload_one(platform, entry, dry_run)

            if ok:
                if not dry_run:
                    mark_uploaded(video_path, platform)
                logger.info("[%s] ✓ '%s' uploaded successfully", platform, video_path)
                success += 1
            else:
                failed += 1

    # Summary report
    logger.info(
        "=== Batch complete: %d total | %d success | %d skipped | %d failed ===",
        total,
        success,
        skipped,
        failed,
    )

    if failed:
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Automatically upload videos to TikTok, YouTube Shorts, and Instagram Reels."
    )
    platform_group = parser.add_mutually_exclusive_group(required=True)
    platform_group.add_argument(
        "--platform",
        choices=SUPPORTED_PLATFORMS,
        help="Target platform for upload.",
    )
    platform_group.add_argument(
        "--all",
        action="store_true",
        help="Upload to all supported platforms.",
    )
    parser.add_argument(
        "--batch",
        required=True,
        metavar="MANIFEST",
        help="Path to the manifest JSON file.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate inputs and log actions without performing actual uploads.",
    )

    args = parser.parse_args()

    platforms = list(SUPPORTED_PLATFORMS) if args.all else [args.platform]

    if args.dry_run:
        logger.info("DRY-RUN mode enabled – no uploads will be performed.")

    _run_batch(platforms, args.batch, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
