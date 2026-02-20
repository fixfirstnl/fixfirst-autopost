"""TikTok uploader using Selenium with session-cookie authentication."""

import os
import time
import logging
from typing import Optional

from utils import build_caption

logger = logging.getLogger("autopost.tiktok")

TIKTOK_UPLOAD_URL = "https://www.tiktok.com/creator-center/upload"
CONFIRMATION_WAIT_SECONDS = 5


def _build_driver(headless: bool = True) -> "webdriver.Chrome":
    """Initialise a Chrome WebDriver."""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def _inject_session_cookie(driver: object, session_id: str) -> None:
    """Navigate to TikTok and inject the session cookie."""
    driver.get("https://www.tiktok.com")
    driver.add_cookie(
        {
            "name": "sessionid",
            "value": session_id,
            "domain": ".tiktok.com",
            "path": "/",
            "secure": True,
        }
    )
    driver.refresh()


def upload_video(
    video_path: str,
    caption: str,
    hashtags: Optional[list[str]] = None,
    dry_run: bool = False,
) -> None:
    """Upload a video to TikTok.

    Args:
        video_path: Absolute path to the video file.
        caption: Post caption text.
        hashtags: Optional list of hashtag strings (without the # prefix).
        dry_run: When True, skip the actual upload.
    """
    session_id = os.getenv("TIKTOK_SESSION_ID")
    if not session_id:
        raise EnvironmentError("TIKTOK_SESSION_ID is not set in the environment")

    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    full_caption = build_caption(caption, hashtags)

    if dry_run:
        logger.info("[DRY-RUN] TikTok: would upload '%s' with caption: %s", video_path, full_caption)
        return

    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    driver = _build_driver()
    try:
        logger.info("TikTok: injecting session cookie …")
        _inject_session_cookie(driver, session_id)

        logger.info("TikTok: navigating to upload page …")
        driver.get(TIKTOK_UPLOAD_URL)
        wait = WebDriverWait(driver, 30)

        # Wait for the file input to appear inside the iframe
        iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe")))
        driver.switch_to.frame(iframe)

        file_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        file_input.send_keys(os.path.abspath(video_path))
        logger.info("TikTok: video file sent to input, waiting for upload …")

        # Wait for the caption textarea
        driver.switch_to.default_content()
        driver.switch_to.frame(iframe)
        caption_input = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-text='true']"))
        )
        caption_input.click()
        caption_input.clear()
        caption_input.send_keys(full_caption)

        # Submit
        submit_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Post')]"))
        )
        submit_btn.click()
        logger.info("TikTok: post submitted, waiting for confirmation …")

        # Wait for success indicator
        time.sleep(CONFIRMATION_WAIT_SECONDS)
        logger.info("TikTok: upload complete for '%s'", video_path)
    finally:
        driver.quit()
