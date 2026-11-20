# Governance Drift Detection — Data Card

## Dataset

Synthetic Healthcare Metadata Governance Metrics

## Source

The governance data was carried forward from Continuous Intelligence Project 04: Rolling Monitoring.

Source repository:
https://github.com/ssowers2/cintel-04-rolling-monitoring

## Files

- `data/governance_metrics_timeseries.csv` — 12 weekly governance observations.
- `data/governance_inventory_timeseries.csv` — supporting asset-level metadata observations.

## Data Description

The weekly dataset contains four governance metrics:

- Metadata completeness (%)
- Data ownership coverage (%)
- Data stewardship coverage (%)
- Documentation gaps (%)

## Data Privacy and Usage

The dataset is described as synthetic healthcare metadata and is not intended to contain actual patient information.

The original data-generation method and applicable license or usage terms should be confirmed from the Project 04 source files.

## Analytical Decisions

### Reference Period

First six weeks: August 24–September 28, 2026.

### Current Period

Last six weeks: October 5–November 9, 2026.

### Comparison Method

Calculate the mean of each governance metric for both periods.

Difference = Current Mean - Reference Mean

### Drift Thresholds

An illustrative threshold of 20 percentage points is applied to all four metrics.

Drift is flagged when the absolute difference exceeds the threshold.

### Interpretation

A drift flag identifies a substantial change, not necessarily a problem.

In this dataset, increases in completeness, ownership, and stewardship coverage and decreases in documentation gaps represent favorable changes.

## Output

`artifacts/governance_drift_summary.csv`
