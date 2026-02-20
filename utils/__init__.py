"""Utils package for fixfirst-autopost."""


def build_caption(caption: str, hashtags: list[str] | None) -> str:
    """Append hashtags to *caption* if they are not already present."""
    if not hashtags:
        return caption
    tag_str = " ".join(f"#{tag}" for tag in hashtags)
    if tag_str in caption:
        return caption
    return f"{caption} {tag_str}"
