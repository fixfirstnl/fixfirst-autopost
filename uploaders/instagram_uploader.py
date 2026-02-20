"""Instagram Reels uploader using instagrapi."""

import os
import logging
from pathlib import Path
from typing import Optional

from utils import build_caption

logger = logging.getLogger("autopost.instagram")

SESSION_FILE = "instagram_session.json"


def _get_client() -> object:
    """Return an authenticated instagrapi Client, reusing a saved session if possible."""
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired

    username = os.getenv("IG_USERNAME")
    password = os.getenv("IG_PASSWORD")

    if not username or not password:
        raise EnvironmentError("IG_USERNAME and IG_PASSWORD must be set in the environment")

    cl = Client()
    cl.delay_range = [1, 3]

    if os.path.exists(SESSION_FILE):
        try:
            cl.load_settings(SESSION_FILE)
            cl.login(username, password)
            logger.debug("Instagram: reused existing session")
            return cl
        except LoginRequired:
            logger.warning("Instagram: saved session expired, re-logging in …")

    cl.login(username, password)
    cl.dump_settings(SESSION_FILE)
    logger.debug("Instagram: logged in and session saved")
    return cl


def upload_video(
    video_path: str,
    caption: str,
    hashtags: Optional[list[str]] = None,
    dry_run: bool = False,
) -> None:
    """Upload a video to Instagram as a Reel.

    Args:
        video_path: Absolute path to the video file.
        caption: Post caption text.
        hashtags: Optional list of hashtag strings (without the # prefix).
        dry_run: When True, skip the actual upload.
    """
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    full_caption = build_caption(caption, hashtags)

    if dry_run:
        logger.info(
            "[DRY-RUN] Instagram: would upload '%s' with caption: %s",
            video_path,
            full_caption,
        )
        return

    cl = _get_client()
    logger.info("Instagram: uploading reel '%s' …", video_path)
    cl.clip_upload(Path(video_path), full_caption)
    logger.info("Instagram: upload complete for '%s'", video_path)
