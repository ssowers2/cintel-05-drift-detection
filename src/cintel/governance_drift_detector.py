"""Detect changes in synthetic healthcare metadata governance metrics.

Continuous Intelligence - Project 05
Data source: Project 04 governance_metrics_timeseries.csv
"""

import logging
from pathlib import Path

from datafun_toolkit.logger import get_logger, log_header, log_path
import polars as pl

# Configure logging
LOG: logging.Logger = get_logger("P5-GOV", level="DEBUG")

# Define file paths
ROOT_DIR = Path.cwd()
DATA_FILE = ROOT_DIR / "data" / "governance_metrics_timeseries.csv"


def main() -> None:
    """Load and inspect the governance monitoring dataset."""
    log_header(LOG, "Governance Drift Detection")
    log_path(LOG, "DATA_FILE", DATA_FILE)

    # Read weekly governance measurements
    governance_df = pl.read_csv(DATA_FILE, try_parse_dates=True)

    LOG.info(f"Loaded {governance_df.height} governance records")
    LOG.info("Governance dataset columns:")
    LOG.info(governance_df.columns)

    LOG.info("Governance data preview:")
    LOG.info(governance_df.head(5))

    LOG.info("Governance data loaded successfully!")

    # STEP 2: Divide data into historical and current periods
    governance_df = governance_df.sort("week")

    reference_df = governance_df.head(6)
    current_df = governance_df.tail(6)

    LOG.info("Reference period:")
    LOG.info(reference_df.select("week"))

    LOG.info("Current period:")
    LOG.info(current_df.select("week"))

    LOG.info(f"Reference records: {reference_df.height}")
    LOG.info(f"Current records: {current_df.height}")

    LOG.info("Reference and current periods created successfully!")

    # STEP 3: Calculate average governance metrics for each period
    governance_metrics = [
        "metadata_completeness_pct",
        "ownership_pct",
        "stewardship_pct",
        "documentation_gaps_pct",
    ]

    reference_means = reference_df.select(
        [pl.col(metric).mean().alias(metric) for metric in governance_metrics]
    )

    current_means = current_df.select(
        [pl.col(metric).mean().alias(metric) for metric in governance_metrics]
    )

    LOG.info("Reference period averages:")
    LOG.info(reference_means)

    LOG.info("Current period averages:")
    LOG.info(current_means)

    LOG.info("Governance period averages calculated successfully!")

    # STEP 4: Calculate differences between current and reference averages
    reference_values = reference_means.to_dicts()[0]
    current_values = current_means.to_dicts()[0]

    differences = {
        metric: current_values[metric] - reference_values[metric]
        for metric in governance_metrics
    }

    LOG.info("Governance metric changes (percentage points):")

    for metric, difference in differences.items():
        LOG.info(f"{metric}: {difference:+.2f} percentage points")

    LOG.info("Governance differences calculated successfully!")

    # STEP 5: Apply governance drift thresholds
    # Thresholds are illustrative and measured in percentage points.
    drift_thresholds = {
        "metadata_completeness_pct": 20.0,
        "ownership_pct": 20.0,
        "stewardship_pct": 20.0,
        "documentation_gaps_pct": 20.0,
    }

    drift_flags = {
        metric: abs(differences[metric]) > drift_thresholds[metric]
        for metric in governance_metrics
    }

    LOG.info("Governance drift detection results:")

    for metric in governance_metrics:
        LOG.info(
            f"{metric}: "
            f"change={differences[metric]:+.2f} pp, "
            f"threshold={drift_thresholds[metric]:.2f} pp, "
            f"drift={drift_flags[metric]}"
        )

    # STEP 6: Save governance drift results as a CSV artifact
    artifacts_dir = ROOT_DIR / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    output_file = artifacts_dir / "governance_drift_summary.csv"

    summary_df = pl.DataFrame(
        {
            "metric": governance_metrics,
            "reference_mean_pct": [
                reference_values[metric] for metric in governance_metrics
            ],
            "current_mean_pct": [
                current_values[metric] for metric in governance_metrics
            ],
            "difference_pp": [differences[metric] for metric in governance_metrics],
            "threshold_pp": [drift_thresholds[metric] for metric in governance_metrics],
            "drift_flag": [drift_flags[metric] for metric in governance_metrics],
        }
    )

    summary_df.write_csv(output_file)

    LOG.info("Governance drift summary:")
    LOG.info(summary_df)
    log_path(LOG, "OUTPUT_FILE", output_file)
    LOG.info("Governance drift artifact saved successfully!")


if __name__ == "__main__":
    main()
