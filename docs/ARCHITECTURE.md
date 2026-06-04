# System Architecture

## Overview
The Network Forensics Analysis system is a modular Python pipeline for ingesting NetFlow-style telemetry, engineering forensic features, detecting anomalies, and providing both programmatic and interactive analysis interfaces.

## Component Breakdown

### Data Layer (`src/netflow_forensics/data_loader.py`)
**Responsibility**: Ingest and normalize NetFlow CSV data  
**Key Functions**:
- `load_netflow_csv()` - Read CSV with proper timestamp parsing and type coercion
- `validate_schema()` - Ensure required flow fields are present
- `normalize_columns()` - Standardize field names and units across data sources

**Output**: Pandas DataFrame with validated flow records

### Preprocessing Layer (`src/netflow_forensics/preprocessing.py`)
**Responsibility**: Transform raw flows into forensic-ready features  
**Key Operations**:
- Timestamp conversion and aggregation windows
- Missing-value imputation using domain-appropriate defaults
- Host classification (internal vs. external) based on IP ranges
- Protocol and port-based risk categorization
- Byte/packet rate derivation for traffic intensity analysis

**Output**: Enhanced DataFrame with derived forensic features

### Analysis Engine (`src/netflow_forensics/analysis.py`)
**Responsibility**: Conduct forensic investigation workflows  
**Core Investigations**:
- Suspicious port identification (scanning, reconnaissance)
- High-volume flow ranking (exfiltration candidates)
- Time-series spike detection (DDoS, burst patterns)
- Port scanner fingerprint matching
- Correlation analysis (multi-dimensional risk scoring)

**Output**: Ranked lists and annotations of suspicious flows

### Machine Learning Layer (`src/netflow_forensics/ml.py`)
**Responsibility**: Apply unsupervised and supervised anomaly detection  
**Methods**:
- **Isolation Forest**: Unsupervised anomaly scoring without labels
- **Local Outlier Factor**: Density-based anomaly detection
- **Random Forest Classification**: Supervised binary (benign/malicious) classification when training labels available
- Feature importance ranking and threshold optimization

**Output**: Anomaly scores, classification probabilities, and feature importance vectors

### Visualization (`src/netflow_forensics/visualization.py`)
**Responsibility**: Generate publication-quality charts and diagnostics  
**Chart Types**:
- Time-series flow volume and rate plots
- Distribution histograms (bytes, packets, duration)
- Port frequency heatmaps and scatter plots
- ROC curves and confusion matrices for model evaluation
- Anomaly score distributions with threshold indicators

**Output**: PNG/PDF chart files and embedded Jupyter artifacts

### Reporting (`src/netflow_forensics/reporting.py`)
**Responsibility**: Generate structured markdown investigation reports  
**Report Sections**:
- Executive summary with key findings
- Methodology and data provenance
- Detailed analysis results with tables and charts
- Anomaly rankings with analyst recommendations
- Appendices with supporting metrics

**Output**: Markdown report suitable for print, PDF export, and presentation

---

## Interfaces

### CLI Interface (`src/main.py`)
Entry point for running the full pipeline programmatically:
```python
python src/main.py --input data/flows.csv --output results/ --model isolation_forest
```

### Dashboard (`src/dashboard.py`)
Interactive Streamlit web application for real-time filtering, sorting, and drill-down analysis:
```bash
streamlit run src/dashboard.py
```

Features:
- Filter flows by port, protocol, IP range, and time window
- Sort by anomaly score or forensic metrics
- Drill into individual flow records
- Export subsets for further investigation
- Visual correlation of multiple metrics

### Jupyter Notebook (`notebooks/Network_Forensics_Analysis.ipynb`)
Interactive exploratory analysis and presentation environment:
- Step-by-step walkthrough of data loading → analysis → visualization
- Inline markdown explanations for stakeholder communication
- Reproducible code cells with documented parameters
- Output-rich analysis with embedded charts and tables

---

## Data Flow

```
Raw NetFlow CSV
      ↓
  [Data Loader] → validate schema, parse timestamps
      ↓
  [Preprocessing] → engineer features, categorize hosts/ports
      ↓
  [Analysis Engine] → forensic scoring, spike detection, correlation
      ↓
  [ML Layer] → anomaly detection, classification
      ↓
  ├─→ [Visualization] → charts and diagnostics
  ├─→ [Reporting] → markdown investigation report
  └─→ [Dashboard] → interactive analyst interface
```

---

## Testing Strategy

### Unit Tests (`tests/test_pipeline.py`)
- Data loader correctness (schema validation, type handling)
- Preprocessing feature derivation (byte rates, host classification)
- Analysis accuracy (port identification, spike detection)
- ML model fit and prediction sanity checks
- Report generation completeness

### Integration Tests
- Full pipeline execution with example data
- End-to-end dashboard functionality
- Report generation from raw CSV to markdown
- Cross-component data contract validation

### Validation
- Example dataset with known ground-truth anomalies
- Baseline performance metrics (precision, recall for anomaly detection)
- Regression testing to prevent feature drift

---

## Deployment Considerations

### Dependencies
- **Python 3.9+** for type hints and modern async patterns
- **pandas** ≥1.3 for efficient data manipulation
- **scikit-learn** ≥1.0 for ML algorithms
- **streamlit** ≥1.10 for dashboard
- **matplotlib, seaborn, plotly** for visualization

### Environment Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\Activate   # Windows
pip install -r requirements.txt
```

### Performance Tuning
- Use chunked CSV loading for datasets >1GB
- Apply preprocessing in parallel using multiprocessing
- Cache ML models post-training for real-time dashboard
- Prune low-variance features to reduce model complexity

---

## Future Enhancements

- Real-time streaming ingestion (Kafka, Splunk forwarders)
- Graph-based attack pattern detection (network propagation)
- Automated report scheduling and alerting
- Integration with ticketing systems (Jira, ServiceNow)
- YARA-style rule engine for forensic signatures
- Multi-tenant dashboard with RBAC
