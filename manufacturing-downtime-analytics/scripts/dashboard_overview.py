import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import gridspec

df = pd.read_csv("/home/claude/project/data/manufacturing_downtime_data.csv")
df["Date"] = pd.to_datetime(df["Date"])

# ---------------- Theme ----------------
BG = "#0B0F17"
PANEL = "#121826"
GRID = "#232B3D"
TEXT = "#E7ECF3"
SUBTEXT = "#8B95A7"
ACCENT = "#F5A623"      # industrial amber
ACCENT2 = "#33C6F4"     # cyan
ACCENT3 = "#EF5B5B"     # alert red
ACCENT4 = "#5FD87A"     # green
PALETTE = ["#F5A623", "#33C6F4", "#EF5B5B", "#5FD87A", "#9B7EDE", "#F2789F", "#6E8FF0", "#F0C419"]

plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor": PANEL,
    "axes.edgecolor": GRID,
    "axes.labelcolor": TEXT,
    "text.color": TEXT,
    "xtick.color": SUBTEXT,
    "ytick.color": SUBTEXT,
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "grid.color": GRID,
})

fig = plt.figure(figsize=(21, 12.5), dpi=150)
fig.patch.set_facecolor(BG)

gs = gridspec.GridSpec(6, 12, figure=fig, wspace=0.55, hspace=1.1,
                        left=0.025, right=0.985, top=0.90, bottom=0.03)

# ---------------- Title bar ----------------
fig.text(0.025, 0.965, "MANUFACTURING DOWNTIME ANALYTICS", fontsize=22, fontweight="bold", color=TEXT)
fig.text(0.025, 0.945, "Executive Overview  |  Multi-Plant Operations  |  Jan 2023 – Dec 2024", fontsize=11, color=SUBTEXT)
fig.text(0.985, 0.965, "Plant: All   Line: All   Shift: All   Category: All", fontsize=9, color=SUBTEXT, ha="right")
fig.text(0.985, 0.945, "Last Refreshed: 31-Dec-2024", fontsize=9, color=SUBTEXT, ha="right")

# ---------------- KPI card helper ----------------
def kpi_card(ax, label, value, sub=None, color=ACCENT):
    ax.set_facecolor(PANEL)
    for s in ax.spines.values():
        s.set_color(GRID)
    ax.set_xticks([]); ax.set_yticks([])
    ax.add_patch(mpatches.Rectangle((0, 0), 1, 0.08, transform=ax.transAxes, color=color, clip_on=False))
    ax.text(0.08, 0.62, value, fontsize=20, fontweight="bold", color=TEXT, transform=ax.transAxes, va="center")
    ax.text(0.08, 0.28, label, fontsize=9.5, color=SUBTEXT, transform=ax.transAxes, va="center")
    if sub:
        ax.text(0.08, 0.10, sub, fontsize=8, color=color, transform=ax.transAxes, va="center")

# ---------------- KPI values ----------------
total_events = len(df)
total_hours = df["Downtime Hours"].sum()
total_cost = df["Repair Cost EURO"].sum()
units_lost = df["Production Units Lost"].sum()
avg_downtime = df["Downtime Minutes"].mean()
avg_cost = df["Repair Cost EURO"].mean()
pending = (df["Status"] == "Pending").sum()
unplanned_pct = (df["Planned or Unplanned"] == "Unplanned").mean() * 100

kpis = [
    ("TOTAL DOWNTIME EVENTS", f"{total_events:,}", None, ACCENT),
    ("TOTAL DOWNTIME HOURS", f"{total_hours:,.0f} h", None, ACCENT2),
    ("TOTAL REPAIR COST", f"€{total_cost/1e6:,.2f}M", None, ACCENT3),
    ("PRODUCTION UNITS LOST", f"{units_lost:,}", None, ACCENT3),
    ("AVG DOWNTIME / EVENT", f"{avg_downtime:,.0f} min", None, ACCENT2),
    ("AVG REPAIR COST", f"€{avg_cost:,.0f}", None, ACCENT),
    ("PENDING EVENTS", f"{pending:,}", "Needs attention", ACCENT3),
    ("UNPLANNED DOWNTIME %", f"{unplanned_pct:,.1f}%", None, ACCENT4),
]
for i, (label, val, sub, color) in enumerate(kpis):
    ax = fig.add_subplot(gs[0, i * 12 // 8:(i + 1) * 12 // 8])
    kpi_card(ax, label, val, sub, color)

def style_ax(ax, title):
    ax.set_title(title, fontsize=10.5, color=TEXT, loc="left", fontweight="bold", pad=6)
    ax.grid(axis="y", alpha=0.25, linewidth=0.6)
    ax.set_axisbelow(True)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    for s in ["bottom", "left"]:
        ax.spines[s].set_color(GRID)

# ---------------- Row 2: Monthly downtime trend + Monthly cost trend ----------------
monthly = df.groupby(df["Date"].dt.to_period("M")).agg(hours=("Downtime Hours", "sum"),
                                                          cost=("Repair Cost EURO", "sum")).reset_index()
monthly["Date"] = monthly["Date"].dt.to_timestamp()

ax1 = fig.add_subplot(gs[1:3, 0:5])
ax1.plot(monthly["Date"], monthly["hours"], color=ACCENT, linewidth=2, marker="o", markersize=3)
ax1.fill_between(monthly["Date"], monthly["hours"], color=ACCENT, alpha=0.12)
style_ax(ax1, "Monthly Downtime Trend (Hours)")
ax1.tick_params(axis="x", rotation=45, labelsize=7.5)

ax2 = fig.add_subplot(gs[1:3, 5:10])
ax2.plot(monthly["Date"], monthly["cost"], color=ACCENT2, linewidth=2, marker="o", markersize=3)
ax2.fill_between(monthly["Date"], monthly["cost"], color=ACCENT2, alpha=0.12)
style_ax(ax2, "Monthly Repair Cost Trend (EUR)")
ax2.tick_params(axis="x", rotation=45, labelsize=7.5)

# Planned vs Unplanned donut
ax3 = fig.add_subplot(gs[1:3, 10:12])
pu = df["Planned or Unplanned"].value_counts()
wedges, _ = ax3.pie(pu.values, colors=[ACCENT3, ACCENT4], startangle=90,
                     wedgeprops=dict(width=0.42, edgecolor=BG))
ax3.text(0, 0.05, f"{pu['Unplanned']/pu.sum()*100:.0f}%", ha="center", va="center", fontsize=16, fontweight="bold", color=TEXT)
ax3.text(0, -0.18, "Unplanned", ha="center", va="center", fontsize=8, color=SUBTEXT)
ax3.set_title("Planned vs Unplanned", fontsize=10.5, color=TEXT, loc="center", fontweight="bold", pad=6)
ax3.legend(["Unplanned", "Planned"], loc="lower center", bbox_to_anchor=(0.5, -0.18), ncol=2,
           frameon=False, fontsize=7.5, labelcolor=TEXT)

# ---------------- Row 3: by plant, by line, by shift, by machine type ----------------
def hbar(ax, series, title, color=ACCENT, fmt="{:.0f}"):
    series = series.sort_values()
    bars = ax.barh(series.index.astype(str), series.values, color=color, height=0.6)
    style_ax(ax, title)
    ax.tick_params(axis="y", labelsize=8)
    for b, v in zip(bars, series.values):
        ax.text(v, b.get_y() + b.get_height() / 2, " " + fmt.format(v), va="center", fontsize=7.5, color=SUBTEXT)

ax4 = fig.add_subplot(gs[3:5, 0:3])
hbar(ax4, df.groupby("Plant")["Downtime Hours"].sum(), "Downtime by Plant (Hours)", ACCENT)

ax5 = fig.add_subplot(gs[3:5, 3:6])
hbar(ax5, df.groupby("Production Line")["Downtime Hours"].sum(), "Downtime by Production Line (Hours)", ACCENT2)

ax6 = fig.add_subplot(gs[3:5, 6:9])
hbar(ax6, df.groupby("Shift")["Downtime Hours"].sum(), "Downtime by Shift (Hours)", ACCENT4)

ax7 = fig.add_subplot(gs[3:5, 9:12])
hbar(ax7, df.groupby("Machine Type")["Downtime Hours"].sum(), "Downtime by Machine Type (Hours)", ACCENT3)

# ---------------- Row 4: top machines by downtime, by reason, cost by machine, units lost by plant ----------------
ax8 = fig.add_subplot(gs[5:6, 0:3])
top_machines = df.groupby("Machine ID")["Downtime Hours"].sum().sort_values(ascending=False).head(10).sort_values()
hbar(ax8, top_machines, "Downtime by Machine (Top 10, Hours)", ACCENT2)
ax8.tick_params(axis="y", labelsize=7)

ax9 = fig.add_subplot(gs[5:6, 3:6])
top_reasons = df.groupby("Downtime Reason")["Downtime Hours"].sum().sort_values(ascending=False).head(10).sort_values()
hbar(ax9, top_reasons, "Downtime by Reason (Top 10, Hours)", ACCENT)
ax9.tick_params(axis="y", labelsize=7)

ax10 = fig.add_subplot(gs[5:6, 6:9])
cost_machine = df.groupby("Machine ID")["Repair Cost EURO"].sum().sort_values(ascending=False).head(10).sort_values()
hbar(ax10, cost_machine, "Repair Cost by Machine (Top 10, EUR)", ACCENT3, fmt="€{:,.0f}")
ax10.tick_params(axis="y", labelsize=7)

ax11 = fig.add_subplot(gs[5:6, 9:12])
units_plant = df.groupby("Plant")["Production Units Lost"].sum()
hbar(ax11, units_plant, "Production Units Lost by Plant", ACCENT4, fmt="{:,.0f}")

fig.text(0.025, 0.008, "Source: Fact_Downtime_Events (synthetic dataset)  |  Portfolio project by Stephen  |  Built for Power BI", fontsize=7.5, color=SUBTEXT)

plt.savefig("/home/claude/project/images/01_executive_overview.png", facecolor=BG, bbox_inches="tight")
print("Saved 01_executive_overview.png")
