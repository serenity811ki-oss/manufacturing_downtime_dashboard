"""
Manufacturing Downtime Analytics - Synthetic Dataset Generator
Generates a realistic, internally-consistent downtime event log for a
multi-plant European manufacturing operation, Jan 2023 - Dec 2024.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

rng = np.random.default_rng(42)

N_RECORDS = 4200
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)
TOTAL_DAYS = (END_DATE - START_DATE).days

# ---------------------------------------------------------------------------
# Reference dimensions
# ---------------------------------------------------------------------------

PLANTS = {
    "Plant A - Stuttgart":  {"lines": ["Line 1", "Line 2", "Line 3"], "weight": 0.30, "reliability": 1.00},
    "Plant B - Lyon":       {"lines": ["Line 1", "Line 2"],           "weight": 0.22, "reliability": 0.95},
    "Plant C - Katowice":   {"lines": ["Line 1", "Line 2", "Line 3"], "weight": 0.28, "reliability": 1.20},
    "Plant D - Bratislava": {"lines": ["Line 1", "Line 2"],           "weight": 0.20, "reliability": 1.10},
}

MACHINE_TYPES = {
    "CNC Machine":        {"cost_factor": 1.30, "unit_rate": 45},
    "Robotic Welder":     {"cost_factor": 1.50, "unit_rate": 60},
    "Injection Molding":  {"cost_factor": 1.20, "unit_rate": 90},
    "Conveyor System":    {"cost_factor": 0.70, "unit_rate": 30},
    "Assembly Robot":     {"cost_factor": 1.40, "unit_rate": 55},
    "Packaging Unit":     {"cost_factor": 0.60, "unit_rate": 70},
    "Press Machine":      {"cost_factor": 1.10, "unit_rate": 50},
    "Painting Robot":     {"cost_factor": 1.15, "unit_rate": 40},
}

SHIFTS = ["Morning (06:00-14:00)", "Afternoon (14:00-22:00)", "Night (22:00-06:00)"]
SHIFT_WEIGHTS = [0.38, 0.36, 0.26]  # night shift slightly fewer events logged

PRODUCT_TYPES = ["Automotive Component", "Industrial Parts", "Consumer Electronics",
                 "Medical Device", "Packaging Materials"]

TECHNICIANS = [
    "M. Novak", "J. Dubois", "A. Schmidt", "P. Kowalski", "L. Fischer",
    "R. Nagy", "T. Weber", "S. Kaczmarek", "D. Muller", "K. Varga",
    "F. Rousseau", "H. Zajac", "B. Klein", "N. Horvat", "E. Wagner",
]

# Downtime category -> (typical reasons, planned flag, minutes range, maintenance type pool)
CATEGORY_MAP = {
    "Mechanical Failure": {
        "reasons": ["Bearing Failure", "Belt Breakage", "Gearbox Malfunction", "Hydraulic Leak", "Motor Burnout"],
        "planned": False, "min_minutes": 20, "max_minutes": 240,
        "maintenance": ["Corrective", "Emergency"],
        "root_causes": ["Component wear beyond tolerance", "Lubrication failure", "Fatigue crack", "Misalignment"],
    },
    "Electrical Failure": {
        "reasons": ["Sensor Fault", "Wiring Short Circuit", "Power Supply Failure", "Control Panel Fault"],
        "planned": False, "min_minutes": 15, "max_minutes": 180,
        "maintenance": ["Corrective", "Emergency"],
        "root_causes": ["Voltage spike", "Corroded contact", "Faulty relay", "Overheated component"],
    },
    "Software/PLC Error": {
        "reasons": ["PLC Program Fault", "HMI Communication Loss", "SCADA Timeout", "Firmware Crash"],
        "planned": False, "min_minutes": 10, "max_minutes": 120,
        "maintenance": ["Corrective"],
        "root_causes": ["Software bug", "Network latency", "Unhandled exception", "Configuration drift"],
    },
    "Tooling Issue": {
        "reasons": ["Tool Wear", "Tool Breakage", "Die Misalignment", "Mold Damage"],
        "planned": False, "min_minutes": 15, "max_minutes": 150,
        "maintenance": ["Corrective"],
        "root_causes": ["Exceeded tool life", "Incorrect feed rate", "Material hardness variance"],
    },
    "Material Shortage": {
        "reasons": ["Raw Material Delay", "Component Stockout", "Supplier Late Delivery"],
        "planned": False, "min_minutes": 30, "max_minutes": 300,
        "maintenance": ["N/A"],
        "root_causes": ["Supplier logistics delay", "Inventory planning gap", "Customs delay"],
    },
    "Utility Failure": {
        "reasons": ["Power Outage", "Compressed Air Loss", "Cooling System Failure", "Water Supply Interruption"],
        "planned": False, "min_minutes": 20, "max_minutes": 200,
        "maintenance": ["Emergency", "Corrective"],
        "root_causes": ["Grid instability", "Compressor failure", "Chiller malfunction"],
    },
    "Operator Error": {
        "reasons": ["Incorrect Setup", "Manual Stop", "Safety Interlock Triggered"],
        "planned": False, "min_minutes": 5, "max_minutes": 60,
        "maintenance": ["N/A"],
        "root_causes": ["Inadequate training", "Procedure not followed", "Distraction"],
    },
    "Quality Inspection": {
        "reasons": ["In-Process Quality Hold", "Non-Conformance Review", "Calibration Check"],
        "planned": True, "min_minutes": 15, "max_minutes": 90,
        "maintenance": ["Preventive"],
        "root_causes": ["Dimensional deviation", "Random audit", "Customer complaint follow-up"],
    },
    "Changeover": {
        "reasons": ["Product Changeover", "Tooling Changeover", "Recipe Changeover"],
        "planned": True, "min_minutes": 20, "max_minutes": 120,
        "maintenance": ["N/A"],
        "root_causes": ["Scheduled production changeover"],
    },
    "Preventive Maintenance": {
        "reasons": ["Scheduled Lubrication", "Scheduled Inspection", "Filter Replacement", "Calibration"],
        "planned": True, "min_minutes": 30, "max_minutes": 180,
        "maintenance": ["Preventive", "Predictive"],
        "root_causes": ["Scheduled maintenance plan (TPM calendar)"],
    },
}

CATEGORIES = list(CATEGORY_MAP.keys())
# Weighting so failures dominate (more realistic than uniform)
CATEGORY_WEIGHTS = [0.19, 0.13, 0.09, 0.11, 0.08, 0.07, 0.06, 0.09, 0.10, 0.08]

STATUS_POOL = ["Resolved", "Resolved", "Resolved", "Resolved", "In Progress", "Pending"]

# ---------------------------------------------------------------------------
# Build records
# ---------------------------------------------------------------------------

plant_names = list(PLANTS.keys())
plant_weights = [PLANTS[p]["weight"] for p in plant_names]
machine_type_names = list(MACHINE_TYPES.keys())

records = []

# Pre-generate a fixed pool of Machine IDs per plant/line/type for consistency
machine_pool = {}
for p in plant_names:
    for line in PLANTS[p]["lines"]:
        for _ in range(rng.integers(4, 7)):
            mtype = rng.choice(machine_type_names)
            mid = f"MC-{rng.integers(1000, 9999)}"
            machine_pool.setdefault((p, line), []).append((mid, mtype))

operator_pool = [f"OP-{i:04d}" for i in rng.choice(range(1001, 1400), size=180, replace=False)]

# Seasonal weighting: slightly higher downtime in Jan (post-holiday restart), Jul/Aug (heat/maintenance), Nov/Dec (peak production strain)
month_seasonality = {1: 1.15, 2: 1.0, 3: 0.95, 4: 0.95, 5: 0.95, 6: 1.0,
                     7: 1.10, 8: 1.05, 9: 0.95, 10: 0.95, 11: 1.10, 12: 1.20}

# Build a day pool weighted by month seasonality across the 2-year range
all_days = [START_DATE + timedelta(days=i) for i in range(TOTAL_DAYS + 1)]
day_weights = np.array([month_seasonality[d.month] for d in all_days], dtype=float)
day_weights = day_weights / day_weights.sum()

chosen_days = rng.choice(all_days, size=N_RECORDS, p=day_weights)

for i, date in enumerate(sorted(chosen_days)):
    plant = rng.choice(plant_names, p=plant_weights)
    line = rng.choice(PLANTS[plant]["lines"])
    machine_id, machine_type = machine_pool[(plant, line)][rng.integers(0, len(machine_pool[(plant, line)]))]

    category = rng.choice(CATEGORIES, p=CATEGORY_WEIGHTS)
    cat_info = CATEGORY_MAP[category]
    reason = rng.choice(cat_info["reasons"])
    root_cause = rng.choice(cat_info["root_causes"])
    planned_flag = "Planned" if cat_info["planned"] else "Unplanned"
    maintenance_type = rng.choice(cat_info["maintenance"])

    shift = rng.choice(SHIFTS, p=SHIFT_WEIGHTS)
    operator_id = rng.choice(operator_pool)
    technician = rng.choice(TECHNICIANS)

    reliability_factor = PLANTS[plant]["reliability"]
    base_minutes = rng.uniform(cat_info["min_minutes"], cat_info["max_minutes"])
    downtime_minutes = round(base_minutes * reliability_factor * rng.uniform(0.85, 1.2), 1)
    downtime_minutes = max(5.0, downtime_minutes)
    downtime_hours = round(downtime_minutes / 60, 2)

    type_info = MACHINE_TYPES[machine_type]
    base_cost_per_min = rng.uniform(3.5, 9.0) * type_info["cost_factor"]
    # unplanned emergency repairs cost more per minute than planned maintenance
    if planned_flag == "Unplanned":
        base_cost_per_min *= rng.uniform(1.1, 1.6)
    repair_cost = round(downtime_minutes * base_cost_per_min, 2)
    cost_per_minute = round(repair_cost / downtime_minutes, 2)

    production_units_lost = int(round((downtime_minutes / 60) * type_info["unit_rate"] * rng.uniform(0.8, 1.15)))

    product_type = rng.choice(PRODUCT_TYPES)

    status = rng.choice(STATUS_POOL)
    if date > END_DATE - timedelta(days=10):
        status = rng.choice(["Resolved", "In Progress", "Pending"], p=[0.4, 0.35, 0.25])

    if status == "Resolved":
        resolution_time = round(downtime_hours * rng.uniform(1.0, 1.8), 2)
    elif status == "In Progress":
        resolution_time = round(downtime_hours * rng.uniform(0.4, 0.9), 2)
    else:
        resolution_time = None  # pending -> not yet resolved

    week_num = int(date.isocalendar()[1])

    records.append({
        "Date": date.strftime("%Y-%m-%d"),
        "Year": date.year,
        "Month": date.strftime("%B"),
        "Week": week_num,
        "Plant": plant,
        "Production Line": line,
        "Machine ID": machine_id,
        "Machine Type": machine_type,
        "Shift": shift,
        "Operator ID": operator_id,
        "Technician": technician,
        "Downtime Category": category,
        "Downtime Reason": reason,
        "Planned or Unplanned": planned_flag,
        "Root Cause": root_cause,
        "Downtime Minutes": downtime_minutes,
        "Downtime Hours": downtime_hours,
        "Repair Cost EURO": repair_cost,
        "Cost per Minute": cost_per_minute,
        "Production Units Lost": production_units_lost,
        "Product Type": product_type,
        "Status": status,
        "Resolution Time": resolution_time,
        "Maintenance Type": maintenance_type,
    })

df = pd.DataFrame(records)

# Add a stable event ID as the first column
df.insert(0, "Event ID", [f"DT-{100000 + i}" for i in range(len(df))])

# Month should sort chronologically later in Power BI via a Month Number column - add helper
month_order = {datetime(2000, m, 1).strftime("%B"): m for m in range(1, 13)}
df.insert(4, "Month Number", df["Month"].map(month_order))

df = df.sort_values("Date").reset_index(drop=True)

print(f"Generated {len(df)} records")
print(df.head(3).to_string())
print("\nColumn dtypes:")
print(df.dtypes)

df.to_csv("/home/claude/project/data/manufacturing_downtime_data.csv", index=False)
print("\nSaved to CSV.")
