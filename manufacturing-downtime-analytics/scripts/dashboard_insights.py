import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import gridspec

BG = "#0B0F17"
PANEL = "#121826"
GRID = "#232B3D"
TEXT = "#E7ECF3"
SUBTEXT = "#8B95A7"
ACCENT = "#F5A623"
ACCENT2 = "#33C6F4"
ACCENT3 = "#EF5B5B"
ACCENT4 = "#5FD87A"

plt.rcParams.update({
    "figure.facecolor": BG, "text.color": TEXT, "font.family": "DejaVu Sans", "font.size": 10,
})

fig = plt.figure(figsize=(21, 12.5), dpi=150)
fig.patch.set_facecolor(BG)

fig.text(0.025, 0.965, "MANUFACTURING DOWNTIME ANALYTICS", fontsize=22, fontweight="bold", color=TEXT)
fig.text(0.025, 0.945, "Executive Insights  |  Key Findings & Recommendations  |  Jan 2023 – Dec 2024", fontsize=11, color=SUBTEXT)

def panel(x, y, w, h, title, color=ACCENT):
    ax = fig.add_axes([x, y, w, h])
    ax.set_facecolor(PANEL)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color(GRID)
    ax.add_patch(mpatches.Rectangle((0, 0.93), 1, 0.07, transform=ax.transAxes, color=color, clip_on=True))
    ax.text(0.035, 0.83, title, fontsize=12.5, fontweight="bold", color=TEXT, transform=ax.transAxes, va="top")
    return ax

def bullet_text(ax, lines, y_start=0.68, dy=0.155, fontsize=10.2, color=TEXT):
    y = y_start
    for line in lines:
        ax.text(0.05, y, "•", fontsize=fontsize, color=ACCENT2, transform=ax.transAxes, va="top")
        ax.text(0.085, y, line, fontsize=fontsize, color=color, transform=ax.transAxes, va="top", wrap=True)
        y -= dy

# ---------------- Row 1: 4 "finding" cards ----------------
w = 0.225
gap = 0.017
x0 = 0.025
y0 = 0.60
h0 = 0.30

ax1 = panel(x0, y0, w, h0, "Worst-Performing Plant", ACCENT3)
ax1.text(0.05, 0.68, "Plant C – Katowice", fontsize=15, fontweight="bold", color=TEXT, transform=ax1.transAxes)
ax1.text(0.05, 0.52, "2,371 downtime hours  |  €1.22M repair cost", fontsize=9.5, color=SUBTEXT, transform=ax1.transAxes)
ax1.text(0.05, 0.38, "1,175 events — highest of all 4 plants", fontsize=9.5, color=SUBTEXT, transform=ax1.transAxes)
ax1.text(0.05, 0.20, "Accounts for ~33% of total downtime hours\nacross the network.", fontsize=9, color=TEXT, transform=ax1.transAxes)

ax2 = panel(x0 + w + gap, y0, w, h0, "Highest-Cost Machine", ACCENT)
ax2.text(0.05, 0.68, "MC-7027", fontsize=15, fontweight="bold", color=TEXT, transform=ax2.transAxes)
ax2.text(0.05, 0.52, "Assembly Robot — Plant C, Katowice", fontsize=9.5, color=SUBTEXT, transform=ax2.transAxes)
ax2.text(0.05, 0.38, "€120,559 in cumulative repair cost", fontsize=9.5, color=SUBTEXT, transform=ax2.transAxes)
ax2.text(0.05, 0.20, "76 events — a strong candidate for\nreplacement or predictive maintenance.", fontsize=9, color=TEXT, transform=ax2.transAxes)

ax3 = panel(x0 + 2 * (w + gap), y0, w, h0, "Most Common Downtime Reason", ACCENT2)
ax3.text(0.05, 0.68, "Motor Burnout", fontsize=15, fontweight="bold", color=TEXT, transform=ax3.transAxes)
ax3.text(0.05, 0.52, "181 events (4.3% of all events)", fontsize=9.5, color=SUBTEXT, transform=ax3.transAxes)
ax3.text(0.05, 0.38, "Belt Breakage drives the most hours (406 h)", fontsize=9.5, color=SUBTEXT, transform=ax3.transAxes)
ax3.text(0.05, 0.20, "Mechanical Failure is the #1 category —\n19.6% of all logged events.", fontsize=9, color=TEXT, transform=ax3.transAxes)

ax4 = panel(x0 + 3 * (w + gap), y0, w, h0, "Highest Downtime Months", ACCENT4)
ax4.text(0.05, 0.68, "Dec 2023 & Dec 2024", fontsize=15, fontweight="bold", color=TEXT, transform=ax4.transAxes)
ax4.text(0.05, 0.52, "380 h and 359 h respectively", fontsize=9.5, color=SUBTEXT, transform=ax4.transAxes)
ax4.text(0.05, 0.38, "July also elevated both years (346–357 h)", fontsize=9.5, color=SUBTEXT, transform=ax4.transAxes)
ax4.text(0.05, 0.20, "Consistent seasonal pattern: year-end\npeak production strain + summer heat load.", fontsize=9, color=TEXT, transform=ax4.transAxes)

# ---------------- Row 2: Key findings narrative + cost breakdown ----------------
ax5 = panel(0.025, 0.31, 0.47, 0.265, "Key Findings", ACCENT)
bullet_text(ax5, [
    "Unplanned downtime accounts for 73.8% of all events and 79.1% of total",
    "hours — and 83.7% of total repair cost, confirming that reactive",
    "maintenance is significantly more expensive than planned work.",
    "Mechanical and Electrical Failures together represent 33.5% of all",
    "events — the two categories with the greatest cost-reduction potential.",
    "705 events remain in Pending status, representing a maintenance",
    "backlog that should be reviewed and closed out.",
], y_start=0.72, dy=0.145, fontsize=9.6)

ax6 = panel(0.025 + 0.47 + 0.02, 0.31, 0.47, 0.265, "Cost & Reliability Snapshot", ACCENT2)
bullet_text(ax6, [
    "Total repair cost across the network: €3.63M over 24 months",
    "(~€151K per month on average).",
    "Corrective (1,663) and Emergency (845) maintenance events combined",
    "outnumber Preventive (515) and Predictive (164) by more than 3-to-1 —",
    "the network is still largely reactive rather than proactive.",
    "409,796 production units were lost to downtime over the 2-year period.",
], y_start=0.72, dy=0.145, fontsize=9.6)

# ---------------- Row 3: Recommendations ----------------
ax7 = panel(0.025, 0.03, 0.955, 0.255, "Recommendations to Reduce Downtime & Maintenance Cost", ACCENT4)
col_w = 0.955 / 3
recs_1 = [
    "Shift the maintenance mix toward Predictive/",
    "Preventive: expand vibration & thermal sensors",
    "on the top 10 costliest machines (led by",
    "MC-7027) to catch failures before breakdown.",
]
recs_2 = [
    "Target Plant C – Katowice with a focused",
    "reliability audit: it drives ~33% of network",
    "downtime hours despite being mid-sized —",
    "root-cause the Mechanical/Electrical spike.",
]
recs_3 = [
    "Build a seasonal maintenance calendar around",
    "the Nov–Dec and Jul peaks (pre-emptive",
    "servicing before high-strain periods) and",
    "clear the 705-event pending backlog monthly.",
]
for i, recs in enumerate([recs_1, recs_2, recs_3]):
    xrel = 0.025 + i * (1/3)
    y = 0.58
    ax7.text(xrel + 0.06, y, str(i+1), fontsize=20, fontweight="bold", color=ACCENT4, transform=ax7.transAxes, va="top")
    yy = y - 0.02
    for line in recs:
        ax7.text(xrel + 0.13, yy, line, fontsize=9.3, color=TEXT, transform=ax7.transAxes, va="top")
        yy -= 0.135

fig.text(0.025, 0.008, "Source: Fact_Downtime_Events (synthetic dataset)  |  Portfolio project by Stephen  |  Built for Power BI", fontsize=7.5, color=SUBTEXT)

plt.savefig("/home/claude/project/images/03_executive_insights.png", facecolor=BG, bbox_inches="tight")
print("Saved 03_executive_insights.png")
