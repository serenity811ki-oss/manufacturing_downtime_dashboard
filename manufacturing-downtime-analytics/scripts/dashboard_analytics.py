import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import gridspec
import squarify

df = pd.read_csv("/home/claude/project/data/manufacturing_downtime_data.csv")
df["Date"] = pd.to_datetime(df["Date"])

BG = "#0B0F17"
PANEL = "#121826"
GRID = "#232B3D"
TEXT = "#E7ECF3"
SUBTEXT = "#8B95A7"
ACCENT = "#F5A623"
ACCENT2 = "#33C6F4"
ACCENT3 = "#EF5B5B"
ACCENT4 = "#5FD87A"
PALETTE = ["#F5A623", "#33C6F4", "#EF5B5B", "#5FD87A", "#9B7EDE", "#F2789F", "#6E8FF0", "#F0C419", "#5CD6C0", "#E88BD8"]

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": PANEL, "axes.edgecolor": GRID,
    "axes.labelcolor": TEXT, "text.color": TEXT, "xtick.color": SUBTEXT,
    "ytick.color": SUBTEXT, "font.family": "DejaVu Sans", "font.size": 9, "grid.color": GRID,
})

fig = plt.figure(figsize=(21, 12.5), dpi=150)
fig.patch.set_facecolor(BG)
gs = gridspec.GridSpec(6, 12, figure=fig, wspace=0.6, hspace=1.3,
                        left=0.03, right=0.98, top=0.90, bottom=0.03)

fig.text(0.025, 0.965, "MANUFACTURING DOWNTIME ANALYTICS", fontsize=22, fontweight="bold", color=TEXT)
fig.text(0.025, 0.945, "Deep-Dive Analytics  |  Root Cause & Cost Drilldown  |  Jan 2023 – Dec 2024", fontsize=11, color=SUBTEXT)
fig.text(0.985, 0.965, "Plant: All   Line: All   Shift: All   Category: All", fontsize=9, color=SUBTEXT, ha="right")

def style_ax(ax, title):
    ax.set_title(title, fontsize=11, color=TEXT, loc="left", fontweight="bold", pad=8)
    ax.grid(axis="y", alpha=0.25, linewidth=0.6)
    ax.set_axisbelow(True)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    for s in ["bottom", "left"]:
        ax.spines[s].set_color(GRID)

# ---------------- Pareto chart: downtime reasons ----------------
ax1 = fig.add_subplot(gs[0:3, 0:5])
reason_hours = df.groupby("Downtime Reason")["Downtime Hours"].sum().sort_values(ascending=False)
cum_pct = reason_hours.cumsum() / reason_hours.sum() * 100
x = np.arange(len(reason_hours))
ax1.bar(x, reason_hours.values, color=ACCENT, width=0.65)
ax1b = ax1.twinx()
ax1b.plot(x, cum_pct.values, color=ACCENT2, marker="o", markersize=3, linewidth=2)
ax1b.axhline(80, color=ACCENT3, linestyle="--", linewidth=1, alpha=0.8)
ax1b.text(len(x) - 1, 82, "80% line", color=ACCENT3, fontsize=8, ha="right")
ax1b.set_ylim(0, 105)
ax1b.tick_params(colors=SUBTEXT, labelsize=7.5)
ax1b.spines["top"].set_visible(False)
ax1.set_xticks(x)
ax1.set_xticklabels(reason_hours.index, rotation=75, ha="right", fontsize=6.5)
style_ax(ax1, "Pareto Analysis — Downtime Reasons (Hours & Cumulative %)")

# ---------------- Heatmap: downtime by day-of-week and shift ----------------
ax2 = fig.add_subplot(gs[0:3, 5:8])
df["DOW"] = df["Date"].dt.day_name()
dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
shift_order = ["Morning (06:00-14:00)", "Afternoon (14:00-22:00)", "Night (22:00-06:00)"]
heat = df.pivot_table(index="Shift", columns="DOW", values="Downtime Hours", aggfunc="sum").reindex(index=shift_order, columns=dow_order)
im = ax2.imshow(heat.values, cmap="inferno", aspect="auto")
ax2.set_xticks(range(len(dow_order)))
ax2.set_xticklabels([d[:3] for d in dow_order], fontsize=8)
ax2.set_yticks(range(len(shift_order)))
ax2.set_yticklabels(["Morning", "Afternoon", "Night"], fontsize=8)
for i in range(heat.shape[0]):
    for j in range(heat.shape[1]):
        val = heat.values[i, j]
        ax2.text(j, i, f"{val:.0f}", ha="center", va="center", fontsize=7.5,
                  color="white" if val < heat.values.max() * 0.7 else "black")
ax2.set_title("Downtime Heatmap — Day of Week × Shift (Hours)", fontsize=11, color=TEXT, loc="left", fontweight="bold", pad=8)
for s in ax2.spines.values():
    s.set_visible(False)
cbar = fig.colorbar(im, ax=ax2, fraction=0.04, pad=0.03)
cbar.ax.tick_params(colors=SUBTEXT, labelsize=7)

# ---------------- Scatter: downtime hours vs repair cost ----------------
ax3 = fig.add_subplot(gs[0:3, 8:12])
sample = df.sample(min(1200, len(df)), random_state=1)
colors_map = {"Planned": ACCENT4, "Unplanned": ACCENT3}
for label, grp in sample.groupby("Planned or Unplanned"):
    ax3.scatter(grp["Downtime Hours"], grp["Repair Cost EURO"], s=10, alpha=0.55,
                color=colors_map[label], label=label, linewidths=0)
style_ax(ax3, "Downtime Hours vs. Repair Cost (EUR)")
ax3.legend(frameon=False, fontsize=8, labelcolor=TEXT, loc="upper left")
ax3.set_xlabel("Downtime Hours", fontsize=8.5)
ax3.set_ylabel("Repair Cost (EUR)", fontsize=8.5)

# ---------------- Waterfall: repair cost by downtime category ----------------
ax4 = fig.add_subplot(gs[3:6, 0:6])
cat_cost = df.groupby("Downtime Category")["Repair Cost EURO"].sum().sort_values(ascending=False)
labels = list(cat_cost.index) + ["Total"]
values = list(cat_cost.values) + [cat_cost.sum()]
cum = 0
for i, (lab, val) in enumerate(zip(labels, values)):
    if lab == "Total":
        ax4.bar(i, val, color=ACCENT2, width=0.6)
        ax4.text(i, val, f"€{val/1e6:.2f}M", ha="center", va="bottom", fontsize=7.5, color=TEXT)
    else:
        ax4.bar(i, val, bottom=cum, color=ACCENT, width=0.6)
        ax4.text(i, cum + val, f"€{val/1000:.0f}K", ha="center", va="bottom", fontsize=7, color=SUBTEXT)
        cum += val
ax4.set_xticks(range(len(labels)))
ax4.set_xticklabels(labels, rotation=40, ha="right", fontsize=7.5)
style_ax(ax4, "Repair Cost Waterfall — by Downtime Category (EUR)")

# ---------------- Treemap: downtime categories ----------------
ax5 = fig.add_subplot(gs[3:6, 6:12])
cat_hours = df.groupby("Downtime Category")["Downtime Hours"].sum().sort_values(ascending=False)
sizes = cat_hours.values
labels_tm = [f"{name}\n{val:,.0f} h" for name, val in zip(cat_hours.index, cat_hours.values)]
squarify.plot(sizes=sizes, label=labels_tm, color=PALETTE[:len(sizes)], ax=ax5,
              text_kwargs={"fontsize": 8.5, "color": "#0B0F17", "fontweight": "bold"}, pad=True,
              bar_kwargs={"linewidth": 1.5, "edgecolor": BG})
ax5.axis("off")
ax5.set_title("Treemap — Downtime Categories (Hours)", fontsize=11, color=TEXT, loc="left", fontweight="bold", pad=8)

fig.text(0.025, 0.008, "Source: Fact_Downtime_Events (synthetic dataset)  |  Portfolio project by Stephen  |  Built for Power BI", fontsize=7.5, color=SUBTEXT)

plt.savefig("/home/claude/project/images/02_deep_dive_analytics.png", facecolor=BG, bbox_inches="tight")
print("Saved 02_deep_dive_analytics.png")
