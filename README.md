# Network Forensics Portfolio Project

A professional NetFlow-based forensic analysis portfolio project built for scalable threat detection, incident investigation, and reporting.

## Project at a Glance

- Full end-to-end network forensics pipeline using NetFlow-style flow telemetry
- Investigative feature engineering, attack detection, and packetless incident reconstruction
- Unsupervised anomaly detection and supervised classification for threat validation
- Interactive Streamlit dashboard for SIEM-style analysis and triage
- Exportable reports, charts, and notebook-based forensic storytelling

## Project Summary

This repository demonstrates a full network-forensics workflow using NetFlow-style telemetry. It includes data ingestion, preprocessing, forensic analysis, visualization, machine learning, and an interactive SIEM-style dashboard.

## Portfolio Highlights

- Reproducible Python-based analysis pipeline for flow telemetry
- Forensic feature engineering and attack pattern detection
- Unsupervised anomaly detection and supervised classification
- Clean, exportable markdown reporting and visual artifacts
- Interactive Streamlit dashboard for threat triage
- Example Jupyter notebook for exploratory investigation

## What’s Included

- `src/netflow_forensics/` — core Python modules for data loading, preprocessing, analysis, visualization, and reporting
- `src/main.py` — command-line entrypoint for running the forensic pipeline
- `src/dashboard.py` — Streamlit application for SIEM-style analysis
- `docs/` — portfolio report, findings summary, and generated plots
- `notebooks/` — guided analysis notebook for reproducibility and presentation
- `tests/` — validation suite for the pipeline

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

3. Validate the project:

```powershell
pytest
```

## Usage

Run the forensic pipeline and generate a findings report:

```powershell
python src\main.py --input data\sample_netflow.csv --output docs\forensic_findings.md
```

Create plot artifacts for the report:

```powershell
python src\main.py --input data\sample_netflow.csv --output docs\forensic_findings.md --plots docs/plots
```

Launch the SIEM-style dashboard:

```powershell
streamlit run src\dashboard.py
```

Open the forensic notebook:

```powershell
jupyter notebook notebooks/Network_Forensics_Analysis.ipynb
```

## Notes

- The included sample data and code are designed for NetFlow-style CSV exports from CIC-IDS-2017 or similar flow telemetry sources.
- This repository is structured for easy extension into enterprise SIEM workflows, cloud telemetry, and incident response automation.

## Next Steps

Potential portfolio enhancements include:
- expanded dataset support and additional labeled traces
- integration with enterprise SIEM and alerting platforms
- richer anomaly scoring and incident classification
- deployment-ready dashboard packaging
