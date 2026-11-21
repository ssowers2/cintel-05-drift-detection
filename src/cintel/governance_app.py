"""Healthcare Metadata Governance Drift Monitor.

Continuous Intelligence | Project 05

Standalone Marimo application for monitoring drift in synthetic
healthcare metadata governance metrics.

The application compares two six-week observation periods and
identifies changes exceeding an interactive percentage-point threshold.

Run locally:
    uv run marimo run src/cintel/governance_app.py

Edit:
    uv run marimo edit src/cintel/governance_app.py

Data:
    data/governance_metrics_timeseries.csv

This application uses synthetic data only.
"""

import marimo

__generated_with = "0.25.0"

app = marimo.App(width="medium")


# ============================================================
# IMPORTS
# ============================================================


@app.cell
async def _():
    import sys

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(["polars", "plotly"])

    import marimo as mo
    import plotly.graph_objects as go
    import polars as pl

    return go, mo, pl, sys


# ============================================================
# APPLICATION TITLE AND INTRODUCTION
# ============================================================


@app.cell
def _(mo):
    mo.md(
        r"""
        # Healthcare Metadata Governance Drift Monitor

        **Continuous Intelligence | Project 05**

        This interactive application evaluates changes in synthetic
        healthcare metadata governance metrics.

        It compares historical and current observations to identify
        changes that exceed a selected drift threshold.

        ### Governance Metrics

        - **Metadata completeness:** Percentage of required metadata
          fields populated.
        - **Ownership coverage:** Percentage of data assets with
          assigned owners.
        - **Stewardship coverage:** Percentage of data assets with
          assigned stewards.
        - **Documentation gaps:** Percentage of metadata
          documentation that is missing or incomplete.

        **Important:** Drift indicates a change exceeding the
        selected threshold. It does not automatically indicate
        a negative outcome.
        """
    )


# ============================================================
# LOAD GOVERNANCE DATA
# ============================================================


@app.cell
def _(mo, pl, sys):
    """Load governance metrics locally or in WebAssembly."""
    _notebook_location = mo.notebook_location()

    if _notebook_location is None:
        raise RuntimeError("Unable to determine notebook location.")

    _filename = "governance_metrics_timeseries.csv"

    if sys.platform == "emscripten":
        from pyodide.http import (
            open_url as _open_url,
        )  # ty: ignore[unresolved-import]

        _url = _notebook_location / "public" / _filename

        governance_df = pl.read_csv(
            _open_url(str(_url)),
            try_parse_dates=True,
        )

    else:
        _data_path = _notebook_location.parents[1] / "data" / _filename

        governance_df = pl.read_csv(
            _data_path,
            try_parse_dates=True,
        )

    governance_df = governance_df.sort("week")

    return (governance_df,)


# ============================================================
# PERIOD INFORMATION
# ============================================================


@app.cell
def _(mo):
    mo.md(
        """
        ## Monitoring Periods

        The dataset contains **12 weekly observations** divided
        into two comparison periods.

        - **Reference period:** August 24–September 28, 2026
          (first six weeks).
        - **Current period:** October 5–November 9, 2026
          (final six weeks).

        Changes are calculated as:

        **Current period average − Reference period average**

        The resulting differences are expressed in
        **percentage points (pp)**.
        """
    )


# ============================================================
# INTERACTIVE THRESHOLD
# ============================================================


@app.cell
def _(mo):
    governance_threshold = mo.ui.slider(
        start=0,
        stop=50,
        step=1,
        value=20,
        label="Drift threshold (percentage points)",
        show_value=True,
    )

    mo.vstack(
        [
            mo.md(
                "## Interactive Drift Threshold\n\n"
                "Adjust the threshold to explore how the "
                "sensitivity of drift detection changes."
            ),
            governance_threshold,
        ]
    )

    return (governance_threshold,)


# ============================================================
# CALCULATE GOVERNANCE DRIFT
# ============================================================


@app.cell
def _(governance_df, governance_threshold, pl):
    """Calculate reference/current averages and drift flags."""
    _metrics = [
        (
            "metadata_completeness_pct",
            "Metadata Completeness",
        ),
        (
            "ownership_pct",
            "Ownership Coverage",
        ),
        (
            "stewardship_pct",
            "Stewardship Coverage",
        ),
        (
            "documentation_gaps_pct",
            "Documentation Gaps",
        ),
    ]

    _reference = governance_df.head(6)
    _current = governance_df.tail(6)

    _rows = []

    for _column, _label in _metrics:
        _reference_mean = _reference[_column].mean()
        _current_mean = _current[_column].mean()

        _difference = _current_mean - _reference_mean

        _drift = abs(_difference) > governance_threshold.value

        _rows.append(
            {
                "Metric": _label,
                "Reference Mean (%)": round(_reference_mean, 2),
                "Current Mean (%)": round(_current_mean, 2),
                "Change (pp)": round(_difference, 2),
                "Threshold (pp)": (governance_threshold.value),
                "Drift": _drift,
            }
        )

    governance_results_df = pl.DataFrame(_rows)

    return (governance_results_df,)


# ============================================================
# GOVERNANCE RESULTS TABLE
# ============================================================


@app.cell
def _(governance_results_df, mo):
    mo.vstack(
        [
            mo.md("## Governance Drift Results"),
            mo.ui.table(governance_results_df),
        ]
    )


# ============================================================
# GOVERNANCE SUMMARY
# ============================================================


@app.cell
def _(governance_results_df, governance_threshold, mo):
    _results = governance_results_df.to_dicts()

    _flagged = sum(1 for _row in _results if _row["Drift"])

    _total = len(_results)

    mo.md(
        f"""
        ### Drift Detection Summary

        **{_flagged} of {_total} governance metrics**
        exceed the selected threshold of
        **{governance_threshold.value} percentage points**.

        The drift flags identify changes requiring
        interpretation rather than automatically
        identifying data quality problems.
        """
    )


# ============================================================
# INTERACTIVE GOVERNANCE VISUALIZATION
# ============================================================


@app.cell
def _(go, governance_results_df, governance_threshold, mo):
    """Create an interactive horizontal drift chart."""
    _results = governance_results_df.to_dicts()

    _labels = [_row["Metric"] for _row in _results]

    _changes = [_row["Change (pp)"] for _row in _results]

    _flags = [_row["Drift"] for _row in _results]

    _threshold = governance_threshold.value

    _colors = ["#147D73" if _flag else "#9AA7B1" for _flag in _flags]

    _fig = go.Figure()

    _fig.add_trace(
        go.Bar(
            x=_changes,
            y=_labels,
            orientation="h",
            marker_color=_colors,
            text=[f"{_value:+.2f} pp" for _value in _changes],
            textposition="outside",
            hovertemplate=("%{y}<br>Change: %{x:+.2f} pp<extra></extra>"),
        )
    )

    _fig.add_vline(
        x=_threshold,
        line_dash="dash",
        line_color="#D97706",
    )

    _fig.add_vline(
        x=-_threshold,
        line_dash="dash",
        line_color="#D97706",
    )

    _fig.add_vline(
        x=0,
        line_color="#344054",
    )

    _fig.update_layout(
        title="Healthcare Metadata Governance Drift",
        xaxis_title="Change in Percentage Points",
        yaxis_title="",
        yaxis={"autorange": "reversed"},
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        height=440,
        margin={
            "l": 170,
            "r": 65,
            "t": 70,
            "b": 65,
        },
        font={"size": 13},
    )

    _fig.update_xaxes(
        range=[-55, 55],
        showgrid=True,
        gridcolor="#E5E7EB",
        zeroline=False,
    )

    mo.vstack(
        [
            mo.md("## Interactive Governance Visualization"),
            mo.md(
                "Teal bars indicate detected drift. "
                "Gray bars indicate changes below the "
                "selected threshold. Orange dashed lines "
                "show the threshold boundaries."
            ),
            mo.ui.plotly(_fig),
            mo.md(
                "*Synthetic data | Reference: Aug 24–Sep 28, "
                "2026 | Current: Oct 5–Nov 9, 2026*"
            ),
        ]
    )


# ============================================================
# INTERPRETATION
# ============================================================


@app.cell
def _(mo):
    mo.md(
        """
        ## Interpreting Governance Drift

        Drift is not necessarily negative. The direction of
        change must be considered alongside the meaning
        of each metric.

        - **Metadata completeness:** Higher values generally
          indicate improved metadata coverage.
        - **Ownership coverage:** Higher values generally
          indicate more assets with assigned owners.
        - **Stewardship coverage:** Higher values generally
          indicate more assets with assigned stewards.
        - **Documentation gaps:** Lower values generally
          indicate fewer missing documentation elements.

        At the default threshold of **20 percentage points**,
        three of the four metrics are flagged as drifting.

        All four metrics move in favorable directions in the
        synthetic dataset.

        ### Limitations

        The analysis compares averages from two six-week
        periods using a fixed, user-adjustable threshold.

        The selected threshold is illustrative and is not
        an established healthcare governance standard.

        The method does not evaluate statistical significance,
        variability, or seasonal patterns.

        **These results are based entirely on synthetic data
        and do not represent actual healthcare organizational
        performance.**
        """
    )


# ============================================================
# PROJECT LINKS
# ============================================================


@app.cell
def _(mo):
    mo.md(
        """
        ---

        ### Project Resources

        [Project 05 Documentation](https://ssowers2.github.io/cintel-05-drift-detection/)

        [GitHub Repository](https://github.com/ssowers2/cintel-05-drift-detection)

        [Project 04 Governance Dashboard](https://ssowers2.github.io/cintel-04-rolling-monitoring/governance/)
        """
    )


if __name__ == "__main__":
    app.run()
