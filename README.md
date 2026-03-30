# SHSM Fraud Analytics Dashboard Suite

Interactive data dashboards covering SEC whistleblower enforcement and DOJ False Claims Act fraud recoveries, built for Sanford Heisler Sharp McKnight.

**Live site:** https://mysticalsends.github.io/shsm-fraud-analytics/

---

## Dashboards

### [DOJ Federal Fraud Recovery](doj_fraud_dashboard.html)
Annual FCA settlements and judgments by agency (HHS, DOD, Other) from FY1987–2025. Stacked/grouped bar charts, trend lines, donut breakdowns, and qui tam relator award data. $85.7B tracked across 39 fiscal years.

### [DOJ Health Care Fraud — CY2024](DOJ_Health_Care_Fraud_Recoveries_2024.html)
Case-level breakdown of 122 individual FCA health care cases announced by DOJ in calendar year 2024. Filterable and sortable by fraud type, defendant type, and federal program. Sourced from DOJ press releases.

### [SEC Whistleblower Program Analysis](sec_macro_dashboard.html)
Comprehensive view of SEC enforcement from 2011–2026: 2,479 Notices of Covered Actions and 996 final award/denial orders. Broken down by SEC Commissioner and Presidential Administration, with a tips pipeline chart and dynamic summary of findings.

---

## Structure

```
├── index.html                          # Dashboard hub / home page
├── doj_fraud_dashboard.html
├── DOJ_Health_Care_Fraud_Recoveries_2024.html
├── sec_macro_dashboard.html
├── blog_dashboard_overview.html        # Methodology & findings write-up
├── css/
│   ├── shared.css                      # Shared dark-navy design system
│   └── blog.css
├── data/
│   ├── sec_macro.json                  # NOCA monthly counts + tips data
│   ├── sec_final_orders.json           # Award/denial order counts by month
│   ├── sec_commissioners.json          # SEC chair periods + colors
│   ├── us_presidents.json              # Presidential periods + colors
│   ├── doj_fca.json                    # FCA annual recovery data
│   └── doj_hc_cy2024.json             # CY2024 health care case data
├── js/
│   └── chart-utils.js
└── run_dashboard.py                    # Data refresh utility (SEC NOCAs)
```

## Tech Stack

- **Charts:** Chart.js 4.4.1 (CDN)
- **Framework:** Pure HTML + vanilla JavaScript — no build step, no server required for most pages
- **Fonts:** Playfair Display + Space Mono (Google Fonts)
- **Data:** JSON files loaded asynchronously — requires a local server (`python -m http.server 8080`) or the live GitHub Pages URL to run locally

## Data Sources

| Dataset | Source |
|---|---|
| FCA annual recoveries | [DOJ Civil Division — Fraud Statistics](https://www.justice.gov/civil/false-claims-act) |
| FCA CY2024 health care cases | DOJ press releases (justice.gov) |
| SEC Notices of Covered Action | [SEC Whistleblower Program](https://www.sec.gov/enforcement-litigation/whistleblower-program/whistleblower-program-notices-covered-action) |
| SEC Final Orders | [SEC Final Orders page](https://www.sec.gov/enforcement-litigation/whistleblower-program/final-orders-whistleblower-award-determinations) |
| SEC tips pipeline | [SEC Annual Reports to Congress](https://www.sec.gov/whistleblower/annual-reports) |

---

*Sanford Heisler Sharp McKnight — Analytics & Data · March 2026*
