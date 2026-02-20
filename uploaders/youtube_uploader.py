"""YouTube Shorts uploader using the YouTube Data API v3 with OAuth2."""

import os
import logging
from typing import Optional

logger = logging.getLogger("autopost.youtube")

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_FILE = "youtube_token.json"


def _get_credentials(client_secret_file: str) -> object:
    """Return valid OAuth2 credentials, refreshing or re-authorising as needed."""
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds: Optional[Credentials] = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w", encoding="utf-8") as token_fh:
            token_fh.write(creds.to_json())

    return creds


def upload_video(
    video_path: str,
    title: str,
    description: str = "",
    tags: Optional[list[str]] = None,
    privacy_status: str = "public",
    dry_run: bool = False,
) -> None:
    """Upload a video to YouTube as a YouTube Short.

    Args:
        video_path: Absolute path to the video file.
        title: Video title (``#Shorts`` will be appended if absent).
        description: Video description.
        tags: Optional list of tag strings.
        privacy_status: One of ``public``, ``private``, or ``unlisted``.
        dry_run: When True, skip the actual upload.
    """
    client_secret_file = os.getenv("YOUTUBE_CLIENT_SECRET_FILE", "client_secret.json")

    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    # YouTube Shorts requirement: #Shorts must appear in title or description
    if "#shorts" not in title.lower():
        title = f"{title} #Shorts"

    if dry_run:
        logger.info(
            "[DRY-RUN] YouTube: would upload '%s' as '%s' (%s)",
            video_path,
            title,
            privacy_status,
        )
        return

    if not os.path.isfile(client_secret_file):
        raise FileNotFoundError(f"YouTube client secret not found: {client_secret_file}")

    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    creds = _get_credentials(client_secret_file)
    youtube = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or [],
            "categoryId": "22",  # People & Blogs
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    logger.info("YouTube: starting upload of '%s' …", video_path)
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            logger.debug("YouTube: upload progress %.1f%%", status.progress() * 100)

    logger.info("YouTube: upload complete – video id %s", response.get("id"))
