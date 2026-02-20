#!/usr/bin/env python3
"""
generate_survival_gids.py — Verify and report on the Survival Basis Gids NL content pipeline.

This script confirms that all required content files exist, counts words in each
chapter, and reports the overall status of the e-book content pipeline.

Run this script to verify that the pipeline is complete, or to regenerate missing
files by running build_ebook.py afterwards.

Usage:
    python content/generate_survival_gids.py
"""

import json
import os
import re
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
BOOK_DIR = os.path.join(SCRIPT_DIR, "survival_basis_gids")
CHAPTERS_DIR = os.path.join(BOOK_DIR, "chapters")
METADATA_FILE = os.path.join(BOOK_DIR, "metadata.json")
GUMROAD_FILE = os.path.join(SCRIPT_DIR, "gumroad_listing.json")
BUILD_SCRIPT = os.path.join(SCRIPT_DIR, "build_ebook.py")
OUTPUT_DIR = os.path.join(REPO_ROOT, "output")

REQUIRED_CHAPTERS = [
    ("01_water_zuivering.md", "Water purification without electricity", 3000),
    ("02_voedsel_bewaren.md", "Food preservation techniques", 3000),
    ("03_noodstroom.md", "Emergency power solutions DIY", 3000),
    ("04_eerste_hulp.md", "First aid essentials", 3000),
    ("05_gereedschap.md", "Essential survival tools checklist", 2000),
    ("06_communicatie.md", "Off-grid communication", 2000),
    ("07_onderdak.md", "Shelter & insulation DIY", 3000),
    ("08_checklist.md", "Complete survival checklist", 0),
]


def count_words(filepath):
    """Count words in a markdown file (rough estimate)."""
    with open(filepath, encoding="utf-8") as f:
        text = f.read()
    # Strip markdown syntax for a cleaner word count
    text = re.sub(r"#+ ", "", text)
    text = re.sub(r"\*\*|__|\*|_|`|~~", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", "", text)
    text = re.sub(r"[-|]", " ", text)
    return len(text.split())


def check_file(filepath, min_words=0):
    """Return (exists, word_count, meets_minimum) tuple."""
    if not os.path.isfile(filepath):
        return False, 0, False
    words = count_words(filepath)
    meets = words >= min_words if min_words > 0 else True
    return True, words, meets


def print_status(label, ok, detail=""):
    symbol = "✅" if ok else "❌"
    msg = f"  {symbol} {label}"
    if detail:
        msg += f"  ({detail})"
    print(msg)


def main():
    print("=" * 60)
    print("  Survival Basis Gids NL — Content Pipeline Status")
    print("=" * 60)

    all_ok = True

    # 1. Check chapters
    print("\n📖 Chapters:")
    for filename, description, min_words in REQUIRED_CHAPTERS:
        filepath = os.path.join(CHAPTERS_DIR, filename)
        exists, words, meets = check_file(filepath, min_words)
        if not exists:
            print_status(f"{filename}  [{description}]", False, "FILE MISSING")
            all_ok = False
        elif min_words > 0 and not meets:
            print_status(
                f"{filename}  [{description}]",
                False,
                f"{words} words (target: {min_words}+)",
            )
            all_ok = False
        else:
            detail = f"{words} words" if min_words > 0 else f"{words} words"
            print_status(f"{filename}  [{description}]", True, detail)

    # 2. Check metadata.json
    print("\n📋 Metadata:")
    if os.path.isfile(METADATA_FILE):
        try:
            with open(METADATA_FILE, encoding="utf-8") as f:
                meta = json.load(f)
            required_keys = ["title", "author", "price_eur", "keywords", "description"]
            missing = [k for k in required_keys if k not in meta]
            if missing:
                print_status(f"metadata.json  (missing keys: {missing})", False)
                all_ok = False
            else:
                print_status(
                    f"metadata.json  (title: '{meta['title']}', price: EUR {meta['price_eur']})",
                    True,
                )
        except json.JSONDecodeError as e:
            print_status(f"metadata.json  (JSON error: {e})", False)
            all_ok = False
    else:
        print_status("metadata.json", False, "FILE MISSING")
        all_ok = False

    # 3. Check gumroad_listing.json
    print("\n🛒 Gumroad Listing:")
    if os.path.isfile(GUMROAD_FILE):
        try:
            with open(GUMROAD_FILE, encoding="utf-8") as f:
                gumroad = json.load(f)
            required_keys = ["product_name", "price", "description_nl", "tags", "seo_description"]
            missing = [k for k in required_keys if k not in gumroad]
            if missing:
                print_status(f"gumroad_listing.json  (missing keys: {missing})", False)
                all_ok = False
            else:
                print_status(
                    f"gumroad_listing.json  (product: '{gumroad['product_name']}', EUR {gumroad['price']})",
                    True,
                )
        except json.JSONDecodeError as e:
            print_status(f"gumroad_listing.json  (JSON error: {e})", False)
            all_ok = False
    else:
        print_status("gumroad_listing.json", False, "FILE MISSING")
        all_ok = False

    # 4. Check build_ebook.py
    print("\n🔧 Build Script:")
    print_status("build_ebook.py", os.path.isfile(BUILD_SCRIPT))
    if not os.path.isfile(BUILD_SCRIPT):
        all_ok = False

    # 5. Run build_ebook.py to generate output files
    print("\n🏗️  Building e-book output...")
    try:
        result = subprocess.run(
            [sys.executable, BUILD_SCRIPT],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        if result.returncode == 0:
            for line in result.stdout.strip().splitlines():
                print(f"   {line}")
        else:
            print(f"  ❌ build_ebook.py failed (exit {result.returncode}):")
            for line in result.stderr.strip().splitlines():
                print(f"     {line}")
            all_ok = False
    except Exception as e:
        print(f"  ❌ Could not run build_ebook.py: {e}")
        all_ok = False

    # 6. Verify output files
    print("\n📤 Output Files:")
    for outfile in ["survival_basis_gids_NL.md", "survival_basis_gids_NL.html"]:
        path = os.path.join(OUTPUT_DIR, outfile)
        if os.path.isfile(path):
            size_kb = os.path.getsize(path) / 1024
            print_status(outfile, True, f"{size_kb:.1f} KB")
        else:
            print_status(outfile, False, "NOT GENERATED")
            all_ok = False

    # 7. Summary
    print("\n" + "=" * 60)
    if all_ok:
        print("  ✅ ALL CHECKS PASSED — Pipeline is complete!")
    else:
        print("  ❌ SOME CHECKS FAILED — Review issues above.")
    print("=" * 60)

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
