# Network Forensics Portfolio Project

A professional NetFlow-based forensic analysis project built around CIC-IDS-2017-style flow telemetry. This portfolio-ready repository demonstrates data ingestion, feature engineering, forensic analysis, visualization, and reporting for insider threat and DDoS detection using flow-level records.

## Project Overview

This project is designed to support a professional portfolio with:
- A structured network-forensics analysis pipeline
- Reproducible data processing and feature engineering
- Visualizations for suspicious flow detection, port analysis, traffic spikes, and anomaly patterns
- A polished report with research context, methodology, and forensic outcomes
- A sample notebook showing exploratory data analysis and results

## Features

- Load NetFlow-style CSV data and normalize records
- Engineer forensic features such as total bytes, total packets, flow rates, and internal/external host indicators
- Detect suspicious destination ports, outbound spike events, and port scanning behaviour
- Unsupervised anomaly detection via Isolation Forest
- Supervised traffic classification when labels are available
- Export polished markdown reports and visual artifacts
- SIEM-style Streamlit dashboard for rapid investigation

## Repository Structure

- `src/netflow_forensics/` — Python modules for loading, preprocessing, analysis, visualization, and reporting
- `data/` — sample dataset placeholder and data preparation helpers
- `notebooks/` — example Jupyter notebook for forensic analysis
- `docs/` — formal project report and documentation

## Installation

1. Create a Python environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. Run tests:

```powershell
pytest
```

## Usage

Run the forensic pipeline on a NetFlow CSV file:

```powershell
python src\main.py --input data\sample_netflow.csv --output docs\forensic_findings.md
```

Generate plot artifacts:

```powershell
python src\main.py --input data\sample_netflow.csv --output docs\forensic_findings.md --plots docs/plots
```

Start the SIEM-style dashboard with Streamlit:

```powershell
streamlit run src\dashboard.py
```

Use the notebook for a guided workflow:

```powershell
jupyter notebook notebooks/Network_Forensics_Analysis.ipynb
```

## Dataset

The CIC-IDS-2017 dataset is not included in this repository because of size and licensing restrictions. The code is designed to work with NetFlow-style CSV exports from that dataset or similar flow telemetry sources.

## Expandability

This project is intentionally modular and ready for further enhancements such as:
- machine learning-based anomaly detection
- integration with SIEM tools
- automated incident classification and alerting
- interactive dashboards
