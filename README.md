# 🏭 Manufacturing Downtime Analytics — Power BI Portfolio Project

An end-to-end business intelligence project analyzing equipment downtime,
repair cost, and production impact across a 4-plant manufacturing
network, built as a data analyst portfolio piece.

![Executive Overview](images/01_executive_overview.png)

## 📌 Project Summary

This project simulates a real-world manufacturing analytics engagement:
a synthetic-but-realistic downtime event log (4,200 records, Jan 2023 –
Dec 2024, 4 European plants) is modeled into a proper Power BI star
schema, enriched with a DAX measure library, and visualized across three
report pages covering executive KPIs, deep-dive root-cause analysis, and
written business recommendations.

**Why this project exists:** it's designed to demonstrate the full
skillset a manufacturing/operations data analyst role expects — data
modeling, DAX, dashboard design, and the ability to translate numbers
into business recommendations — in a single, coherent, interview-ready
package.

## 🧰 Tech / Skills Demonstrated

- Data modeling (star schema: fact + date + machine dimensions)
- DAX (base measures, ratios, time intelligence, RANKX/Pareto patterns)
- Power BI dashboard design (dark/industrial theme, KPI cards, slicers)
- Root-cause & Pareto analysis
- Business storytelling / executive summary writing

## 📂 Repository Structure

```
├── README.md                          ← you are here
├── data/
│   ├── Manufacturing_Downtime_Dataset.xlsx   ← Power BI source (Fact + Dims + Data Dictionary)
│   └── manufacturing_downtime_data.csv       ← raw flat export of the fact table
├── docs/
│   ├── Data_Model.md                  ← star schema, relationships, setup steps
│   ├── DAX_Measures.md                ← full DAX measure library (copy-paste ready)
│   └── Business_Recommendations.md    ← written executive findings & recommendations
├── images/
│   ├── 01_executive_overview.png      ← Page 1 screenshot: KPIs + core visuals
│   ├── 02_deep_dive_analytics.png     ← Page 2 screenshot: Pareto, heatmap, waterfall, scatter, treemap
│   └── 03_executive_insights.png      ← Page 3 screenshot: findings & recommendations
└── scripts/
    ├── generate_data.py               ← synthetic dataset generator
    ├── build_excel.py                 ← builds the Power BI-ready workbook
    ├── dashboard_overview.py          ← renders Page 1 screenshot
    ├── dashboard_analytics.py         ← renders Page 2 screenshot
    └── dashboard_insights.py          ← renders Page 3 screenshot
```

> **A note on the `.pbix` file:** this project was built in a sandboxed
> environment without Power BI Desktop installed, so no live `.pbix` file
> ships in this repo. Everything needed to rebuild the actual report in
> ~20–30 minutes is included: the ready-to-import Excel data model, the
> complete DAX measure library, the data-model/relationship spec, and
> pixel-accurate mockups of every report page to build against. See
> **Rebuilding the Report in Power BI Desktop** below.

## 📊 The Dataset

4,200 downtime events across 4 plants, 8 machine types, and 3 shifts,
covering **Plant A – Stuttgart**, **Plant B – Lyon**, **Plant C –
Katowice**, and **Plant D – Bratislava**.

| Column | Description |
|---|---|
| Date, Year, Month, Month Number, Week | Time attributes |
| Plant, Production Line, Machine ID, Machine Type | Location/asset attributes |
| Shift, Operator ID, Technician | Workforce attributes |
| Downtime Category, Downtime Reason, Root Cause | Root-cause taxonomy |
| Planned or Unplanned, Maintenance Type | Maintenance classification |
| Downtime Minutes, Downtime Hours | Event duration |
| Repair Cost EURO, Cost per Minute | Financial impact |
| Production Units Lost | Production impact |
| Product Type | Product running on the line |
| Status, Resolution Time | Case management |

Full data dictionary: see the `Data_Dictionary` sheet in
`Manufacturing_Downtime_Dataset.xlsx`, or `docs/Data_Model.md`.

**Assumptions baked into the synthetic data** (documented in full inside
`scripts/generate_data.py`):
- Downtime durations and costs vary by machine type and by plant (a
  `reliability_factor` per plant creates realistic between-site
  variance).
- Unplanned events carry a cost-per-minute premium (1.1×–1.6×) over
  planned work, reflecting real-world emergency labor/parts premiums.
- Mild seasonality is built in (higher downtime around Nov/Dec and
  Jul/Aug) to make trend charts and the "highest downtime months"
  insight non-trivial and realistic.
- ~17% of events are left in "Pending" status and ~18% "In Progress" to
  simulate a live maintenance backlog rather than a fully closed dataset.

## 🗂️ Data Model

Star schema: `Fact_Downtime_Events` (4,200 rows) related to `Dim_Date`
(731-day contiguous calendar, marked as the official Date Table) and
`Dim_Machine` (47 deduplicated assets). Full relationship diagram and
setup steps in [`docs/Data_Model.md`](docs/Data_Model.md).

## 🧮 DAX Measures

A full library of 25+ measures is documented in
[`docs/DAX_Measures.md`](docs/DAX_Measures.md), including:

- **Volume/duration:** Total Downtime Events, Total Downtime Hours,
  Average Downtime per Event
- **Cost:** Total Repair Cost, Average Repair Cost, Cost per Downtime Hour
- **Planned vs. Unplanned:** Planned/Unplanned Downtime %, cost & hours share
- **Case management:** Average Resolution Time, Number of Pending/Resolved Events
- **Time intelligence:** YoY comparisons, MTD, rolling 3-month trend
- **Pareto support:** RANKX-based cumulative % for the 80/20 reason analysis

## 📈 Dashboard Pages

### Page 1 — Executive Overview
KPI cards (Total Downtime Events, Total Downtime Hours, Total Repair
Cost, Production Units Lost, Average Downtime, Average Repair Cost,
Pending Events, Unplanned Downtime %), monthly downtime & cost trends,
Planned vs. Unplanned donut, and breakdowns by Plant, Production Line,
Shift, Machine Type, Machine, and Downtime Reason. Slicers: Date, Plant,
Machine, Production Line, Shift, Machine Type, Downtime Category,
Planned/Unplanned.

![Executive Overview](images/01_executive_overview.png)

### Page 2 — Deep-Dive Analytics
Pareto analysis of downtime reasons (80/20 rule), a day-of-week ×
shift downtime heatmap, a downtime-hours-vs-repair-cost scatter plot, a
repair-cost waterfall by downtime category, and a treemap of downtime
categories by hours.

![Deep-Dive Analytics](images/02_deep_dive_analytics.png)

### Page 3 — Executive Insights
Written summary of the worst-performing plant, highest-cost machine,
most common downtime reason, highest-downtime months, and prioritized
recommendations to reduce downtime and maintenance cost. Full text
version: [`docs/Business_Recommendations.md`](docs/Business_Recommendations.md).

![Executive Insights](images/03_executive_insights.png)

## 🔑 Headline Findings (see full write-up for detail)

- **Worst plant:** Plant C – Katowice (2,371 h / €1.22M — ~33% of network downtime)
- **Costliest machine:** MC-7027, Assembly Robot, Plant C (€120,559 across 76 events)
- **Most frequent reason:** Motor Burnout (181 events); Belt Breakage drives the most hours (405.5 h)
- **Worst months:** December (both years) and July — a repeatable seasonal pattern
- **Unplanned downtime** is 73.8% of events but 83.7% of repair cost — reactive maintenance is disproportionately expensive

## 🔁 Rebuilding the Report in Power BI Desktop

1. Open Power BI Desktop → **Get Data → Excel** → select
   `data/Manufacturing_Downtime_Dataset.xlsx` → load `Fact_Downtime_Events`,
   `Dim_Date`, and `Dim_Machine`.
2. Follow the relationship & Date-Table setup in
   [`docs/Data_Model.md`](docs/Data_Model.md).
3. Create a blank `_Measures` table and paste in the DAX from
   [`docs/DAX_Measures.md`](docs/DAX_Measures.md).
4. Build the three report pages using the screenshots in `images/` as
   the visual spec — KPI cards along the top, slicers on the left/top,
   and the chart grid as shown.
5. Apply a dark theme: background `#0B0F17`, panel `#121826`, gridlines
   `#232B3D`, text `#E7ECF3`, accents amber `#F5A623` / cyan `#33C6F4` /
   red `#EF5B5B` / green `#5FD87A` (matches the mockups exactly).

## 📄 License / Usage

This is a portfolio/demonstration project built on **synthetic data**.
Feel free to fork, adapt, and use it as a template for your own BI
portfolio piece.
