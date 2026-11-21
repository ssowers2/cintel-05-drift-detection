"""Create a governance drift visualization from Project 05 results."""

from pathlib import Path

import matplotlib.pyplot as plt
import polars as pl

ROOT_DIR = Path.cwd()
INPUT_FILE = ROOT_DIR / "artifacts" / "governance_drift_summary.csv"
OUTPUT_FILE = ROOT_DIR / "artifacts" / "governance_drift_chart.png"


def main() -> None:
    """Create a horizontal chart of governance metric changes."""
    df = pl.read_csv(INPUT_FILE)

    labels = [
        "Metadata Completeness",
        "Ownership Coverage",
        "Stewardship Coverage",
        "Documentation Gaps",
    ]

    changes = df["difference_pp"].to_list()
    flags = df["drift_flag"].to_list()

    fig, ax = plt.subplots(figsize=(11, 6))

    colors = ["#147D73" if flag else "#9AA7B1" for flag in flags]

    bars = ax.barh(
        labels,
        changes,
        color=colors,
        height=0.55,
    )

    ax.axvline(0, color="#344054", linewidth=1.2)

    # Illustrative drift thresholds
    ax.axvline(20, color="#D97706", linestyle="--", linewidth=1.3)
    ax.axvline(-20, color="#D97706", linestyle="--", linewidth=1.3)

    for bar, value in zip(bars, changes, strict=True):
        x = value + 1 if value >= 0 else value - 1
        alignment = "left" if value >= 0 else "right"

        ax.text(
            x,
            bar.get_y() + bar.get_height() / 2,
            f"{value:+.2f} pp",
            va="center",
            ha=alignment,
            fontsize=11,
            fontweight="bold",
        )

    ax.invert_yaxis()
    ax.set_xlim(-35, 40)
    ax.set_xlabel("Change in Percentage Points")
    ax.set_title(
        "Healthcare Metadata Governance Drift",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )

    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis="x", alpha=0.15)
    ax.set_axisbelow(True)

    fig.text(
        0.5,
        0.01,
        "Synthetic data | Reference: Aug 24-Sep 28, 2026 | "
        "Current: Oct 5-Nov 9, 2026 | Threshold: +/-20 pp",
        ha="center",
        fontsize=9,
        color="#667085",
    )

    plt.tight_layout(rect=(0, 0.04, 1, 1))
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_FILE, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print(f"Governance visualization saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
