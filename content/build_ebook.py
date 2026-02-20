#!/usr/bin/env python3
"""
build_ebook.py — Build the Survival Basis Gids NL e-book

Reads all chapter .md files in order, combines them into a single markdown
with a table of contents, and outputs:
  - output/survival_basis_gids_NL.md   (combined markdown)
  - output/survival_basis_gids_NL.html  (styled, print-ready HTML)

Usage:
    python content/build_ebook.py
"""

import json
import os
import re
import sys

try:
    import markdown
except ImportError:
    markdown = None

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
BOOK_DIR = os.path.join(SCRIPT_DIR, "survival_basis_gids")
METADATA_FILE = os.path.join(BOOK_DIR, "metadata.json")
OUTPUT_DIR = os.path.join(REPO_ROOT, "output")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  /* Reset & base */
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 11pt;
    line-height: 1.7;
    color: #1a1a1a;
    background: #fff;
    max-width: 800px;
    margin: 0 auto;
    padding: 2cm 2.5cm;
  }}

  /* Headings */
  h1 {{ font-size: 2.4em; margin: 2em 0 0.5em; color: #1a3a2a; page-break-before: always; }}
  h1:first-of-type {{ page-break-before: avoid; }}
  h2 {{ font-size: 1.6em; margin: 1.8em 0 0.4em; color: #1a3a2a; border-bottom: 2px solid #2d6a4f; padding-bottom: 0.2em; }}
  h3 {{ font-size: 1.2em; margin: 1.4em 0 0.3em; color: #2d6a4f; }}
  h4 {{ font-size: 1.05em; margin: 1.2em 0 0.2em; color: #40916c; font-style: italic; }}

  /* Paragraphs and lists */
  p {{ margin: 0.8em 0; }}
  ul, ol {{ margin: 0.6em 0 0.6em 2em; }}
  li {{ margin: 0.3em 0; }}
  ul li {{ list-style-type: disc; }}
  ol li {{ list-style-type: decimal; }}

  /* Blockquotes (summary boxes) */
  blockquote {{
    background: #d8f3dc;
    border-left: 5px solid #2d6a4f;
    margin: 1.5em 0;
    padding: 1em 1.5em;
    border-radius: 0 6px 6px 0;
    font-style: italic;
    color: #1b4332;
  }}

  /* Code */
  code {{
    background: #f4f4f4;
    padding: 0.15em 0.4em;
    border-radius: 3px;
    font-family: 'Courier New', monospace;
    font-size: 0.9em;
  }}
  pre {{
    background: #f4f4f4;
    padding: 1em;
    border-radius: 6px;
    overflow-x: auto;
    margin: 1em 0;
  }}
  pre code {{ background: none; padding: 0; }}

  /* Tables */
  table {{
    border-collapse: collapse;
    width: 100%;
    margin: 1.2em 0;
    font-size: 0.95em;
  }}
  th {{
    background: #2d6a4f;
    color: #fff;
    padding: 0.6em 1em;
    text-align: left;
  }}
  td {{ padding: 0.5em 1em; border-bottom: 1px solid #d0e8da; }}
  tr:nth-child(even) td {{ background: #f0faf4; }}

  /* Horizontal rule */
  hr {{ border: none; border-top: 1px solid #b7e4c7; margin: 2em 0; }}

  /* TOC */
  .toc {{ background: #f0faf4; border: 1px solid #b7e4c7; padding: 1.5em 2em; border-radius: 8px; margin: 2em 0; }}
  .toc h2 {{ border-bottom: none; margin-top: 0; }}
  .toc ol {{ margin-left: 1.5em; }}
  .toc li {{ margin: 0.5em 0; }}
  .toc a {{ color: #2d6a4f; text-decoration: none; }}
  .toc a:hover {{ text-decoration: underline; }}

  /* Cover */
  .cover {{
    text-align: center;
    padding: 4em 0 3em;
    page-break-after: always;
  }}
  .cover h1 {{ font-size: 3em; page-break-before: avoid; border-bottom: none; }}
  .cover .subtitle {{ font-size: 1.3em; color: #2d6a4f; margin: 0.5em 0 2em; }}
  .cover .author {{ font-size: 1.1em; color: #555; }}
  .cover .logo {{ font-size: 2.5em; margin-bottom: 0.5em; }}

  /* Print */
  @media print {{
    body {{ padding: 1.5cm 2cm; max-width: none; }}
    h1 {{ page-break-before: always; }}
    h2, h3 {{ page-break-after: avoid; }}
    blockquote, table {{ page-break-inside: avoid; }}
    .cover {{ page-break-after: always; }}
  }}
</style>
</head>
<body>

<div class="cover">
  <div class="logo">🌿</div>
  <h1>{title}</h1>
  <p class="subtitle">{subtitle}</p>
  <p class="author">door <strong>{author}</strong></p>
</div>

{body}

</body>
</html>
"""


def load_metadata():
    """Load book metadata from metadata.json."""
    with open(METADATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def get_chapter_files(metadata):
    """Return ordered list of chapter file paths based on metadata."""
    chapters = []
    for chapter in metadata.get("chapters", []):
        chapter_path = os.path.join(BOOK_DIR, chapter["file"])
        if not os.path.isfile(chapter_path):
            print(f"WARNING: Chapter file not found: {chapter_path}", file=sys.stderr)
            continue
        chapters.append((chapter["number"], chapter["title"], chapter_path))
    return chapters


def extract_heading(content, default_title):
    """Extract the first H1 heading from markdown content."""
    for line in content.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return default_title


def build_toc(chapters):
    """Build a markdown table of contents."""
    lines = ["## Inhoudsopgave\n"]
    for number, title, _ in chapters:
        anchor = re.sub(r"[^a-z0-9\-]", "", title.lower().replace(" ", "-"))
        lines.append(f"{number}. [{title}](#{anchor})")
    return "\n".join(lines)


def combine_markdown(metadata, chapters):
    """Combine all chapters into a single markdown string with TOC."""
    parts = []

    # Cover / title block
    title = metadata.get("title", "Survival Basis Gids NL")
    subtitle = metadata.get("subtitle", "")
    author = metadata.get("author", "FixFirst NL")
    description = metadata.get("description", "")

    parts.append(f"# {title}\n")
    if subtitle:
        parts.append(f"**{subtitle}**\n")
    parts.append(f"*door {author}*\n")
    if description:
        parts.append(f"\n> {description}\n")
    parts.append("\n---\n")

    # Table of contents
    parts.append(build_toc(chapters))
    parts.append("\n---\n")

    # Chapter content
    for number, title, filepath in chapters:
        with open(filepath, encoding="utf-8") as f:
            content = f.read().strip()
        parts.append(f"\n{content}\n")
        parts.append("\n---\n")

    return "\n".join(parts)


def markdown_to_html(md_text, metadata):
    """Convert markdown text to styled HTML."""
    title = metadata.get("title", "Survival Basis Gids NL")
    subtitle = metadata.get("subtitle", "")
    author = metadata.get("author", "FixFirst NL")

    if markdown is not None:
        md_instance = markdown.Markdown(
            extensions=["tables", "fenced_code", "toc", "nl2br"],
            extension_configs={
                "toc": {"permalink": False}
            },
        )
        body_html = md_instance.convert(md_text)
    else:
        # Fallback: wrap in <pre> if markdown package is not installed
        print("WARNING: 'markdown' package not installed. Falling back to plain text HTML.")
        escaped = md_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        body_html = f"<pre>{escaped}</pre>"

    return HTML_TEMPLATE.format(
        title=title,
        subtitle=subtitle,
        author=author,
        body=body_html,
    )


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Loading metadata...")
    metadata = load_metadata()

    print("Collecting chapter files...")
    chapters = get_chapter_files(metadata)
    if not chapters:
        print("ERROR: No chapter files found.", file=sys.stderr)
        sys.exit(1)
    print(f"  Found {len(chapters)} chapters.")

    print("Building combined markdown...")
    combined_md = combine_markdown(metadata, chapters)

    md_output = os.path.join(OUTPUT_DIR, "survival_basis_gids_NL.md")
    with open(md_output, "w", encoding="utf-8") as f:
        f.write(combined_md)
    print(f"  Written: {md_output}")

    print("Generating HTML...")
    html_content = markdown_to_html(combined_md, metadata)

    html_output = os.path.join(OUTPUT_DIR, "survival_basis_gids_NL.html")
    with open(html_output, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"  Written: {html_output}")

    print("\nBuild complete!")
    print(f"  Markdown : {md_output}")
    print(f"  HTML     : {html_output}")


if __name__ == "__main__":
    main()
