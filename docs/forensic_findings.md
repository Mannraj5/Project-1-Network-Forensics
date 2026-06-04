# Forensic Findings

## Executive Summary

This report summarizes flow-level forensic findings from the provided NetFlow dataset.

## Dataset Summary

- Total flows: 12
- Unique source IPs: 7
- Unique destination IPs: 9

### Protocol distribution
- TCP: 11
- UDP: 1

### Label distribution
- benign: 6
- ddos: 6

## Suspicious Ports

- Port 80: 3 flows
- Port 443: 1 flows
- Port 53: 1 flows
- Port 52784: 1 flows
- Port 445: 1 flows
- Port 22: 1 flows
- Port 139: 1 flows
- Port 8080: 1 flows
- Port 49666: 1 flows
- Port 49671: 1 flows

## High-Volume Flows

- Destination port 80, bytes=1887436, packets=1800
- Destination port 8080, bytes=5930, packets=70
- Destination port 80, bytes=4820, packets=55
- Destination port 52784, bytes=3336, packets=28
- Destination port 443, bytes=2436, packets=32
- Destination port 80, bytes=1784, packets=20
- Destination port 445, bytes=510, packets=6
- Destination port 53, bytes=500, packets=10
- Destination port 139, bytes=360, packets=4
- Destination port 22, bytes=270, packets=3

## Anomaly Detection Summary
- Detected anomalies: 2
- Anomaly ratio: 16.67%
- Features used: total_bytes, total_packets, flow_duration, total_fwd_packets, total_bwd_packets

## Top Anomalous Flows

- Port 80, anomaly_score=-0.2590527566093985, anomaly_flag=True
- Port 52784, anomaly_score=-0.003074477685279575, anomaly_flag=True

## Correlation Summary
- total_bytes: total_bytes=1.00, total_packets=1.00, flow_duration=0.46
- total_packets: total_bytes=1.00, total_packets=1.00, flow_duration=0.48
- flow_duration: total_bytes=0.46, total_packets=0.48, flow_duration=1.00
