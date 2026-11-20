# Detecting Changes in System Behavior

Continuous Intelligence | Project 05 | Example Report

## Overview

This project examines whether recent system behavior
differs meaningfully from an earlier reference period.

The objective is to detect changes in operational metrics
that may indicate a need for investigation.

## Data

Two datasets represent different observation periods:

- Reference data representing earlier behavior.
- Current data representing more recent behavior.

Each contains measurements of requests,
errors, and total latency.

[View Data](https://github.com/ssowers2/cintel-05-drift-detection/tree/main/data)

## Methods

The pipeline calculates the mean of each metric
for both observation periods.

It then calculates:

    difference = current_mean - reference_mean

Drift is flagged when the absolute difference
exceeds the configured threshold.

The original example uses the following thresholds:

- Requests: 20.
- Errors: 2.
- Total latency: 1,000 milliseconds.

These thresholds are illustrative and should
be justified for a production monitoring system.

## Results

The original example compared historical and current system metrics. All three metrics were initially flagged as drifting.

| Metric | Reference Mean | Current Mean | Difference | Modified Threshold | Drift Flag |
|---|---:|---:|---:|---:|---|
| Requests | 128.3 | 164.5 | +36.2 | 40.0 | False |
| Errors | 2.3 | 6.3 | +4.0 | 2.0 | True |
| Total latency (ms) | 3,835 | 5,670 | +1,835 | 1,000 | True |

After increasing the requests drift threshold from 20.0 to 40.0, requests were no longer flagged as drifting. Errors and latency remained flagged because their differences still exceeded the configured thresholds.

In the original example, all three metrics exceeded their configured thresholds. After increasing the requests threshold to 40.0, only errors and latency were flagged as drifting.

[View Drift Results](https://github.com/ssowers2/cintel-05-drift-detection/tree/main/artifacts)

[View Detailed Summary](https://github.com/ssowers2/cintel-05-drift-detection/tree/main/artifacts)

## Custom Modifications

### Adjusting the Requests Drift Threshold

**Change:** Updated `REQUESTS_DRIFT_THRESHOLD` from `20.0` to `40.0` in `src/cintel/drift_detector.py`.

**Reason:** To evaluate how increasing a drift threshold affects which metrics are flagged as drifting.

**Prediction:** If the requests drift threshold increases from 20.0 to 40.0, requests will no longer be flagged as drifting because the observed difference of 36.2 is below the new threshold.

**Verification:** Used `git status` and `git diff` to confirm that only the requests threshold was changed.

**Results:** The prediction was confirmed. The requests drift flag changed from `True` to `False`, while the errors and latency drift flags remained `True`. The pipeline executed successfully.

**Conclusion:** Increasing the threshold made drift detection less sensitive to changes in request volume without affecting the underlying measurements.

## Interpretation

The current period shows higher average request volume,
higher average errors, and greater total latency.

These changes suggest that the system is operating
differently from its reference behavior.

An analyst could investigate whether the changes
reflect increased workload, changing demand,
or a potential performance problem.

Although request volume increased, the modified
threshold no longer flags it as drifting.This demonstrates how
threshold selection influences which changes are identified
for further investigation.

## Limitations

The approach compares means using fixed thresholds.

It does not account for variability,
statistical significance, or seasonal patterns.

Higher request volume may also explain part
of the increase in errors and total latency.

Additional normalized signals, such as error rate
and average latency per request, would help
distinguish workload changes from degraded performance.

## Conclusion

Baseline comparisons provide a practical starting point
for detecting changes in operational behavior.

Drift indicators are evidence for investigation,
not proof that a system is malfunctioning.

## Documentation Index

- **Home** - this landing page
- [**Project Instructions**](project-instructions.md)
- [**Glossary**](glossary.md)
- [**API**](api.md)
- [**Reactive App**](./app/index.html)

## Project Links

- [GitHub Repository](https://github.com/ssowers2/cintel-05-drift-detection)
- [Example Pipeline](https://github.com/ssowers2/cintel-05-drift-detection/tree/main/src/cintel)
- [Results and Artifacts](https://github.com/ssowers2/cintel-05-drift-detection/tree/main/artifacts)

## Project Resources

- [Project Instructions](project-instructions.md)
- [Professional Python Guide](https://denisecase.github.io/pro-analytics-02/)
- [Professional Python Project Explainer](https://pup-pack.github.io/professional-python-project-explainer/).
- [Suggested Datasets](https://denisecase.github.io/pro-analytics-02/reference/datasets/cintel/)
