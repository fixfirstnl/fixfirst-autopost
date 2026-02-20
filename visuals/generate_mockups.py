#!/usr/bin/env python3
"""Generate product mockup HTML pages for Gumroad-ready previews.

Usage
-----
python visuals/generate_mockups.py
python visuals/generate_mockups.py --cover-dir /path/to/covers --output-dir output/mockups
python visuals/generate_mockups.py --product survival_basis_gids_nl
"""

import argparse
import json
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
COVER_PROMPTS_FILE = Path(__file__).resolve().parent / "cover_prompts.json"
DEFAULT_COVER_DIR = REPO_ROOT / "output" / "covers"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "output" / "mockups"

# ---------------------------------------------------------------------------
# HTML template
# ---------------------------------------------------------------------------
_PAGE_TEMPLATE = """\
<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} – Productpreview</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: 'Segoe UI', Arial, sans-serif;
      background: {bg_color};
      color: {text_color};
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 40px 20px;
    }}
    .container {{
      max-width: 960px;
      width: 100%;
    }}
    .hero {{
      display: flex;
      gap: 40px;
      align-items: flex-start;
      flex-wrap: wrap;
      margin-bottom: 48px;
    }}
    .cover-wrapper {{
      flex: 0 0 340px;
    }}
    .cover-wrapper img {{
      width: 100%;
      border-radius: 12px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.30);
    }}
    .cover-placeholder {{
      width: 340px;
      height: 191px;  /* 16:9 */
      background: {placeholder_bg};
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: {placeholder_text};
      font-size: 14px;
      text-align: center;
      padding: 16px;
    }}
    .info {{
      flex: 1 1 280px;
    }}
    .badge {{
      display: inline-block;
      background: {badge_color};
      color: #fff;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 1px;
      text-transform: uppercase;
      padding: 4px 12px;
      border-radius: 4px;
      margin-bottom: 12px;
    }}
    h1 {{
      font-size: 2rem;
      margin: 0 0 12px;
      color: {heading_color};
    }}
    .subheadline {{
      font-size: 1.1rem;
      margin-bottom: 20px;
      opacity: 0.85;
    }}
    .price-block {{
      margin-bottom: 24px;
    }}
    .price {{
      font-size: 2rem;
      font-weight: 700;
      color: {price_color};
    }}
    .price-original {{
      font-size: 1.1rem;
      text-decoration: line-through;
      opacity: 0.55;
      margin-left: 8px;
    }}
    .cta-btn {{
      display: inline-block;
      background: {cta_bg};
      color: {cta_text};
      font-size: 1.1rem;
      font-weight: 700;
      text-decoration: none;
      padding: 14px 36px;
      border-radius: 8px;
      transition: opacity 0.2s;
    }}
    .cta-btn:hover {{ opacity: 0.88; }}
    .features {{
      margin-top: 40px;
    }}
    .features h2 {{
      font-size: 1.4rem;
      margin-bottom: 16px;
      color: {heading_color};
    }}
    .features ul {{
      padding: 0;
      list-style: none;
      margin: 0;
    }}
    .features li {{
      padding: 8px 0;
      border-bottom: 1px solid {divider_color};
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .features li::before {{
      content: '✓';
      color: {check_color};
      font-weight: 700;
      flex-shrink: 0;
    }}
    footer {{
      margin-top: 60px;
      text-align: center;
      font-size: 0.85rem;
      opacity: 0.55;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="hero">
      <div class="cover-wrapper">
        {cover_html}
      </div>
      <div class="info">
        <span class="badge">{badge}</span>
        <h1>{title}</h1>
        <p class="subheadline">{subheadline}</p>
        <div class="price-block">
          <span class="price">&euro;{price}</span>
          <span class="price-original">&euro;{price_original}</span>
        </div>
        <a href="{gumroad_url}" class="cta-btn">{cta_label}</a>
      </div>
    </div>
    <div class="features">
      <h2>Wat zit er in?</h2>
      <ul>
        {feature_items}
      </ul>
    </div>
  </div>
  <footer>
    &copy; FixFirst NL &mdash; fixfirst.nl
  </footer>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# Product catalogue – extend or override via cover_prompts.json
# ---------------------------------------------------------------------------
PRODUCT_DEFAULTS: dict[str, dict] = {
    "survival_basis_gids_nl": {
        "subheadline": "Alles wat je moet weten om te overleven in elke situatie",
        "price": "12.95",
        "price_original": "24.95",
        "badge": "BESTSELLER",
        "badge_color": "#FF4500",
        "bg_color": "#1a2a1a",
        "text_color": "#e8f5e9",
        "heading_color": "#f5c518",
        "placeholder_bg": "#2d4a2d",
        "placeholder_text": "#90a490",
        "price_color": "#f5c518",
        "cta_bg": "#f5c518",
        "cta_text": "#1a2a1a",
        "cta_label": "Nu downloaden",
        "divider_color": "rgba(255,255,255,0.12)",
        "check_color": "#69f069",
        "gumroad_url": "https://fixfirstnl.gumroad.com/l/survival-basis-gids-nl",
        "features": [
            "Meer dan 80 pagina's praktische overlevingstips",
            "Waterfiltratie, vuur maken en schuilplaats bouwen",
            "EHBO-gids voor noodsituaties",
            "Voedsel vinden en bewaren in de natuur",
            "Printklaar PDF formaat",
        ],
    },
    "emergency_toolkit_pro": {
        "subheadline": "Jouw complete gids voor elke noodsituatie thuis en onderweg",
        "price": "9.95",
        "price_original": "19.95",
        "badge": "NIEUW",
        "badge_color": "#cc0000",
        "bg_color": "#1c0a0a",
        "text_color": "#ffebee",
        "heading_color": "#ff5252",
        "placeholder_bg": "#3d1515",
        "placeholder_text": "#a07070",
        "price_color": "#ff5252",
        "cta_bg": "#e53935",
        "cta_text": "#ffffff",
        "cta_label": "Bestel nu",
        "divider_color": "rgba(255,255,255,0.10)",
        "check_color": "#ff8a80",
        "gumroad_url": "https://fixfirstnl.gumroad.com/l/emergency-toolkit-pro",
        "features": [
            "Complete checklist voor noodpakket thuis",
            "72-uurs overlevingsplan voor het hele gezin",
            "Eerste hulp bij stroomuitval, overstroming en brand",
            "Bewaren van noodvoorraden – stap voor stap",
            "Printklaar PDF + invulformulieren",
        ],
    },
    "weekend_klusplanner": {
        "subheadline": "Plan en klaar je klussen slim – elke zaterdag als een professional",
        "price": "7.95",
        "price_original": "14.95",
        "badge": "GRATIS UPDATE",
        "badge_color": "#0066cc",
        "bg_color": "#f0f6ff",
        "text_color": "#1a3a6b",
        "heading_color": "#1a3a6b",
        "placeholder_bg": "#d0e4ff",
        "placeholder_text": "#6080a0",
        "price_color": "#0066cc",
        "cta_bg": "#0066cc",
        "cta_text": "#ffffff",
        "cta_label": "Download de planner",
        "divider_color": "rgba(0,0,0,0.08)",
        "check_color": "#0066cc",
        "gumroad_url": "https://fixfirstnl.gumroad.com/l/weekend-klusplanner",
        "features": [
            "52-weekse klusplanner met seizoenskalender",
            "Materiaalinkooplijsten per klus",
            "Tijdschattingen en budget-tracker",
            "Tips voor de populairste 30 klusjes",
            "Digitaal invulbaar + printklaar",
        ],
    },
    "budget_bespaar_gids": {
        "subheadline": "Bespaar honderden euro's per maand zonder in te leveren op comfort",
        "price": "8.95",
        "price_original": "17.95",
        "badge": "TOP VERKOPER",
        "badge_color": "#2e7d32",
        "bg_color": "#f1f8f1",
        "text_color": "#1b3a1b",
        "heading_color": "#1b5e20",
        "placeholder_bg": "#c8e6c9",
        "placeholder_text": "#558b55",
        "price_color": "#2e7d32",
        "cta_bg": "#2e7d32",
        "cta_text": "#ffffff",
        "cta_label": "Start met besparen",
        "divider_color": "rgba(0,0,0,0.08)",
        "check_color": "#2e7d32",
        "gumroad_url": "https://fixfirstnl.gumroad.com/l/budget-bespaar-gids",
        "features": [
            "50+ bewezen tips om direct op te bezuinigen",
            "Maandelijkse budgettemplate (Excel + PDF)",
            "Energiebesparing: €200+ per jaar",
            "Boodschappen-hacken: slimmer en goedkoper",
            "Schulden aflossen met de sneeuwbalmethode",
        ],
    },
    "diy_keukenkast_reparatie_gids": {
        "subheadline": "Repareer je keuken als een professional – zonder dure vakman",
        "price": "9.95",
        "price_original": "18.95",
        "badge": "STAP VOOR STAP",
        "badge_color": "#795548",
        "bg_color": "#fdf6f0",
        "text_color": "#3e2723",
        "heading_color": "#4e342e",
        "placeholder_bg": "#d7ccc8",
        "placeholder_text": "#8d6e63",
        "price_color": "#795548",
        "cta_bg": "#795548",
        "cta_text": "#ffffff",
        "cta_label": "Bekijk de gids",
        "divider_color": "rgba(0,0,0,0.08)",
        "check_color": "#795548",
        "gumroad_url": "https://fixfirstnl.gumroad.com/l/diy-keukenkast-reparatie-gids",
        "features": [
            "Scharnier vervangen in 10 minuten",
            "Kast-deuren schilderen zonder strepen",
            "Laden repareren en verstellen",
            "Werkblad krassen verwijderen",
            "Meer dan 60 foto's en illustraties",
        ],
    },
}


def _build_cover_html(product_id: str, cover_dir: Path, title: str, placeholder_bg: str, placeholder_text: str) -> str:
    """Return an <img> tag if a cover file exists, otherwise a placeholder div."""
    for ext in ("png", "jpg", "jpeg", "webp"):
        candidate = cover_dir / f"{product_id}.{ext}"
        if candidate.exists():
            rel = os.path.relpath(candidate)
            return f'<img src="{rel}" alt="{title} cover" />'
    # Fallback placeholder
    return (
        f'<div class="cover-placeholder" '
        f'style="background:{placeholder_bg};color:{placeholder_text};">'
        f'Cover afbeelding<br/>(plaats {product_id}.png in {cover_dir})'
        f"</div>"
    )


def _render_mockup(product_id: str, meta: dict, cover_dir: Path, output_dir: Path) -> Path:
    """Render one HTML mockup and return the output path."""
    title = meta["title"]
    defaults = PRODUCT_DEFAULTS.get(product_id, {})

    cover_html = _build_cover_html(
        product_id,
        cover_dir,
        title,
        defaults.get("placeholder_bg", "#cccccc"),
        defaults.get("placeholder_text", "#666666"),
    )

    feature_items = "\n        ".join(
        f"<li>{f}</li>" for f in defaults.get("features", ["Zie productpagina voor details."])
    )

    html = _PAGE_TEMPLATE.format(
        title=title,
        subheadline=defaults.get("subheadline", ""),
        price=defaults.get("price", "9.95"),
        price_original=defaults.get("price_original", "19.95"),
        badge=defaults.get("badge", ""),
        badge_color=defaults.get("badge_color", "#333333"),
        bg_color=defaults.get("bg_color", "#ffffff"),
        text_color=defaults.get("text_color", "#212121"),
        heading_color=defaults.get("heading_color", "#000000"),
        placeholder_bg=defaults.get("placeholder_bg", "#cccccc"),
        placeholder_text=defaults.get("placeholder_text", "#666666"),
        price_color=defaults.get("price_color", "#000000"),
        cta_bg=defaults.get("cta_bg", "#333333"),
        cta_text=defaults.get("cta_text", "#ffffff"),
        cta_label=defaults.get("cta_label", "Kopen"),
        divider_color=defaults.get("divider_color", "rgba(0,0,0,0.10)"),
        check_color=defaults.get("check_color", "#43a047"),
        gumroad_url=defaults.get("gumroad_url", "#"),
        cover_html=cover_html,
        feature_items=feature_items,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"{product_id}.html"
    out_path.write_text(html, encoding="utf-8")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Gumroad-ready product mockup HTML pages."
    )
    parser.add_argument(
        "--cover-dir",
        default=str(DEFAULT_COVER_DIR),
        help=f"Directory containing product cover images (default: {DEFAULT_COVER_DIR})",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help=f"Output directory for generated HTML files (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--product",
        default=None,
        help="Generate mockup for a single product ID only (default: all products)",
    )
    args = parser.parse_args()

    cover_dir = Path(args.cover_dir)
    output_dir = Path(args.output_dir)

    # Load product list from cover_prompts.json
    with open(COVER_PROMPTS_FILE, encoding="utf-8") as fh:
        prompts_data = json.load(fh)

    products = prompts_data.get("products", [])
    if not products:
        print("No products found in cover_prompts.json", file=sys.stderr)
        sys.exit(1)

    generated = []
    for product in products:
        pid = product["id"]
        if args.product and pid != args.product:
            continue
        out_path = _render_mockup(pid, product, cover_dir, output_dir)
        print(f"✓  {pid}  →  {out_path}")
        generated.append(out_path)

    if not generated:
        print(f"No products matched filter '{args.product}'", file=sys.stderr)
        sys.exit(1)

    print(f"\n{len(generated)} mockup(s) written to {output_dir}")


if __name__ == "__main__":
    main()
