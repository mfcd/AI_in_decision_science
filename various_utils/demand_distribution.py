"""Plot the distribution of demand for a fictional product.

Demand ~ Normal(mean=100, std=15)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

MEAN = 100
STD = 15
N_SAMPLES = 10_000

BLUE = "#3B82F6"      # single hue for a single series
INK = "#1F2937"       # text / labels
MUTED = "#6B7280"     # gridlines, secondary text

rng = np.random.default_rng(42)
demand = rng.normal(MEAN, STD, N_SAMPLES)

fig, ax = plt.subplots(figsize=(9, 5.5))

# Histogram of sampled demand
counts, bins, patches = ax.hist(
    demand, bins=40, density=True, color=BLUE, alpha=0.55,
    edgecolor="white", linewidth=0.5, label="data",
)

# Theoretical normal curve on top
x = np.linspace(MEAN - 4 * STD, MEAN + 4 * STD, 400)
ax.plot(x, norm.pdf(x, MEAN, STD), color=BLUE, linewidth=2.5, label="Normal fit")

# Mean and +/- 1 std reference lines
ax.axvline(MEAN, color=INK, linewidth=1.5, linestyle="--")
ax.text(MEAN, ax.get_ylim()[1] * 0.96, f"mean = {MEAN}", color=INK,
        ha="center", va="top", fontsize=10)

for sign, label in [(-1, "-1σ"), (1, "+1σ")]:
    xv = MEAN + sign * STD
    ax.axvline(xv, color=MUTED, linewidth=1, linestyle=":")
    ax.text(xv, ax.get_ylim()[1] * 0.02, label, color=MUTED,
            ha="center", va="bottom", fontsize=9)

ax.set_title("Distribution of Product Demand", fontsize=14, color=INK, pad=14)
ax.set_xlabel("Units demanded", fontsize=11, color=INK)
ax.set_ylabel("Probability density", fontsize=11, color=INK)
ax.tick_params(colors=MUTED)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color(MUTED)
ax.spines["bottom"].set_color(MUTED)
ax.grid(axis="y", color=MUTED, alpha=0.2, linewidth=0.6)
ax.legend(frameon=False, loc="upper right")

fig.tight_layout()
fig.savefig("demand_distribution.png", dpi=150)
try:
    plt.show()
except Exception:
    pass

print(f"Sampled {N_SAMPLES} demand values: mean={demand.mean():.2f}, std={demand.std():.2f}")
