
# cintel-05-drift-detection

[![Python 3.14](https://img.shields.io/badge/python-3.14%2B-blue?logo=python)](pyproject.toml)
[![CI](https://github.com/ssowers2/cintel-05-drift-detection/actions/workflows/ci-python-zensical.yml/badge.svg)](https://github.com/ssowers2/cintel-05-drift-detection/actions/workflows/ci-python-zensical.yml)
[![Documentation](https://img.shields.io/badge/docs-site-blue?logo=github)](https://ssowers2.github.io/cintel-05-drift-detection/)

[![uv managed](https://img.shields.io/badge/uv-managed-DE5FE9)](https://docs.astral.sh/uv/)
[![ty type checked](https://img.shields.io/badge/ty-type_checked-2F80ED)](https://docs.astral.sh/ty/)
[![Zensical docs](https://img.shields.io/badge/Zensical-docs-purple)](https://zensical.org/)
[![MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

> Detecting meaningful changes in healthcare metadata quality and governance readiness using Python, Polars, and drift detection techniques.

## Project Overview

**Author:** Sabriya Sowers
**Date:** November 2026
**Course:** Continuous Intelligence – Project 05

This project introduces drift detection by comparing current measurements against historical reference data to identify changes that exceed defined thresholds.

The project will extend the **Metadata Completeness & Governance Readiness Monitor** developed in previous Continuous Intelligence assignments.

Project 03 introduced data governance metrics and signals. Project 04 expanded the project with weekly monitoring, rolling averages, and an interactive dashboard.

Project 05 will build on that work by introducing drift detection to identify changes in metadata quality, ownership, and stewardship coverage that may require further investigation.

The project uses synthetic healthcare metadata and does not contain actual patient information.

Project configuration is maintained in [pyproject.toml](pyproject.toml).

## Project Progression

| Project | Focus | Governance Application |
|---|---|---|
| Project 03 | Signals and feature engineering | Established metadata quality and governance metrics |
| Project 04 | Rolling monitoring | Tracked governance metrics over time using rolling averages and an interactive dashboard |
| Project 05 | Drift detection | Planned comparison of historical and current governance metrics to identify meaningful changes |

**Previous project:** [Project 04 – Rolling Monitoring](https://github.com/ssowers2/cintel-04-rolling-monitoring)

**Previous dashboard:** [Governance Monitoring Dashboard](https://ssowers2.github.io/cintel-04-rolling-monitoring/governance/)

## Data

### Instructor's Example Data

The original example uses two datasets from the `data/` directory:

- **Reference data:** Measurements representing earlier system behavior.
- **Current data:** Measurements representing more recent system behavior.

Both datasets contain:

- `requests` – number of requests handled.
- `errors` – number of failed requests.
- `total_latency_ms` – total response time in milliseconds.

### Planned Custom Governance Data

The custom project will build on the synthetic healthcare metadata used in Project 04.

The planned metrics include:

- **Metadata completeness:** Percentage of required metadata fields populated.
- **Data ownership coverage:** Percentage of assets with assigned data owners.
- **Stewardship coverage:** Percentage of assets with assigned data stewards.
- **Documentation gaps:** Missing or incomplete metadata documentation.

Historical measurements will serve as the reference period, while more recent measurements will be evaluated for potential drift.

## Approach

### Instructor's Example

The example pipeline uses Polars to:

1. Calculate summary statistics for reference and current data.
2. Calculate differences between the two periods.
3. Compare the differences against defined thresholds.
4. Flag measurements that indicate possible drift.
5. Save the results as CSV artifacts.

### Planned Governance Customization

The custom implementation will follow a similar approach:

1. Reuse the synthetic governance metrics developed in Project 04.
2. Establish a historical baseline for selected governance metrics.
3. Compare more recent measurements against the baseline.
4. Apply thresholds to identify potentially meaningful changes.
5. Generate drift flags for metrics requiring further review.
6. Explore visualizations to communicate the results.

The goal is to demonstrate how drift detection can support ongoing data quality monitoring and help identify changes that may require investigation.

Drift flags will be treated as indicators for review rather than automatic evidence of a data quality problem.

## Project Components

- [pyproject.toml](pyproject.toml) – project configuration and dependencies.
- [src/cintel/drift_detector.py](src/cintel/drift_detector.py) – example drift detection pipeline.
- [src/cintel/app.py](src/cintel/app.py) – reactive Marimo application.
- [data/](data/) – reference and current measurements.
- [artifacts/](artifacts/) – generated comparisons and results.
- [tests/](tests/) – automated tests.
- [.github/workflows/](.github/workflows/) – automated checks and documentation deployment.
- [docs/](docs/) – project documentation.

Additional governance-specific files and artifacts will be documented as the customization is developed.

## Run the Project

Follow the [Professional Python Workflow Guide](https://denisecase.github.io/pro-analytics-02/) to set up the project environment.

From the VS Code terminal in the project root:

```shell
uv run python -m cintel.drift_detector
```

## Run the Reactive App

From the VS Code terminal in the project root:

```shell
uv run marimo run src/cintel/app.py
```

Press `CTRL + C` to stop the application.

## Results

The instructor's example pipeline produces:

- `artifacts/drift_summary.csv` – summary comparisons and drift flags.
- `artifacts/drift_summary_long.csv` – comparison results in a longer format.
- `artifacts/drift_stats.csv` – statistical comparison of error rates.

The pipeline also creates a `project.log` file.

Successful execution produces:

```text
========================
Pipeline executed successfully!
========================
```

### Planned Custom Results

The governance customization is expected to produce:

- Historical and current governance metric comparisons.
- Differences between baseline and recent measurements.
- Drift flags based on selected thresholds.
- Visualizations highlighting changes in governance metrics.
- Interpretation of findings and possible areas for investigation.

Results will be added after the custom pipeline is implemented and tested.

## Verification

Run automated tests:

```shell
uv run pytest
```

Additional tests will be added as needed for the governance drift detection implementation.

## Project Documentation

The [hosted documentation site](https://ssowers2.github.io/cintel-05-drift-detection/) is published using Zensical and GitHub Pages.

The documentation will present the project report, including:

- Data
- Methods
- Results
- Visualizations
- Interpretation
- Limitations
- Conclusions

The final report will explain how drift detection extends the governance monitoring work from Project 04.

## CI/CD and GitHub Actions

This project includes continuous integration and continuous deployment (CI/CD) to check project files and publish documentation.

GitHub Actions include:

- [CI: Python and Documentation Checks](https://github.com/ssowers2/cintel-05-drift-detection/actions/workflows/ci-python-zensical.yml)
- [CD: Documentation Deployment](https://github.com/ssowers2/cintel-05-drift-detection/actions/workflows/deploy-zensical.yml)

## Developer Reference

Follow the [Professional Python Workflow Guide](https://denisecase.github.io/pro-analytics-02/) for detailed instructions and troubleshooting.

### Initialize and Update the Python Environment

From the VS Code terminal:

```shell
uvx pup-clean --delete
uv self update
uv python pin 3.14
uv python install
uv lock --upgrade
uv sync
uv audit
```

### Set Up and Run Git Hooks

```shell
uvx prek install --force
uvx prek update --freeze --cooldown-days 7

git add -A
uvx prek run --all-files

# Repeat if changes were made
uvx prek run --all-files
```

### Run Common Chores

Run linters, formatters, type checks, tests, and build documentation.

```shell
uv run ruff check . --fix
uv run ruff format .

uv run ty check
uv run python -m pytest
uv run python -m zensical build
```

### Git Add, Commit, and Push

```shell
git add -A
git commit -m "describe your changes in quotes"
git push -u origin main
```

## Developer Notes

- Use the **UP ARROW** and **DOWN ARROW** in the terminal to scroll through previous commands.
- Use `CTRL + F` to find text within a file.
- Review generated artifacts and test results before committing changes.

## Developer Tools

This project uses professional Python tools for development, testing, documentation, and code quality.

- [uv](https://docs.astral.sh/uv/) – Python environments and dependencies.
- [Ruff](https://docs.astral.sh/ruff/) – Python linting and formatting, configured in [.ruff.toml](.ruff.toml).
- [ty](https://docs.astral.sh/ty/) – Python type checking.
- [pytest](https://docs.pytest.org/) – automated Python testing, configured in [.pytest.toml](.pytest.toml).
- [prek](https://prek.j178.dev/) – Git hooks and automated checks, configured in [prek.toml](prek.toml).
- [Zensical](https://zensical.org/) – project documentation, configured in [zensical.toml](zensical.toml).
- [Polars](https://pola.rs/) – DataFrame processing and analysis.
- [Marimo](https://marimo.io/) – reactive Python applications.

## Links

- [GitHub Repository](https://github.com/ssowers2/cintel-05-drift-detection)
- [Hosted Documentation](https://ssowers2.github.io/cintel-05-drift-detection/)
- [Project 04 Repository](https://github.com/ssowers2/cintel-04-rolling-monitoring)
- [Project 04 Governance Dashboard](https://ssowers2.github.io/cintel-04-rolling-monitoring/governance/)
- [Instructor's Project 05 Example](https://github.com/denisecase/cintel-05-drift-detection)
- [Professional Python Workflow Guide](https://denisecase.github.io/pro-analytics-02/)
- [Citation](CITATION.cff)
- [License](LICENSE)
