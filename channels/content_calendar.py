#!/usr/bin/env python3
"""
content_calendar.py – Generate a 30-day content calendar for HomeFixTips EN channels.

Outputs a CSV compatible with Later.com import format.

Usage:
    python content_calendar.py --month 3 --year 2026
    python content_calendar.py --month 3 --year 2026 --niches diy survival budget
    python content_calendar.py --month 3 --year 2026 --output my_calendar.csv
"""

import argparse
import calendar
import csv
import itertools
import sys
from datetime import date, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Content database
# ---------------------------------------------------------------------------

CONTENT_IDEAS = {
    "diy": [
        ("Fix a leaky faucet in 5 minutes", "🔧 Stop that drip today – no plumber needed!"),
        ("Repair a cabinet hinge", "🪛 Broken cabinet? Back on track in 10 minutes."),
        ("Patch a hole in drywall", "🖼️ Invisible repair – step by step."),
        ("Re-caulk your bathtub", "🛁 Fresh caulk = no more mould. Here's how."),
        ("Fix a running toilet", "🚽 Save water and money in under 20 minutes."),
        ("Replace a door handle", "🚪 New handle, new look – takes 10 minutes."),
        ("Silence a squeaky floor", "👣 No more squeaks – simple fix from below."),
        ("Fix a sticking door", "🔑 Why doors stick and how to fix it fast."),
        ("Replace a light switch", "💡 Safe, simple, and totally DIY."),
        ("Repair a window screen", "🪟 Keep bugs out – patch a screen in minutes."),
    ],
    "survival": [
        ("Build a 72-hour home emergency kit", "🛡️ Be ready before disaster strikes."),
        ("How to shut off your main water valve", "💧 Know this before a pipe bursts."),
        ("Emergency power outage checklist", "🔦 What to do when the lights go out."),
        ("How to reset a tripped circuit breaker", "⚡ Safe steps everyone should know."),
        ("Temporary roof leak repair", "☔ Stop water damage fast – emergency fix."),
        ("Winterize your pipes in 30 minutes", "🌡️ Prevent freezing before it happens."),
        ("How to use a fire extinguisher", "🧯 PASS method explained – must-know skill."),
        ("Detect a gas leak at home", "⚠️ Signs, steps, and when to evacuate."),
        ("Emergency door lock if key breaks", "🔐 Stay secure after a broken lock."),
        ("Flood proofing your home on a budget", "🌊 Simple barriers that actually work."),
    ],
    "budget": [
        ("5 home repairs under €10", "💶 Big fixes, tiny budget – here's how."),
        ("Paint a room for under €25", "🎨 Pro results without the pro price tag."),
        ("Cheap tools that actually work", "🛒 Budget buys that hold up on real jobs."),
        ("Save on heating: seal air leaks", "🌬️ DIY draught proofing saves hundreds."),
        ("Refurbish old furniture instead of buying", "🪑 Upcycle in an afternoon – looks brand new."),
        ("Free materials for home repair", "♻️ Where to find good stuff for nothing."),
        ("DIY tile repair for under €15", "🧱 Fix cracked tiles without a tradesman."),
        ("Lower your water bill with one fix", "💧 One simple change = instant savings."),
        ("Budget weekend project: garden fence", "🌿 Build it yourself for a fraction of the cost."),
        ("Cheap weatherproofing that lasts", "🏠 Keep heat in, bills down."),
    ],
}

# Optimal posting times per platform (local time strings)
POSTING_TIMES = {
    "youtube":   ["09:00", "15:00", "20:00"],
    "tiktok":    ["07:00", "12:00", "19:00"],
    "instagram": ["08:00", "13:00", "20:00"],
}

# Later.com CSV column headers
LATER_HEADERS = [
    "Date",
    "Time",
    "Platform",
    "Caption",
    "Niche",
    "Topic",
    "Hook",
    "Hashtags",
    "Media_Placeholder",
]

HASHTAGS_BY_NICHE = {
    "diy": "#HomeRepair #DIY #FixItYourself #HandymanTips #HomeImprovement #QuickFix #HomeFixTips #BudgetDIY",
    "survival": "#SurvivalSkills #EmergencyPrep #HomeEmergency #Preparedness #SurvivalHacks #HomeFixTips #EmergencyKit",
    "budget": "#BudgetDIY #SaveMoney #FrugalLiving #AffordableDIY #HomeOnABudget #HomeFixTips #DIYForLess",
}


def iter_niches(niches: list[str]):
    """Cycle through the requested niches indefinitely."""
    return itertools.cycle(niches)


def build_calendar(month: int, year: int, niches: list[str]) -> list[dict]:
    """Return a list of row dicts for the 30-day calendar."""
    rows: list[dict] = []

    _, days_in_month = calendar.monthrange(year, month)
    niche_cycle = iter_niches(niches)

    # Track per-niche idea indices so we rotate through ideas
    idea_indices: dict[str, int] = {n: 0 for n in niches}

    for day_num in range(1, min(days_in_month, 30) + 1):
        current_date = date(year, month, day_num)
        niche = next(niche_cycle)
        ideas = CONTENT_IDEAS.get(niche, CONTENT_IDEAS["diy"])
        idx = idea_indices[niche] % len(ideas)
        topic, hook = ideas[idx]
        idea_indices[niche] += 1

        hashtags = HASHTAGS_BY_NICHE.get(niche, "")

        for platform, times in POSTING_TIMES.items():
            # Each day gets one post per platform; use a different time slot per day
            time_slot = times[(day_num - 1) % len(times)]
            caption = f"{hook}\n\n{topic}\n\n{hashtags}"
            rows.append(
                {
                    "Date": current_date.strftime("%Y-%m-%d"),
                    "Time": time_slot,
                    "Platform": platform,
                    "Caption": caption,
                    "Niche": niche,
                    "Topic": topic,
                    "Hook": hook,
                    "Hashtags": hashtags,
                    "Media_Placeholder": f"video_{current_date.strftime('%Y%m%d')}_{platform}.mp4",
                }
            )

    return rows


def write_csv(rows: list[dict], output_path: Path) -> None:
    """Write rows to a CSV file."""
    with output_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=LATER_HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a 30-day content calendar (CSV) for HomeFixTips EN channels."
    )
    parser.add_argument(
        "--month",
        type=int,
        required=True,
        choices=range(1, 13),
        metavar="MONTH",
        help="Month number (1–12)",
    )
    parser.add_argument(
        "--year",
        type=int,
        required=True,
        help="Four-digit year (e.g. 2026)",
    )
    parser.add_argument(
        "--niches",
        nargs="+",
        default=["diy", "survival", "budget"],
        choices=list(CONTENT_IDEAS.keys()),
        help="Niches to include, in rotation order (default: diy survival budget)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output CSV file path (default: content_calendar_YYYY_MM.csv)",
    )
    args = parser.parse_args()

    if args.year < 2000 or args.year > 2100:
        print("ERROR: --year must be between 2000 and 2100.", file=sys.stderr)
        sys.exit(1)

    output_path = Path(
        args.output
        if args.output
        else f"content_calendar_{args.year}_{args.month:02d}.csv"
    )

    rows = build_calendar(args.month, args.year, args.niches)
    write_csv(rows, output_path)

    print(f"✅ Calendar generated: {output_path} ({len(rows)} rows)")
    print(f"   Month  : {calendar.month_name[args.month]} {args.year}")
    print(f"   Niches : {', '.join(args.niches)}")
    print(f"   Days   : {len(rows) // len(POSTING_TIMES)} days × {len(POSTING_TIMES)} platforms")


if __name__ == "__main__":
    main()
