# Quick Start Guide

## 5-Minute Setup

### 1. Clone & Environment
```bash
git clone https://github.com/Mannraj5/Project-1-Network-Forensics.git
cd Project-1-Network-Forensics
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\Activate    # Windows
pip install -r requirements.txt
```

### 2. Validate Installation
```bash
pytest -q
```
Expected output: `3 passed` (or similar)

### 3. Run the Pipeline
```bash
python src/main.py --input data/example_flows.csv --output results/
```

This will:
- Load NetFlow data
- Engineer forensic features  
- Run anomaly detection
- Generate markdown report
- Save visualizations

**Output**: `results/investigation_report.md` with findings and charts

---

## Using the Dashboard

Interactive real-time analysis for incident response:

```bash
streamlit run src/dashboard.py
```

Opens browser to `http://localhost:8501`

**Features**:
- Filter by IP, port, protocol, time range
- Sort by anomaly score or volume
- Drill into individual flow details
- Export suspicious flows to CSV
- View real-time trends

---

## Using the Notebook

Guided exploratory analysis with inline commentary:

```bash
jupyter notebook notebooks/Network_Forensics_Analysis.ipynb
```

Walk through:
1. Data loading and schema validation
2. Forensic feature engineering
3. Statistical analysis and visualization
4. Anomaly detection results
5. Supervised classification (if labels available)
6. Executive summary generation

---

## Common Workflows

### Investigate Suspicious Outbound Traffic
```python
from netflow_forensics import data_loader, preprocessing, analysis

flows = data_loader.load_netflow_csv('data/flows.csv')
flows = preprocessing.engineer_forensic_features(flows)

# Filter to external destinations with high volume
external = flows[~flows['is_internal_dst']]
high_volume = external[external['bytes'] > external['bytes'].quantile(0.95)]

# Sort by byte rate (intensity)
high_volume_sorted = high_volume.sort_values('byte_rate', ascending=False)
print(high_volume_sorted[['src_ip', 'dst_ip', 'dst_port', 'bytes', 'byte_rate']].head(20))
```

### Detect Port Scanning Activity
```python
# Find flows with diverse destination ports from same source
scanner_candidates = flows.groupby('src_ip')['dst_port'].nunique().sort_values(ascending=False)
print("Top port scanners (unique dest ports):")
print(scanner_candidates.head(10))

# Investigate top candidate
top_scanner_ip = scanner_candidates.index[0]
scanner_flows = flows[flows['src_ip'] == top_scanner_ip]
print(f"\n{top_scanner_ip} scanned {scanner_flows['dst_port'].nunique()} unique ports")
print(scanner_flows[['dst_ip', 'dst_port', 'protocol']].drop_duplicates().head(20))
```

### Identify Data Exfiltration
```python
# High byte rate from internal to external
exfil_candidates = flows[
    (flows['is_internal_src']) & 
    (~flows['is_internal_dst']) &
    (flows['byte_rate'] > flows['byte_rate'].quantile(0.95))
].sort_values('bytes', ascending=False)

print(f"Found {len(exfil_candidates)} potential exfiltration flows")
print(exfil_candidates[['src_ip', 'dst_ip', 'dst_port', 'bytes', 'duration']].head(10))
```

### Find Anomalies with ML
```python
from netflow_forensics import ml, visualization
from sklearn.preprocessing import StandardScaler

# Train model
features = ['byte_rate', 'packet_rate', 'duration', 'bytes', 'packets']
X = flows[features].fillna(0)
X_scaled = StandardScaler().fit_transform(X)

model = ml.fit_isolation_forest(flows, features, contamination=0.05)
scores = ml.score_anomalies(flows, model, features)
flows['anomaly_score'] = scores

# Visualize
visualization.plot_anomaly_scores(scores, output_file='anomalies.png')

# Inspect top anomalies
anomalies = flows[flows['anomaly_score'] == -1].sort_values('bytes', ascending=False)
print(f"Found {len(anomalies)} anomalies")
print(anomalies[['src_ip', 'dst_ip', 'dst_port', 'bytes', 'packet_rate']].head(10))
```

---

## Data Format

Expected CSV columns:
```
timestamp,src_ip,dst_ip,src_port,dst_port,protocol,packets,bytes,duration,label
2024-06-01 10:30:45,10.0.1.100,8.8.8.8,50123,53,UDP,5,450,0.5,benign
2024-06-01 10:30:46,10.0.1.101,192.0.2.1,60000,3389,TCP,1000,500000,30.2,malicious
...
```

**Required fields**:
- `timestamp`: ISO format datetime
- `src_ip`, `dst_ip`: IPv4 addresses
- `src_port`, `dst_port`: Integer port numbers
- `protocol`: UDP, TCP, ICMP, etc.
- `packets`, `bytes`: Integer counts
- `duration`: Float seconds

**Optional fields**:
- `label`: benign/malicious (for supervised learning)

---

## Troubleshooting

**Q: "ModuleNotFoundError: No module named 'pandas'"**  
A: Ensure virtual environment is activated and requirements installed:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

**Q: "SchemaError: Missing required columns"**  
A: Check CSV column names match expected format. Run:
```python
import pandas as pd
df = pd.read_csv('your_file.csv')
print(df.columns.tolist())
```

**Q: Dashboard won't start with Streamlit**  
A: Streamlit needs Python >=3.8. Check version:
```bash
python --version
pip install --upgrade streamlit
```

**Q: Tests fail with "FileNotFoundError"**  
A: Ensure you're running from project root:
```bash
cd Project-1-Network-Forensics
pytest -q
```

**Q: Anomaly detection too sensitive/insensitive**  
A: Adjust `contamination` parameter:
```python
# More sensitive (flag more as anomalies):
model = ml.fit_isolation_forest(flows, features, contamination=0.1)

# Less sensitive (fewer false positives):
model = ml.fit_isolation_forest(flows, features, contamination=0.01)
```

---

## Next Steps

- Read [ARCHITECTURE.md](./ARCHITECTURE.md) for deep technical dive
- Review [API_REFERENCE.md](./API_REFERENCE.md) for all available functions
- Check [Project_Report.md](./Project_Report.md) for research findings
- Explore [Network_Forensics_Analysis.ipynb](../notebooks/Network_Forensics_Analysis.ipynb) for interactive walkthrough

## Support & Contribution

For issues, questions, or contributions:
- Open an issue on GitHub
- Submit pull requests with improvements
- Extend with custom analysis modules following the modular design
