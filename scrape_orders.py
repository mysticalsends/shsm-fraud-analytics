#!/usr/bin/env python3
"""
SEC Final Orders Scraper
=========================
Scrapes the SEC whistleblower final orders page and writes
data/sec_final_orders.json (used by sec_macro_dashboard.html).

Usage:
    python scrape_orders.py

Requirements:
    pip install curl_cffi beautifulsoup4
"""

try:
    from curl_cffi import requests
except ImportError:
    print("Missing dependency. Run: .venv/Scripts/pip install curl_cffi beautifulsoup4")
    import sys; sys.exit(1)

from bs4 import BeautifulSoup
from collections import defaultdict
import re, time, json
from pathlib import Path

ORDERS_URL = (
    "https://www.sec.gov/enforcement-litigation/whistleblower-program/"
    "final-orders-whistleblower-award-determinations"
)

# The page title text contains "Award" or "Denial" — these are the keywords
# used to classify each order row.
AWARD_KEYWORDS  = re.compile(r'\baward\b', re.IGNORECASE)
DENIAL_KEYWORDS = re.compile(r'\bden(ial|ied)\b', re.IGNORECASE)


def fetch_page(page_num):
    url = ORDERS_URL if page_num == 0 else f"{ORDERS_URL}?page={page_num}"
    headers = {"Referer": ORDERS_URL} if page_num > 0 else {}
    resp = requests.get(url, impersonate="chrome120", headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.text


def get_total_pages(html):
    m = re.search(r"of\s+([\d,]+)\s+items", html, re.IGNORECASE)
    if m:
        total = int(m.group(1).replace(",", ""))
        # The SEC orders page uses 25 items per page (not 100 like NOCAs)
        per_page = 25
        return (total + per_page - 1) // per_page
    pages = re.findall(r'[?&]page=(\d+)', html)
    return max((int(p) for p in pages), default=0) + 1


def parse_orders(html):
    """
    Parse a single page of the final orders listing.
    Returns a list of dicts: {date, year_month, type}
    where type is 'award' or 'denial'.
    """
    soup = BeautifulSoup(html, "html.parser")
    results = []

    for row in soup.select("table tr"):
        cells = row.find_all("td")
        if len(cells) < 2:
            continue

        # Row text — combine all cells for classification
        row_text = " ".join(c.get_text(" ", strip=True) for c in cells)

        # Date: look for MM/DD/YYYY pattern in any cell
        date_match = re.search(r"(\d{2})/(\d{2})/(\d{4})", row_text)
        if not date_match:
            continue
        mm, dd, yyyy = date_match.group(1), date_match.group(2), date_match.group(3)
        year = int(yyyy)
        if not (2011 <= year <= 2030):
            continue
        year_month = f"{yyyy}-{mm}"

        # Classify as award or denial based on row text
        is_award  = bool(AWARD_KEYWORDS.search(row_text))
        is_denial = bool(DENIAL_KEYWORDS.search(row_text))

        if is_award and not is_denial:
            order_type = "award"
        elif is_denial and not is_award:
            order_type = "denial"
        elif is_denial and is_award:
            # Both keywords present — "denial of award" means denial
            order_type = "denial"
        else:
            # Can't classify — skip and warn
            print(f"  WARN: could not classify row: {row_text[:120]}")
            continue

        results.append({"year_month": year_month, "type": order_type, "date": f"{yyyy}-{mm}-{dd}"})

    return results


def scrape_all():
    all_orders = []
    print("Fetching page 1...", end=" ", flush=True)
    html0 = fetch_page(0)
    page0 = parse_orders(html0)
    total_pages = get_total_pages(html0)
    all_orders.extend(page0)
    print(f"{len(page0)} orders.  Total pages: {total_pages}")

    for p in range(1, total_pages):
        try:
            print(f"  Page {p+1}/{total_pages}...", end=" ", flush=True)
            html = fetch_page(p)
            recs = parse_orders(html)
            all_orders.extend(recs)
            print(f"{len(recs)} orders  (running total: {len(all_orders)})")
        except Exception as e:
            print(f"FAILED: {e}")
        time.sleep(0.4)

    return all_orders


def build_monthly_maps(orders):
    awards  = defaultdict(int)
    denials = defaultdict(int)
    for o in orders:
        if o["type"] == "award":
            awards[o["year_month"]] += 1
        else:
            denials[o["year_month"]] += 1
    return dict(sorted(awards.items())), dict(sorted(denials.items()))


def main():
    print("=" * 55)
    print("  SEC Final Orders Scraper")
    print("=" * 55)
    print()

    orders = scrape_all()

    awards_map, denials_map = build_monthly_maps(orders)

    total_awards  = sum(awards_map.values())
    total_denials = sum(denials_map.values())
    total         = total_awards + total_denials

    print(f"\n--- Results ---")
    print(f"  Awards:  {total_awards}")
    print(f"  Denials: {total_denials}")
    print(f"  Total:   {total}")
    print()

    from datetime import datetime, timezone
    out_json = Path(__file__).parent / "data" / "sec_final_orders.json"
    out_json.parent.mkdir(exist_ok=True)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({
            "description": "SEC whistleblower final order counts (awards and denials) by month",
            "generatedAt": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            "totalAwards":  total_awards,
            "totalDenials": total_denials,
            "awardsMonthly":  awards_map,
            "denialsMonthly": denials_map,
        }, f, ensure_ascii=False, separators=(',', ':'))
    size_kb = out_json.stat().st_size // 1024
    print(f"Saved {out_json.relative_to(Path(__file__).parent)}  ({size_kb} KB)")


if __name__ == "__main__":
    main()
