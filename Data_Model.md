# Power BI Data Model

## Overview

The model follows a **star schema**: one fact table capturing every
downtime event, surrounded by supporting dimension tables. This is the
standard, recommended shape for Power BI — it keeps DAX simple, gives
good performance (VertiPaq compresses star schemas efficiently), and is
what interviewers expect to see in a portfolio project.

```
                     ┌───────────────────┐
                     │     Dim_Date      │
                     │───────────────────│
                     │ Date  (PK)        │
                     │ Year              │
                     │ Month             │
                     │ Month Number      │
                     │ Month Short       │
                     │ Year-Month        │
                     │ Week              │
                     │ Day Name          │
                     │ Day Number        │
                     │ Quarter           │
                     │ Is Weekend        │
                     └─────────┬─────────┘
                               │ 1
                               │
                               │ *
                 ┌─────────────┴─────────────┐
                 │   Fact_Downtime_Events     │
                 │────────────────────────────│
                 │ Event ID          (PK)     │
                 │ Date              (FK)     │───────┐
                 │ Machine ID        (FK)     │       │
                 │ Plant                      │       │
                 │ Production Line            │       │
                 │ Machine Type                │       │
                 │ Shift                       │       │
                 │ Operator ID                 │       │
                 │ Technician                  │       │
                 │ Downtime Category           │       │
                 │ Downtime Reason             │       │
                 │ Planned or Unplanned        │       │
                 │ Root Cause                  │       │
                 │ Downtime Minutes / Hours     │       │
                 │ Repair Cost EURO             │       │
                 │ Cost per Minute              │       │
                 │ Production Units Lost         │       │
                 │ Product Type                  │       │
                 │ Status                        │       │
                 │ Resolution Time                │       │
                 │ Maintenance Type                │       │
                 └─────────────┬────────────────────┘       │
                               │ *                            │
                               │                               │
                               │ 1                             │
                     ┌─────────┴──────────┐                    │
                     │    Dim_Machine     │◄───────────────────┘
                     │─────────────────────│
                     │ Machine ID   (PK)   │
                     │ Machine Type        │
                     │ Plant               │
                     │ Production Line     │
                     └─────────────────────┘

                     ┌────────────────────┐
                     │     _Measures      │  (blank helper table, DAX only)
                     └────────────────────┘
```

## Tables

### `Fact_Downtime_Events` (the fact table)
One row per downtime event — 4,200 rows spanning January 2023 through
December 2024. Contains all the transactional attributes and numeric
measures listed in the data dictionary (see the `Data_Dictionary` sheet
in the workbook).

### `Dim_Date`
A contiguous calendar table covering every day from 2023-01-01 to
2024-12-31 (731 rows), independent of whether an event occurred that
day. This is essential for accurate time-intelligence — a date table
built only from distinct dates *in the fact table* would silently break
`SAMEPERIODLASTYEAR`, `TOTALMTD`, and similar functions on days with no
events. In Power BI: **Modeling → Mark as Date Table**, using the `Date`
column.

### `Dim_Machine`
A deduplicated list of the 47 machines referenced in the fact table,
with their type, plant, and line. Included so Machine-level attributes
can be sliced independently of the fact grain and to demonstrate proper
dimensional modeling rather than relying on repeated text columns in
the fact table alone (in this build, `Plant`/`Production Line`/`Machine
Type` are also kept on the fact table for simplicity of slicing — in a
stricter enterprise model you would remove them from the fact table and
relate through `Dim_Machine` only, then hide `Machine ID` on the fact
table from the report view).

### `_Measures`
An empty table used purely to host all DAX measures (see
`DAX_Measures.md`). Keeping measures off the fact/dimension tables makes
the field list easier to navigate and signals modeling discipline.

## Relationships

| From | To | Cardinality | Cross-filter | Active |
|---|---|---|---|---|
| `Dim_Date[Date]` | `Fact_Downtime_Events[Date]` | 1 : Many | Single | Yes |
| `Dim_Machine[Machine ID]` | `Fact_Downtime_Events[Machine ID]` | 1 : Many | Single | Yes |

Both relationships filter in a single direction (dimension → fact),
which is the standard, most performant, and least error-prone pattern.
Avoid bidirectional filtering unless a specific many-to-many scenario
requires it.

## Why a Date Dimension Instead of Just Using the Fact Table's Date Column

1. **Correct time intelligence.** `DATEADD`, `SAMEPERIODLASTYEAR`, and
   `TOTALMTD` require a contiguous, gap-free date range.
2. **Consistent calendar attributes.** Month names, week numbers, and
   quarters are calculated once, centrally, rather than repeated (and
   potentially inconsistently derived) on every fact row.
3. **Filtering on days with zero events.** A trend chart built from
   `Dim_Date` correctly shows a `0` for a day with no downtime, rather
   than omitting the day entirely.

## Setting Up the Model in Power BI Desktop

1. Import `Fact_Downtime_Events`, `Dim_Date`, and `Dim_Machine` from
   `Manufacturing_Downtime_Dataset.xlsx`.
2. Create a blank query / enter-data table named `_Measures` (one column,
   no rows) to host measures.
3. In **Model view**, drag `Dim_Date[Date]` to `Fact_Downtime_Events[Date]`
   and `Dim_Machine[Machine ID]` to `Fact_Downtime_Events[Machine ID]`.
4. Right-click `Dim_Date` → **Mark as Date Table** → select the `Date`
   column.
5. Set data types: `Date` as Date, all `*Cost*` fields as Fixed Decimal
   Number with currency format (`€`), `*%` measures as Percentage.
6. Sort `Dim_Date[Month]` by `Dim_Date[Month Number]` (and, on the fact
   table, sort `Month` by `Month Number` too) so month names display in
   calendar order rather than alphabetically.
7. Hide foreign keys and helper columns not meant for report-level
   slicing (e.g., `Month Short`, `Day Number`) to keep the field list
   clean.
8. Paste in the measures from `DAX_Measures.md`.
