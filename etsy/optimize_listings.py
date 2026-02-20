#!/usr/bin/env python3
"""
optimize_listings.py – Validate and report on Etsy listing templates.

Reads all JSON listing templates in etsy/listing_templates/, validates SEO
requirements, and outputs an optimization report with keyword suggestions.

Usage:
    python optimize_listings.py
    python optimize_listings.py --templates-dir listing_templates
    python optimize_listings.py --output report.txt
"""

import argparse
import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Validation constants
# ---------------------------------------------------------------------------

TITLE_MAX_CHARS = 140
TAG_MAX_CHARS = 20
TAG_REQUIRED_COUNT = 13
DESCRIPTION_MIN_CHARS = 2000
REQUIRED_FIELDS = [
    "title", "description", "tags", "price", "currency",
    "category_path", "materials", "who_made", "when_made",
    "is_digital", "seo_keywords",
]

# Keyword suggestions by niche (used when keywords appear missing)
NICHE_KEYWORD_HINTS = {
    "diy": [
        "DIY repair guide", "home repair PDF", "fix it yourself", "repair tutorial",
        "instant download", "printable guide", "step by step repair",
    ],
    "survival": [
        "emergency kit", "survival guide PDF", "preparedness checklist",
        "72 hour kit", "home emergency plan", "disaster prep",
    ],
    "budget": [
        "budget home repair", "save money DIY", "cheap repairs", "frugal home",
        "affordable renovation", "DIY savings guide",
    ],
    "nl": [
        "digitale download", "direct downloaden", "printbare gids",
        "klussen thuis", "huisreparatie", "besparen",
    ],
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_template(path: Path) -> dict | None:
    """Load and parse a JSON listing template. Returns None on error."""
    try:
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError) as exc:
        return None


def validate_template(name: str, data: dict) -> list[str]:
    """
    Validate a listing template against Etsy SEO requirements.
    Returns a list of issue strings (empty list = all good).
    """
    issues: list[str] = []

    # --- Required fields ---
    for field in REQUIRED_FIELDS:
        if field not in data:
            issues.append(f"MISSING FIELD: '{field}'")

    # --- Title ---
    title = data.get("title", "")
    if not title:
        issues.append("TITLE: empty")
    elif len(title) > TITLE_MAX_CHARS:
        issues.append(
            f"TITLE TOO LONG: {len(title)} chars (max {TITLE_MAX_CHARS})"
        )

    # --- Tags ---
    tags = data.get("tags", [])
    if not isinstance(tags, list):
        issues.append("TAGS: must be a list")
    else:
        if len(tags) < TAG_REQUIRED_COUNT:
            issues.append(
                f"TOO FEW TAGS: {len(tags)} (minimum {TAG_REQUIRED_COUNT})"
            )
        for tag in tags:
            if len(tag) > TAG_MAX_CHARS:
                issues.append(
                    f"TAG TOO LONG: '{tag}' ({len(tag)} chars, max {TAG_MAX_CHARS})"
                )

    # --- Description ---
    description = data.get("description", "")
    if len(description) < DESCRIPTION_MIN_CHARS:
        issues.append(
            f"DESCRIPTION TOO SHORT: {len(description)} chars (min {DESCRIPTION_MIN_CHARS})"
        )

    # --- Price ---
    price = data.get("price")
    if price is None:
        issues.append("PRICE: missing")
    elif not isinstance(price, (int, float)) or price <= 0:
        issues.append(f"PRICE: invalid value '{price}'")

    # --- Boolean / string fields ---
    if data.get("is_digital") is not True:
        issues.append("IS_DIGITAL: should be true for digital products")
    if data.get("who_made") != "i_did":
        issues.append("WHO_MADE: expected 'i_did'")

    return issues


def suggest_keywords(data: dict) -> list[str]:
    """
    Return a list of suggested keywords that may be missing from the listing.
    """
    existing_text = " ".join([
        data.get("title", ""),
        data.get("description", ""),
        " ".join(data.get("tags", [])),
        " ".join(data.get("seo_keywords", {}).get("primary", [])),
        " ".join(data.get("seo_keywords", {}).get("secondary", [])),
    ]).lower()

    suggestions: list[str] = []
    for niche, keywords in NICHE_KEYWORD_HINTS.items():
        for kw in keywords:
            if kw.lower() not in existing_text:
                suggestions.append(f"[{niche}] {kw}")

    return suggestions


def format_report(results: list[dict]) -> str:
    """Format the full optimization report as a human-readable string."""
    lines: list[str] = []
    lines.append("=" * 60)
    lines.append("ETSY LISTING OPTIMIZATION REPORT")
    lines.append("=" * 60)

    total = len(results)
    passed = sum(1 for r in results if not r["issues"])
    failed = total - passed

    lines.append(f"Templates checked : {total}")
    lines.append(f"Passed            : {passed}")
    lines.append(f"Failed / warnings : {failed}")
    lines.append("")

    for result in results:
        status = "✅ PASS" if not result["issues"] else "⚠️  ISSUES"
        lines.append(f"{'─' * 60}")
        lines.append(f"{status}  {result['name']}")
        lines.append(f"  Title ({result['title_len']} chars): {result['title'][:80]}{'…' if result['title_len'] > 80 else ''}")
        lines.append(f"  Description   : {result['desc_len']} chars")
        lines.append(f"  Tags          : {result['tag_count']}")
        lines.append(f"  Price         : {result.get('currency', 'EUR')} {result.get('price', '?')}")

        if result["issues"]:
            lines.append("  Issues:")
            for issue in result["issues"]:
                lines.append(f"    ❌ {issue}")

        if result["suggestions"]:
            lines.append("  Keyword suggestions (consider adding):")
            for sug in result["suggestions"][:5]:
                lines.append(f"    💡 {sug}")

        lines.append("")

    lines.append("=" * 60)
    lines.append("END OF REPORT")
    lines.append("=" * 60)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate Etsy listing templates and generate an SEO optimization report."
    )
    parser.add_argument(
        "--templates-dir",
        default=Path(__file__).parent / "listing_templates",
        type=Path,
        help="Directory containing listing JSON templates (default: listing_templates/)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Write report to this file instead of stdout",
    )
    args = parser.parse_args()

    templates_dir = Path(args.templates_dir)
    if not templates_dir.is_dir():
        print(f"ERROR: templates directory not found: {templates_dir}", file=sys.stderr)
        sys.exit(1)

    json_files = sorted(templates_dir.glob("*.json"))
    if not json_files:
        print(f"ERROR: no JSON files found in {templates_dir}", file=sys.stderr)
        sys.exit(1)

    results: list[dict] = []
    load_errors: list[str] = []

    for path in json_files:
        data = load_template(path)
        if data is None:
            load_errors.append(str(path))
            continue

        issues = validate_template(path.stem, data)
        suggestions = suggest_keywords(data)

        results.append(
            {
                "name": path.stem,
                "title": data.get("title", ""),
                "title_len": len(data.get("title", "")),
                "desc_len": len(data.get("description", "")),
                "tag_count": len(data.get("tags", [])),
                "price": data.get("price"),
                "currency": data.get("currency", "EUR"),
                "issues": issues,
                "suggestions": suggestions,
            }
        )

    if load_errors:
        print("WARNING: Could not load the following files:", file=sys.stderr)
        for p in load_errors:
            print(f"  {p}", file=sys.stderr)

    report = format_report(results)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"Report written to: {args.output}")
    else:
        print(report)

    # Exit 1 if any template has issues
    if any(r["issues"] for r in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
