#!/usr/bin/env python3
"""
build_ebook.py – FixFirst Emergency Toolkit Pro eBook Builder

Reads all chapter Markdown files defined in metadata.json,
combines them into a single Markdown file, and generates an HTML version.

Output:
  output/emergency_toolkit_pro_NL.md
  output/emergency_toolkit_pro_NL.html

Usage:
  python content/emergency_toolkit_pro/build_ebook.py
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
OUTPUT_DIR = REPO_ROOT / "output"
METADATA_FILE = SCRIPT_DIR / "metadata.json"

OUTPUT_MD = OUTPUT_DIR / "emergency_toolkit_pro_NL.md"
OUTPUT_HTML = OUTPUT_DIR / "emergency_toolkit_pro_NL.html"


def load_metadata(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def read_chapter(chapter_path: Path) -> str:
    if not chapter_path.exists():
        print(f"  [WARN] Chapter not found: {chapter_path}", file=sys.stderr)
        return f"<!-- Chapter not found: {chapter_path.name} -->\n"
    with open(chapter_path, encoding="utf-8") as f:
        return f.read()


def build_markdown(metadata: dict) -> str:
    """Combine cover, TOC, and all chapters into one Markdown string."""
    parts = []

    # ── Cover page ──────────────────────────────────────────────────────────
    parts.append(f"# {metadata['title']}\n")
    parts.append(f"## {metadata['subtitle']}\n")
    parts.append(f"**Auteur:** {metadata['author']}  \n")
    parts.append(f"**Versie:** {metadata['version']}  \n")
    parts.append(f"**Taal:** {metadata['language']}  \n")
    parts.append(f"**Prijs:** EUR {metadata['price_eur']:.2f}  \n")
    parts.append(f"**Gepubliceerd:** {metadata['published_date']}  \n")
    parts.append("\n---\n\n")

    # ── Description ─────────────────────────────────────────────────────────
    parts.append("## Over dit boek\n\n")
    parts.append(f"{metadata['description']}\n\n")
    parts.append("---\n\n")

    # ── Table of Contents ───────────────────────────────────────────────────
    parts.append("## Inhoudsopgave\n\n")
    for ch in metadata["chapters"]:
        parts.append(f"{ch['number']}. {ch['title']}\n")
    parts.append("\n---\n\n")

    # ── Chapters ────────────────────────────────────────────────────────────
    for ch in metadata["chapters"]:
        chapter_path = SCRIPT_DIR / ch["file"]
        content = read_chapter(chapter_path)
        parts.append(content)
        parts.append("\n\n---\n\n")

    # ── Footer ──────────────────────────────────────────────────────────────
    parts.append("---\n\n")
    parts.append(f"*© {datetime.now().year} {metadata['author']}. "
                 "Alle rechten voorbehouden.*  \n")
    parts.append(f"*Meer producten op: {metadata['gumroad_url']}*\n")

    return "".join(parts)


def markdown_to_html(md_text: str, metadata: dict) -> str:
    """
    Convert Markdown to a self-contained HTML page using minimal inline rules.
    Requires no external dependencies – covers headings, bold, italic,
    horizontal rules, code blocks, tables, lists, and paragraphs.
    """
    try:
        import markdown  # type: ignore
        body = markdown.markdown(
            md_text,
            extensions=["tables", "fenced_code", "nl2br"],
        )
    except ImportError:
        # Fallback: very simple line-by-line conversion
        body = _simple_md_to_html(md_text)

    title = metadata["title"]
    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <style>
    body {{
      font-family: Georgia, 'Times New Roman', serif;
      max-width: 800px;
      margin: 40px auto;
      padding: 0 20px;
      line-height: 1.7;
      color: #222;
      background: #fff;
    }}
    h1 {{ font-size: 2em; color: #c0392b; margin-top: 1.5em; }}
    h2 {{ font-size: 1.5em; color: #2c3e50; border-bottom: 2px solid #c0392b;
          padding-bottom: 4px; margin-top: 1.5em; }}
    h3 {{ font-size: 1.2em; color: #34495e; margin-top: 1.2em; }}
    hr  {{ border: none; border-top: 1px solid #ddd; margin: 2em 0; }}
    code {{ background: #f4f4f4; padding: 2px 5px; border-radius: 3px;
            font-family: monospace; }}
    pre  {{ background: #f4f4f4; padding: 15px; border-radius: 5px;
            overflow-x: auto; }}
    blockquote {{
      border-left: 4px solid #c0392b;
      margin: 1em 0;
      padding: 8px 16px;
      background: #fdf3f3;
      color: #555;
    }}
    table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
    th, td {{ border: 1px solid #ccc; padding: 8px 12px; text-align: left; }}
    th {{ background: #2c3e50; color: #fff; }}
    tr:nth-child(even) {{ background: #f9f9f9; }}
    ul, ol {{ padding-left: 1.5em; }}
    a {{ color: #c0392b; }}
    @media print {{
      body {{ margin: 0; padding: 10mm; }}
      h1, h2 {{ page-break-after: avoid; }}
    }}
  </style>
</head>
<body>
{body}
</body>
</html>
"""


def _simple_md_to_html(md: str) -> str:
    """Minimal Markdown → HTML without external libraries."""
    import re
    html_lines = []
    in_code_block = False
    in_table = False

    for line in md.splitlines():
        # Fenced code blocks
        if line.startswith("```"):
            if in_code_block:
                html_lines.append("</code></pre>")
                in_code_block = False
            else:
                html_lines.append("<pre><code>")
                in_code_block = True
            continue

        if in_code_block:
            html_lines.append(line)
            continue

        # Headings
        if line.startswith("### "):
            html_lines.append(f"<h3>{_inline(line[4:])}</h3>")
        elif line.startswith("## "):
            html_lines.append(f"<h2>{_inline(line[3:])}</h2>")
        elif line.startswith("# "):
            html_lines.append(f"<h1>{_inline(line[2:])}</h1>")
        # Horizontal rules
        elif re.match(r"^-{3,}$", line.strip()) or re.match(r"^={3,}$", line.strip()):
            html_lines.append("<hr />")
        # Blockquote
        elif line.startswith("> "):
            html_lines.append(f"<blockquote>{_inline(line[2:])}</blockquote>")
        # Table rows
        elif "|" in line:
            cells = [c.strip() for c in line.split("|") if c.strip()]
            if re.match(r"^[\s|:-]+$", line):  # separator row
                in_table = True
                continue
            tag = "th" if not in_table else "td"
            row = "".join(f"<{tag}>{_inline(c)}</{tag}>" for c in cells)
            if not in_table:
                html_lines.append(f"<table><thead><tr>{row}</tr></thead><tbody>")
                in_table = True
            else:
                html_lines.append(f"<tr>{row}</tr>")
        # Unordered list
        elif re.match(r"^[-*] ", line):
            html_lines.append(f"<li>{_inline(line[2:])}</li>")
        # Ordered list
        elif re.match(r"^\d+\. ", line):
            html_lines.append(f"<li>{_inline(re.sub(r'^\d+\. ', '', line))}</li>")
        # Empty line – close open table if needed
        elif line.strip() == "":
            if in_table:
                html_lines.append("</tbody></table>")
                in_table = False
            html_lines.append("<br />")
        else:
            html_lines.append(f"<p>{_inline(line)}</p>")

    if in_table:
        html_lines.append("</tbody></table>")

    return "\n".join(html_lines)


def _inline(text: str) -> str:
    """Apply inline Markdown formatting: bold, italic, code, links."""
    import re
    # Bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Italic
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    # Inline code
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    # Links
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', text)
    return text


def main() -> int:
    print("FixFirst Emergency Toolkit Pro – eBook Builder")
    print("=" * 50)

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load metadata
    print(f"Loading metadata from {METADATA_FILE} …")
    metadata = load_metadata(METADATA_FILE)
    print(f"  Title   : {metadata['title']}")
    print(f"  Chapters: {len(metadata['chapters'])}")

    # Build combined Markdown
    print("\nCombining chapters …")
    md_content = build_markdown(metadata)
    word_count = len(md_content.split())
    print(f"  Total words: {word_count:,}")

    # Write Markdown output
    OUTPUT_MD.write_text(md_content, encoding="utf-8")
    print(f"\n✅  Markdown written → {OUTPUT_MD}")

    # Write HTML output
    html_content = markdown_to_html(md_content, metadata)
    OUTPUT_HTML.write_text(html_content, encoding="utf-8")
    print(f"✅  HTML     written → {OUTPUT_HTML}")

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
