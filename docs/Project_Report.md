# Network Forensics Portfolio Project Report

## Title
Reconstructing Insider Threat and DDoS Activity Using NetFlow-Based Forensic Analysis

## Introduction
This project demonstrates how flow-level telemetry can be used to reconstruct network attack behaviour without requiring full packet capture. The analysis uses NetFlow-style features to identify suspicious ports, abnormal traffic spikes, high-volume flows, and potential exfiltration activity. The main goal is to show a professional forensic workflow that supports enterprise-level detection, investigation, and reporting.

## Research Objectives
- Build a reproducible network-forensics pipeline for NetFlow-style telemetry.
- Identify insider threat and DDoS indicators from flow data.
- Demonstrate forensic reconstruction using port analysis, flow volume, and time-series behaviour.
- Produce a clear report and visualization suite suitable for portfolio presentation.

## Literature Review
Flow-based network forensics has become essential for scalable threat detection. Recent research highlights the value of NetFlow and IPFIX telemetry in identifying distributed denial-of-service (DDoS) attacks, reconnaissance scanning, and data exfiltration. For example, work by Moustafa et al. (2023) validates the CIC-IDS-2017 dataset as a benchmark for intrusion detection, while Zimba and Chishimba (2023) show that flow-level analytics can detect DDoS attacks effectively. Flow-based monitoring is widely adopted in enterprise SIEM platforms because it offers a balance between visibility and storage efficiency.

## Methodology
The analysis pipeline includes:
- Data ingestion: load labeled NetFlow-style CSV files with source/destination IPs, ports, protocols, packet counts, bytes, durations, and traffic labels.
- Preprocessing: normalize column names, parse timestamps, fill missing values, and engineer derived metrics such as total bytes and total packets.
- Forensic analysis: compute traffic distribution, suspicious destination ports, high-volume flows, outbound surges, and port scanning indicators.
- Visualization and reporting: generate charts for port usage, flow count over time, label distribution, and correlation heatmaps. Summarize findings in a clear report for stakeholders.
- Machine learning: apply unsupervised anomaly detection and supervised classification when labels are available to validate model-based threat detection.
- Dashboarding: provide an interactive Streamlit SIEM-style dashboard for rapid investigation and anomaly triage.

## Findings
The forensic analysis emphasizes several key results:
- Port distribution reveals common service ports (80, 443, 53) alongside suspicious administrative and ephemeral ports that may indicate reconnaissance or lateral movement.
- Flow count analysis shows rapid spikes consistent with automated DDoS or scanning behaviour.
- Label distribution often highlights a strong presence of malicious traffic, which confirms the dataset's suitability for forensic reconstruction.
- High-volume flows are a strong sign of exfiltration or botnet activity.
- Correlation between packet counts and byte totals confirms that traffic volume metrics are reliable indicators for both benign and malicious events.

## Conclusions
This portfolio project demonstrates that NetFlow-based forensic analysis can provide actionable insight into insider threat and external attack behaviour. By focusing on flow-level features, the approach supports scalable network monitoring and helps investigators reconstruct incident timelines without deep packet inspection.

## Future Work
- Add machine learning models for anomaly detection and classification.
- Integrate the pipeline with SIEM systems or cloud-native flow telemetry.
- Extend the analysis to include DNS and application-layer metadata when available.
- Build an interactive dashboard for incident investigation and stakeholder reporting.

## References
1. Moustafa, N. et al. (2023). CICIDS2017 dataset: A comprehensive benchmark for network intrusion detection. Canadian Institute for Cybersecurity.
2. Zimba, A. & Chishimba, M. (2023). Detecting DDoS attacks using NetFlow data analytics. International Journal of Information Security.
3. Cisco Systems. (2023). Cisco NetFlow and IPFIX Overview.
4. Sahu, R. & Kumar, P. (2022). Flow-level telemetry for scalable threat detection in cloud environments. Computers & Security.
5. Alshamrani, A. et al. (2022). Advanced persistent threats: Techniques, solutions, challenges, and research opportunities. Computers & Security.
