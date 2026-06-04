# Network Forensics Portfolio Case Study

## Project Summary
This portfolio project delivers a professional-grade NetFlow analysis toolkit for enterprise network forensics. It combines data engineering, flow-level feature extraction, unsupervised anomaly detection, supervised classification, visual reporting, and an interactive analyst dashboard.

## What Makes This Project Strong
- Uses flow telemetry instead of full packet capture, matching modern scalable SIEM and network detection strategies.
- Engineers derived forensic features such as bytes-per-packet, byte rate, packet rate, and internal/external host indicators.
- Includes both anomaly detection and supervised classification to validate suspicious flow patterns.
- Provides a polished Streamlit dashboard for rapid incident investigation.
- Ships with notebooks, test coverage, and runnable pipelines for reproducible results.

## Key Deliverables
- `src/main.py` — end-to-end forensic pipeline
- `src/dashboard.py` — SIEM-style analyst dashboard
- `src/netflow_forensics/` — modular forensic library
- `notebooks/Network_Forensics_Analysis.ipynb` — exploratory workflow and model evaluation
- `docs/forensic_findings.md` — generated findings report with attack summary
- `tests/` — validation for ingestion, preprocessing, anomaly detection, and classification

## Using This Project in a Portfolio
1. Show the repository structure and explain the modular architecture.
2. Highlight the data preprocessing and feature engineering steps.
3. Demonstrate the anomaly detection and supervised classification results.
4. Run the dashboard and show interactive results for suspicious hosts and flows.
5. Share the generated report and plots as evidence of a repeatable investigative workflow.
