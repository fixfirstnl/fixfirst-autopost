#!/usr/bin/env python3
"""Generate manifest.json from script_*.md files in scripts/video_shorts/.

Usage
-----
python scripts/generate_manifest.py
python scripts/generate_manifest.py --niche diy
python scripts/generate_manifest.py --niche survival
python scripts/generate_manifest.py --niche budget
python scripts/generate_manifest.py --output my_manifest.json
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# Directory containing the script markdown files (relative to this file)
SCRIPTS_DIR = Path(__file__).parent / "video_shorts"

# Map niche frontmatter values to --niche filter argument values
NICHE_ALIASES: dict[str, list[str]] = {
    "diy": ["diy"],
    "survival": ["survival"],
    "budget": ["budget"],
}

# Script number → video file name mapping
def _video_filename(script_path: Path) -> str:
    """Derive the video filename from the script filename.

    ``script_01_kraan_lekt.md`` → ``video_01.mp4``
    """
    match = re.match(r"script_(\d+)_", script_path.name)
    if match:
        return f"video_{match.group(1)}.mp4"
    return script_path.stem + ".mp4"


def _parse_frontmatter(content: str) -> dict[str, str]:
    """Extract key: value pairs from a YAML-style frontmatter block."""
    frontmatter: dict[str, str] = {}
    # Match the block between the first pair of --- delimiters
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return frontmatter
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            frontmatter[key.strip()] = value.strip().strip('"')
    return frontmatter


def _extract_section(content: str, section_name: str) -> str:
    """Return the text body of a ## Section in the markdown."""
    pattern = rf"## {re.escape(section_name)}\n(.*?)(?=\n##|\Z)"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def _parse_hashtags(raw: str) -> list[str]:
    """Convert a hashtag string like '#diy #besparen ...' into a list."""
    return [tag.lstrip("#") for tag in raw.split() if tag.startswith("#")]


def _parse_script(script_path: Path) -> dict | None:
    """Parse a single script markdown file into a manifest entry dict."""
    content = script_path.read_text(encoding="utf-8")
    frontmatter = _parse_frontmatter(content)

    title_nl = frontmatter.get("title_nl", "").strip('"')
    niche = frontmatter.get("niche", "").lower()

    hook_raw = _extract_section(content, "Hook")
    # Strip surrounding quotes from the hook line
    hook = hook_raw.strip('"')

    hashtag_raw = _extract_section(content, "Hashtags")
    hashtags = _parse_hashtags(hashtag_raw)

    video_file = f"videos/{_video_filename(script_path)}"

    # Build caption: hook + top hashtags (first 5 for caption brevity)
    top_tags = " ".join(f"#{t}" for t in hashtags[:5])
    caption = f"{hook} {top_tags}"

    # Use Script NL section as the long description
    description_nl = _extract_section(content, "Script NL")

    cta_raw = _extract_section(content, "CTA")

    return {
        "video_path": video_file,
        "title": title_nl,
        "caption": caption,
        "hashtags": hashtags,
        "description": description_nl + ("\n\n" + cta_raw if cta_raw else ""),
        "platforms": ["tiktok", "youtube", "instagram"],
        "niche": niche,
        "privacy_status": "public",
    }


def generate_manifest(
    scripts_dir: Path,
    niche_filter: str | None = None,
) -> list[dict]:
    """Read all script_*.md files and return a list of manifest entry dicts."""
    script_files = sorted(scripts_dir.glob("script_*.md"))
    if not script_files:
        print(f"WARNING: No script_*.md files found in '{scripts_dir}'", file=sys.stderr)
        return []

    entries: list[dict] = []
    for script_path in script_files:
        entry = _parse_script(script_path)
        if entry is None:
            continue
        if niche_filter and entry.get("niche") != niche_filter.lower():
            continue
        entries.append(entry)

    return entries


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a manifest JSON file from script_*.md files."
    )
    parser.add_argument(
        "--niche",
        choices=list(NICHE_ALIASES.keys()),
        default=None,
        help="Filter scripts by niche (diy / survival / budget). Omit for all niches.",
    )
    parser.add_argument(
        "--output",
        default=None,
        metavar="FILE",
        help=(
            "Output path for the generated manifest JSON. "
            "Defaults to 'scripts/manifest_batch_01.json' (or "
            "'scripts/manifest_batch_01_<niche>.json' when --niche is used)."
        ),
    )
    parser.add_argument(
        "--scripts-dir",
        default=str(SCRIPTS_DIR),
        metavar="DIR",
        help="Directory containing script_*.md files.",
    )
    args = parser.parse_args()

    scripts_dir = Path(args.scripts_dir)
    if not scripts_dir.is_dir():
        print(f"ERROR: Scripts directory '{scripts_dir}' not found.", file=sys.stderr)
        sys.exit(1)

    entries = generate_manifest(scripts_dir, niche_filter=args.niche)

    if args.output:
        output_path = Path(args.output)
    elif args.niche:
        output_path = Path(__file__).parent / f"manifest_batch_01_{args.niche}.json"
    else:
        output_path = Path(__file__).parent / "manifest_batch_01.json"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(entries, fh, indent=2, ensure_ascii=False)

    print(
        f"Generated {len(entries)} manifest entries → '{output_path}'"
        + (f"  (niche filter: {args.niche})" if args.niche else "")
    )


if __name__ == "__main__":
    main()
