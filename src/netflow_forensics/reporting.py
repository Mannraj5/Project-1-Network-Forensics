from pathlib import Path


def save_findings_report(findings: dict, output_path: Path) -> None:
    output_path = Path(output_path)
    lines = [
        '# Forensic Findings',
        '',
        '## Executive Summary',
        '',
        'This report summarizes flow-level forensic findings from the provided NetFlow dataset.',
        '',
        '## Dataset Summary',
        '',
    ]

    summary = findings.get('summary', {})
    lines.append(f"- Total flows: {summary.get('total_flows', 0)}")
    lines.append(f"- Unique source IPs: {summary.get('unique_source_ips', 0)}")
    lines.append(f"- Unique destination IPs: {summary.get('unique_destination_ips', 0)}")
    lines.append('')

    lines.append('### Protocol distribution')
    for protocol, count in summary.get('protocols', {}).items():
        lines.append(f'- {protocol}: {count}')
    lines.append('')

    lines.append('### Label distribution')
    for label, count in summary.get('label_distribution', {}).items():
        lines.append(f'- {label}: {count}')
    lines.append('')

    lines.append('## Suspicious Ports')
    lines.append('')
    for port in findings.get('suspicious_ports', []):
        lines.append(f"- Port {port.get('destination_port')}: {port.get('count')} flows")
    lines.append('')

    lines.append('## High-Volume Flows')
    lines.append('')
    for flow in findings.get('high_volume_flows', []):
        port = flow.get('destination_port', 'N/A')
        bytes_total = flow.get('total_bytes', 'N/A')
        packets = flow.get('total_packets', 'N/A')
        lines.append(f'- Destination port {port}, bytes={bytes_total}, packets={packets}')
    lines.append('')

    lines.append('## Anomaly Detection Summary')
    anomaly_summary = findings.get('anomaly_summary', {})
    lines.append(f"- Detected anomalies: {anomaly_summary.get('anomaly_count', 0)}")
    lines.append(f"- Anomaly ratio: {anomaly_summary.get('anomaly_ratio', 0.0):.2%}")
    lines.append(f"- Features used: {', '.join(anomaly_summary.get('features', []))}")
    lines.append('')

    lines.append('## Top Anomalous Flows')
    lines.append('')
    for flow in findings.get('anomaly_flows', []):
        score = flow.get('anomaly_score', 'N/A')
        flag = flow.get('anomaly_flag', 'N/A')
        port = flow.get('destination_port', 'N/A')
        lines.append(f'- Port {port}, anomaly_score={score}, anomaly_flag={flag}')
    lines.append('')

    lines.append('## Port Scanning Candidates')
    for scanner in findings.get('port_scanners', []):
        lines.append(f"- Source {scanner.get('source_ip')}: {scanner.get('unique_destination_ports', 0)} unique destination ports")
    lines.append('')

    lines.append('## Outbound Byte Spikes')
    for spike in findings.get('outbound_spikes', []):
        timestamp = spike.get('timestamp')
        bytes_value = spike.get('bytes')
        lines.append(f'- {timestamp}: {bytes_value}')
    lines.append('')

    if 'classification' in findings:
        classification = findings['classification']
        lines.append('## Supervised Classification Summary')
        lines.append(f"- Accuracy: {classification.get('accuracy', 0.0):.2%}")
        lines.append(f"- F1 score: {classification.get('f1_score', 0.0):.2f}")
        lines.append(f"- Features used: {', '.join(classification.get('features', []))}")
        lines.append('')
        if classification.get('report'):
            lines.append('### Classification Report')
            for label, metrics in classification['report'].items():
                if isinstance(metrics, dict):
                    lines.append(f"- {label}: precision={metrics.get('precision', 0.0):.2f}, recall={metrics.get('recall', 0.0):.2f}, f1-score={metrics.get('f1-score', 0.0):.2f}")
            lines.append('')

    lines.append('## Correlation Summary')
    correlation = findings.get('correlation', {})
    for feature, values in correlation.items():
        row = ', '.join(f'{k}={v:.2f}' for k, v in values.items())
        lines.append(f'- {feature}: {row}')
    lines.append('')

    output_path.write_text('\n'.join(lines), encoding='utf-8')
