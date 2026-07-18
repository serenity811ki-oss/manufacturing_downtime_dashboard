# DAX Measures Library

All measures below are written for a model where the fact table is named
`Fact_Downtime_Events` and is related to `Dim_Date` (on `Date`) and
`Dim_Machine` (on `Machine ID`). Create a dedicated **`_Measures`** table
(a blank table with no data) and place all measures there — this is a
Power BI best practice that keeps the model tree clean and separates
measures from columns.

Copy-paste each block into a new measure in Power BI Desktop.

---

## Core Volume & Duration Measures

```dax
Total Downtime Events =
COUNTROWS ( Fact_Downtime_Events )
```

```dax
Total Downtime Hours =
SUM ( Fact_Downtime_Events[Downtime Hours] )
```

```dax
Total Downtime Minutes =
SUM ( Fact_Downtime_Events[Downtime Minutes] )
```

```dax
Average Downtime per Event (Minutes) =
DIVIDE (
    [Total Downtime Minutes],
    [Total Downtime Events]
)
```

```dax
Average Downtime per Event (Hours) =
DIVIDE (
    [Total Downtime Hours],
    [Total Downtime Events]
)
```

---

## Cost Measures

```dax
Total Repair Cost =
SUM ( Fact_Downtime_Events[Repair Cost EURO] )
```

```dax
Average Repair Cost =
DIVIDE (
    [Total Repair Cost],
    [Total Downtime Events]
)
```

```dax
Cost per Downtime Hour =
DIVIDE (
    [Total Repair Cost],
    [Total Downtime Hours]
)
```

```dax
Cost per Downtime Minute =
DIVIDE (
    [Total Repair Cost],
    [Total Downtime Minutes]
)
```

---

## Production Impact Measures

```dax
Total Production Units Lost =
SUM ( Fact_Downtime_Events[Production Units Lost] )
```

```dax
Avg Units Lost per Event =
DIVIDE (
    [Total Production Units Lost],
    [Total Downtime Events]
)
```

---

## Planned vs. Unplanned Measures

```dax
Planned Downtime Events =
CALCULATE (
    [Total Downtime Events],
    Fact_Downtime_Events[Planned or Unplanned] = "Planned"
)
```

```dax
Unplanned Downtime Events =
CALCULATE (
    [Total Downtime Events],
    Fact_Downtime_Events[Planned or Unplanned] = "Unplanned"
)
```

```dax
Planned Downtime % =
DIVIDE (
    [Planned Downtime Events],
    [Total Downtime Events]
)
```

```dax
Unplanned Downtime % =
DIVIDE (
    [Unplanned Downtime Events],
    [Total Downtime Events]
)
```

```dax
Unplanned Downtime Hours % =
DIVIDE (
    CALCULATE ( [Total Downtime Hours], Fact_Downtime_Events[Planned or Unplanned] = "Unplanned" ),
    [Total Downtime Hours]
)
```

```dax
Unplanned Repair Cost % =
DIVIDE (
    CALCULATE ( [Total Repair Cost], Fact_Downtime_Events[Planned or Unplanned] = "Unplanned" ),
    [Total Repair Cost]
)
```

> Format each `%` measure as a percentage with one decimal place in the
> Modeling ribbon so it renders as `73.8%` rather than `0.738`.

---

## Resolution & Status Measures

```dax
Average Resolution Time =
AVERAGE ( Fact_Downtime_Events[Resolution Time] )
```

```dax
Number of Pending Events =
CALCULATE (
    [Total Downtime Events],
    Fact_Downtime_Events[Status] = "Pending"
)
```

```dax
Number of Resolved Events =
CALCULATE (
    [Total Downtime Events],
    Fact_Downtime_Events[Status] = "Resolved"
)
```

```dax
Number of In-Progress Events =
CALCULATE (
    [Total Downtime Events],
    Fact_Downtime_Events[Status] = "In Progress"
)
```

```dax
Resolved Rate % =
DIVIDE (
    [Number of Resolved Events],
    [Total Downtime Events]
)
```

---

## Time-Intelligence Measures (require Dim_Date marked as the Date table)

```dax
Downtime Hours PY =
CALCULATE (
    [Total Downtime Hours],
    SAMEPERIODLASTYEAR ( Dim_Date[Date] )
)
```

```dax
Downtime Hours YoY % =
DIVIDE (
    [Total Downtime Hours] - [Downtime Hours PY],
    [Downtime Hours PY]
)
```

```dax
Repair Cost PY =
CALCULATE (
    [Total Repair Cost],
    SAMEPERIODLASTYEAR ( Dim_Date[Date] )
)
```

```dax
Repair Cost YoY % =
DIVIDE (
    [Total Repair Cost] - [Repair Cost PY],
    [Repair Cost PY]
)
```

```dax
Downtime Hours MTD =
TOTALMTD ( [Total Downtime Hours], Dim_Date[Date] )
```

```dax
Downtime Hours Rolling 3M =
CALCULATE (
    [Total Downtime Hours],
    DATESINPERIOD ( Dim_Date[Date], MAX ( Dim_Date[Date] ), -3, MONTH )
)
```

---

## Ranking / Pareto Support Measures

```dax
Downtime Hours Rank (Reason) =
RANKX (
    ALL ( Fact_Downtime_Events[Downtime Reason] ),
    CALCULATE ( [Total Downtime Hours] )
)
```

```dax
Cumulative Downtime Hours % (Pareto) =
VAR CurrentReasonRank = [Downtime Hours Rank (Reason)]
VAR CumulativeHours =
    CALCULATE (
        [Total Downtime Hours],
        FILTER (
            ALL ( Fact_Downtime_Events[Downtime Reason] ),
            [Downtime Hours Rank (Reason)] <= CurrentReasonRank
        )
    )
VAR TotalHours =
    CALCULATE ( [Total Downtime Hours], ALL ( Fact_Downtime_Events[Downtime Reason] ) )
RETURN
    DIVIDE ( CumulativeHours, TotalHours )
```

> Used to drive the 80/20 cumulative-percentage line on the Pareto chart.

---

## KPI Cards Used on the Executive Overview Page

| KPI Card | Measure |
|---|---|
| Total Downtime Events | `[Total Downtime Events]` |
| Total Downtime Hours | `[Total Downtime Hours]` |
| Total Repair Cost | `[Total Repair Cost]` |
| Production Units Lost | `[Total Production Units Lost]` |
| Average Downtime | `[Average Downtime per Event (Minutes)]` |
| Average Repair Cost | `[Average Repair Cost]` |
| Pending Events | `[Number of Pending Events]` |
| Unplanned Downtime % | `[Unplanned Downtime %]` |

---

## Notes on Measure Design

- Every ratio measure uses `DIVIDE()` instead of the `/` operator so it
  returns `BLANK()` instead of an error when a filter context produces a
  zero denominator (e.g., a slicer selection with no matching rows).
- Base measures (`Total Downtime Hours`, `Total Repair Cost`, etc.) are
  built first and referenced by every derived measure — this keeps the
  logic DRY and means a single formula change propagates everywhere.
- Time-intelligence measures assume `Dim_Date` has been marked as the
  official **Date Table** in Power BI (Modeling → Mark as Date Table) and
  that its `Date` column is contiguous with no gaps (see `Dim_Date` sheet
  in the workbook, which covers every calendar day from 2023-01-01 to
  2024-12-31).
