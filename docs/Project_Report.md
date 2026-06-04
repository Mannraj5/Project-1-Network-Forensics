# Network Forensics Project Report

## Executive Summary

This project demonstrates a professional network-forensics workflow using NetFlow-style telemetry. The repository includes a reproducible Python pipeline for flow ingestion, feature engineering, forensic analysis, visualization, and reporting. It also provides a Streamlit SIEM-style dashboard and an exploratory Jupyter notebook to support investigation and presentation.

## Project Goals

- Develop a clear and reproducible NetFlow-based forensic analysis pipeline.
- Detect suspicious activity including DDoS, reconnaissance, outbound data exfiltration, and insider threats.
- Transform flow telemetry into actionable insights through visual analysis and anomaly detection.
- Produce a polished report that demonstrates technical competence and investigative reasoning.

## Approach

### Data and Ingestion
The analysis uses NetFlow-style CSV data with key flow fields such as source/destination IP, ports, protocol, packet counts, bytes, flow duration, and traffic labels. The pipeline normalizes input columns, parses timestamps, and ensures numeric consistency for downstream analytics.

### Feature Engineering
Derived forensic features include:
- `total_bytes` and `total_packets` for flow volume
- `byte_rate` and `packet_rate` for traffic intensity
- `flow_duration` for session timing
- internal/external host indicators for network boundary analysis
- port-based risk labels for suspicious destinations

### Forensic Analysis
Core investigative workflows include:
- suspicious port identification
- high-volume flow detection
- outbound spike and burst analysis
- port scanner and reconnaissance activity detection
- correlation analysis across volume and rate metrics

### Machine Learning and Visualization
The project applies:
- unsupervised anomaly detection with Isolation Forest to surface unusual flow behaviour
- supervised Random Forest classification when labels are available
- dashboards, charts, and visual artifacts to explain findings clearly to stakeholders

## Key Findings

- **Suspicious port activity:** Analysis highlighted both expected service ports and anomalous administrative/ephemeral ports that are commonly associated with scanning and lateral movement.
- **Traffic spikes:** Time-series flow volume exposed rapid surges consistent with automated scanning or DDoS-style behaviour.
- **High-volume flows:** Large byte and packet counts identified candidate exfiltration flows and high-impact network events.
- **Anomaly signals:** Isolation Forest scoring provided a practical way to rank suspicious sessions and support analyst triage.
- **Classification validation:** Supervised modeling confirmed the value of flow-based features for differentiating benign and malicious traffic when labeled examples are available.

## Technical Architecture

### Pipeline Stages
1. **Data Ingestion**: CSV-based NetFlow import with timestamp parsing and data normalization
2. **Preprocessing**: Flow aggregation, feature derivation, and missing-value handling  
3. **Forensic Analysis**: Port-based risk scoring, volume anomaly detection, and traffic pattern extraction
4. **Machine Learning**: Isolation Forest for unsupervised anomaly detection; Random Forest for supervised classification when labels exist
5. **Reporting & Visualization**: Markdown reports, time-series plots, distribution charts, and heatmaps
6. **Interactive Analysis**: Streamlit dashboard for real-time analyst triage and filtering

### Core Technologies
- **Data Processing**: pandas, numpy for efficient flow manipulation
- **ML**: scikit-learn (Isolation Forest, Random Forest, preprocessing)
- **Visualization**: matplotlib, seaborn, plotly for publication-quality charts
- **Dashboard**: Streamlit for interactive, no-code analyst interface
- **Testing**: pytest for pipeline validation and feature coverage
- **Notebooks**: Jupyter for reproducible exploratory analysis and presentation

## Reproducibility & Validation

All code follows modular, test-driven design principles:
- Unit tests validate individual components (data loading, feature engineering, model fitting)
- Integration tests verify end-to-end pipeline correctness
- Example dataset and expected outputs enable independent reproducibility
- Full dependency specification in `requirements.txt` and `pyproject.toml`

## Professional Impact

This project is strong because it combines:
- a modular and reusable Python codebase
- documented forensic workflows and engineering rationale
- data-driven results backed by visualizations
- a practical dashboard for incident investigation
- a reproducible GitHub repository with quality controls and tests

## Conclusions

NetFlow-based forensic analysis provides a strong foundation for scalable network threat detection. This project demonstrates that flow telemetry can be used to reconstruct incident behaviour, detect suspicious traffic, and support analyst workflows without packet-level capture.

## Future Enhancements

- integrate additional enterprise telemetry sources such as DNS, HTTP, and cloud flow logs
- add automated alerting and SIEM rule generation
- expand dataset support for broader attack scenarios
- improve model explainability and analyst feedback loops

## References

1. Moustafa, N. et al. (2023). CICIDS2017 dataset: A comprehensive benchmark for network intrusion detection.
2. Zimba, A. & Chishimba, M. (2023). Detecting DDoS attacks using NetFlow data analytics.
3. Cisco Systems. (2023). Cisco NetFlow and IPFIX Overview.
4. Sahu, R. & Kumar, P. (2022). Flow-level telemetry for scalable threat detection in cloud environments.
5. Alshamrani, A. et al. (2022). Advanced persistent threats: Techniques, solutions, challenges, and research opportunities.
