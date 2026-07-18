# Executive Insights — Key Findings & Recommendations

*Derived from the 4,200-event synthetic dataset (Jan 2023 – Dec 2024, 4 plants).
This is the written companion to the "Executive Insights" report page.*

## Headline Numbers

| Metric | Value |
|---|---|
| Total downtime events | 4,200 |
| Total downtime hours | 7,299.7 h |
| Total repair cost | €3,629,527 |
| Production units lost | 409,796 |
| Average downtime per event | 104.3 min |
| Average repair cost per event | €864 |
| Unplanned downtime (share of events) | 73.8% |
| Unplanned downtime (share of hours) | 79.1% |
| Unplanned downtime (share of cost) | 83.7% |
| Events still Pending | 705 |

## Key Findings

**1. Worst-performing plant: Plant C – Katowice.**
Katowice logged 2,371 downtime hours and €1.22M in repair cost across
1,175 events — the highest of the four plants on both hours and cost,
despite not being the largest site by event count margin. This points to
a reliability problem specific to the plant (equipment age, maintenance
staffing, or process discipline) rather than simply higher volume.

**2. Highest-cost machine: MC-7027 (Assembly Robot, Plant C).**
This single asset accumulated €120,559 in repair cost over 76 events —
an average of ~€1,586 per event, well above the network average of €864.
It is the clearest single candidate for either replacement or a
predictive-maintenance retrofit.

**3. Most common downtime reason: Motor Burnout (by event count) / Belt
Breakage (by total hours).**
Motor Burnout was logged 181 times; Belt Breakage, while slightly less
frequent, consumed more total hours (405.5 h) because individual
incidents run longer. Mechanical Failure is the single largest downtime
category overall, responsible for 19.6% of all events.

**4. Highest downtime months: December (both years) and July.**
December 2023 (379.6 h) and December 2024 (358.8 h) were the two worst
months in the dataset, with July 2023/2024 (346–357 h) close behind.
This is a consistent, repeatable seasonal pattern — not noise — and
points to year-end production-volume strain and summer thermal load on
equipment.

**5. The network is still reactive, not predictive.**
Corrective (1,663 events) and Emergency (845 events) maintenance
together outnumber Preventive (515) and Predictive (164) maintenance by
more than 3-to-1. Unplanned work costs disproportionately more too:
unplanned events are 73.8% of all events but 83.7% of all repair spend —
each unplanned hour of downtime costs meaningfully more than a planned
one, consistent with the extra labor premiums, expedited parts, and
production disruption that come with unscheduled failures.

**6. A real maintenance backlog exists.**
705 events (16.8% of the dataset) remain in "Pending" status. Left
unaddressed, a pending backlog compounds: unresolved minor issues become
tomorrow's major failures.

## Recommendations

### 1. Shift the maintenance mix from reactive to predictive
Deploy vibration and thermal sensors on the top 10 costliest machines
(starting with MC-7027) to catch bearing wear, belt fatigue, and motor
overheating before they cause an unplanned stop. Given that Mechanical
and Electrical Failure together drive ~33% of all events, condition
monitoring on rotating equipment offers the highest expected return.

### 2. Run a targeted reliability audit at Plant C – Katowice
Investigate whether Katowice's elevated downtime stems from equipment
age, technician staffing levels, spare-parts availability, or process
adherence. Given it already accounts for roughly a third of network
downtime hours, even a modest improvement here would move the network
average meaningfully.

### 3. Build a seasonal maintenance calendar
Schedule additional preventive maintenance passes in the weeks *before*
the recurring November/December and July peaks, rather than reacting to
them after the fact. Pair this with a monthly cadence to clear the
Pending backlog so minor issues don't accumulate into the next seasonal
spike.

### 4. Track cost-per-downtime-hour by machine, not just total cost
Total repair cost rewards machines that already run more; cost *per
downtime hour* or *per event* better isolates which assets are
genuinely expensive to maintain versus which are simply busier. Use this
lens when deciding where to invest in replacement versus repair.

### 5. Set a target to reduce the unplanned-hours share
Because unplanned downtime is disproportionately expensive (83.7% of
cost from 79.1% of hours), even a modest shift of volume from unplanned
to planned maintenance — via the predictive-maintenance program above —
would produce cost savings larger than the percentage-point shift alone
suggests.

## Suggested KPIs to Monitor Going Forward

- Unplanned downtime % (target: downward trend, quarter over quarter)
- Cost per downtime hour by plant and by machine type
- Preventive + Predictive share of all maintenance events (target: upward trend)
- Open/Pending event count (target: cleared within a rolling 30-day window)
- Repeat-failure rate per machine (same `Downtime Reason` recurring within 90 days)
