# API Reference

## Overview
This document provides complete API documentation for the Network Forensics Analysis library.

## Core Modules

### `netflow_forensics.data_loader`
Module for ingesting and validating NetFlow data.

#### Functions

**`load_netflow_csv(filepath: str, **kwargs) -> pd.DataFrame`**
- Load a CSV file containing NetFlow flow records
- Automatically parse timestamp columns and convert numeric types
- Validate schema against required flow fields
- **Parameters**:
  - `filepath`: Path to CSV file
  - `timestamp_col`: Column name for flow timestamps (default: 'timestamp')
  - `parse_dates`: List of date columns (auto-detected if not specified)
- **Returns**: Validated DataFrame with flow records
- **Raises**: `ValueError` if required columns missing

**`validate_schema(df: pd.DataFrame) -> None`**
- Verify that DataFrame contains all required NetFlow fields
- Raise informative error if schema incomplete
- **Required Fields**: src_ip, dst_ip, src_port, dst_port, protocol, packets, bytes, duration
- **Raises**: `SchemaError` if validation fails

**`normalize_columns(df: pd.DataFrame) -> pd.DataFrame`**
- Standardize column names to lowercase, underscores
- Convert numeric columns to appropriate dtypes
- Drop duplicate rows
- **Returns**: Normalized DataFrame

---

### `netflow_forensics.preprocessing`
Feature engineering and data transformation.

#### Functions

**`engineer_forensic_features(df: pd.DataFrame, internal_cidrs: List[str] = None) -> pd.DataFrame`**
- Derive forensic features from raw flow records
- Add byte rate, packet rate, internal/external indicators
- **Parameters**:
  - `df`: Input flow DataFrame
  - `internal_cidrs`: List of internal IP ranges (e.g., ['10.0.0.0/8', '172.16.0.0/12'])
- **Returns**: DataFrame with additional forensic feature columns
- **New Columns Added**: 
  - `byte_rate`: bytes/second
  - `packet_rate`: packets/second
  - `is_internal_src`: True if source IP in internal range
  - `is_internal_dst`: True if dest IP in internal range
  - `port_risk_score`: 0-10 based on destination port

**`categorize_ports(df: pd.DataFrame) -> pd.DataFrame`**
- Add port category and risk labels
- **Port Categories**: 
  - 'well_known' (0-1023)
  - 'registered' (1024-49151)
  - 'dynamic' (49152-65535)
  - 'suspicious' (admin ports, P2P, VPN)
- **Returns**: DataFrame with port_category column

**`aggregate_flows(df: pd.DataFrame, time_window: str = '1H', agg_func: str = 'sum') -> pd.DataFrame`**
- Aggregate flows into time windows
- **Parameters**:
  - `df`: Input DataFrame with timestamp index
  - `time_window`: Pandas frequency string ('1H', '1D', '5T', etc.)
  - `agg_func`: Aggregation function ('sum', 'mean', 'max', 'count')
- **Returns**: Time-indexed aggregated flows

**`handle_missing_values(df: pd.DataFrame, strategy: str = 'drop') -> pd.DataFrame`**
- Handle NaN/null values
- **Strategies**: 'drop', 'forward_fill', 'mean_impute'
- **Returns**: DataFrame with missing values handled

---

### `netflow_forensics.analysis`
Forensic investigation workflows.

#### Functions

**`identify_suspicious_ports(df: pd.DataFrame, port_risk_threshold: float = 7.0) -> pd.DataFrame`**
- Find flows to high-risk destination ports
- **Risk Scoring**: 0-10 scale based on port category and known exploits
- **Parameters**:
  - `df`: Input flow DataFrame
  - `port_risk_threshold`: Minimum risk score to flag
- **Returns**: Filtered DataFrame of suspicious port flows, sorted by risk

**`detect_high_volume_flows(df: pd.DataFrame, percentile: float = 95.0) -> pd.DataFrame`**
- Identify flows in top percentile by bytes or packets
- **Parameters**:
  - `df`: Input DataFrame
  - `percentile`: Upper percentile threshold (default: 95th)
- **Returns**: High-volume flows sorted by bytes descending

**`detect_traffic_spikes(df: pd.DataFrame, window: str = '1H', threshold_sigma: float = 2.0) -> pd.DataFrame`**
- Detect anomalous traffic volume changes
- Uses time-series windowing and Z-score thresholding
- **Parameters**:
  - `df`: Time-indexed flow DataFrame
  - `window`: Aggregation window
  - `threshold_sigma`: Z-score threshold (>N indicates anomaly)
- **Returns**: DataFrame with spike_detected boolean column

**`correlate_metrics(df: pd.DataFrame, metrics: List[str]) -> pd.DataFrame`**
- Calculate multi-dimensional risk scores
- Combines byte rate, packet rate, port risk, volume metrics
- **Parameters**:
  - `df`: Input DataFrame
  - `metrics`: Feature columns to correlate
- **Returns**: DataFrame with correlation_score column (0-1)

---

### `netflow_forensics.ml`
Machine learning anomaly detection and classification.

#### Functions

**`fit_isolation_forest(df: pd.DataFrame, features: List[str], contamination: float = 0.1, **kwargs) -> IsolationForest`**
- Train unsupervised anomaly detector
- **Parameters**:
  - `df`: Input DataFrame with features
  - `features`: List of column names to use
  - `contamination`: Expected proportion of anomalies (0-1)
- **Returns**: Fitted scikit-learn IsolationForest model
- **Output**: Model object can be pickled for reuse

**`score_anomalies(df: pd.DataFrame, model: IsolationForest, features: List[str]) -> np.ndarray`**
- Generate anomaly scores for flows
- **Parameters**:
  - `df`: Input DataFrame
  - `model`: Fitted model
  - `features`: Feature columns matching training
- **Returns**: Array of anomaly scores (-1 = anomaly, 1 = normal)

**`fit_random_forest(df: pd.DataFrame, features: List[str], target: str, test_size: float = 0.2, **kwargs) -> RandomForestClassifier`**
- Train supervised benign/malicious classifier
- **Parameters**:
  - `df`: Labeled training DataFrame
  - `features`: Feature column names
  - `target`: Target column name (0/1, benign/malicious)
  - `test_size`: Train/test split fraction
- **Returns**: Fitted RandomForestClassifier model
- **Output**: Includes cross-validation scores and ROC metrics

**`predict_classes(df: pd.DataFrame, model: RandomForestClassifier, features: List[str]) -> np.ndarray`**
- Generate classification probabilities
- **Parameters**:
  - `df`: Input DataFrame
  - `model`: Fitted model
  - `features`: Feature columns
- **Returns**: Array of class probabilities (shape: N x 2)

**`feature_importance(model: RandomForestClassifier) -> pd.Series`**
- Extract and rank feature importances
- **Returns**: Series with feature names and importance scores, sorted descending

---

### `netflow_forensics.visualization`
Charting and diagnostic plotting.

#### Functions

**`plot_flow_volume(df: pd.DataFrame, time_col: str = 'timestamp', output_file: str = None) -> None`**
- Time-series plot of total flow bytes/packets
- **Parameters**:
  - `df`: Time-indexed flow DataFrame
  - `time_col`: Timestamp column name
  - `output_file`: Optional PNG file to save
- **Output**: Matplotlib figure (displays or saves)

**`plot_port_distribution(df: pd.DataFrame, top_n: int = 20, output_file: str = None) -> None`**
- Bar chart of most common destination ports
- **Parameters**:
  - `df`: Flow DataFrame
  - `top_n`: Number of top ports to display
  - `output_file`: Optional PNG file
- **Output**: Matplotlib figure

**`plot_anomaly_scores(scores: np.ndarray, threshold: float = -0.5, output_file: str = None) -> None`**
- Histogram of anomaly scores with threshold indicator
- **Parameters**:
  - `scores`: Array of anomaly scores from model
  - `threshold`: Anomaly decision boundary
  - `output_file`: Optional PNG file
- **Output**: Matplotlib figure

**`plot_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, labels: List[str] = None, output_file: str = None) -> None`**
- Classification confusion matrix heatmap
- **Parameters**:
  - `y_true`: Ground-truth labels
  - `y_pred`: Predicted labels
  - `labels`: Optional class names
  - `output_file`: Optional PNG file
- **Output**: Matplotlib figure

**`plot_roc_curve(y_true: np.ndarray, y_score: np.ndarray, output_file: str = None) -> None`**
- ROC curve for binary classification evaluation
- **Parameters**:
  - `y_true`: Ground-truth binary labels
  - `y_score`: Prediction probabilities or scores
  - `output_file`: Optional PNG file
- **Output**: Matplotlib figure with AUC score annotation

---

### `netflow_forensics.reporting`
Report generation and export.

#### Functions

**`generate_markdown_report(df: pd.DataFrame, suspicious_flows: pd.DataFrame, findings_dict: Dict, output_file: str = 'report.md') -> None`**
- Generate comprehensive markdown investigation report
- **Parameters**:
  - `df`: Full flow DataFrame
  - `suspicious_flows`: Filtered/ranked suspicious flows
  - `findings_dict`: Dict with 'high_volume_flows', 'suspicious_ports', 'anomalies', etc.
  - `output_file`: Output markdown filename
- **Report Contents**: 
  - Executive summary
  - Methodology
  - Findings tables with top anomalies
  - Appendix with flow details and metrics
- **Output**: Markdown file (can be converted to PDF, HTML)

**`export_csv(df: pd.DataFrame, output_file: str) -> None`**
- Export flows to CSV with full features
- **Parameters**:
  - `df`: Flow DataFrame
  - `output_file`: Output CSV filename
- **Output**: CSV file

**`export_json(df: pd.DataFrame, output_file: str) -> None`**
- Export flows to JSON Lines format
- **Parameters**:
  - `df`: Flow DataFrame
  - `output_file`: Output JSON Lines filename
- **Output**: JSONL file (one flow per line)

---

## Example Usage

```python
from netflow_forensics import data_loader, preprocessing, analysis, ml, reporting

# 1. Load and validate data
flows = data_loader.load_netflow_csv('data/flows.csv')
data_loader.validate_schema(flows)

# 2. Engineer features
flows = preprocessing.engineer_forensic_features(
    flows, 
    internal_cidrs=['10.0.0.0/8', '172.16.0.0/12']
)

# 3. Run analysis
suspicious_ports = analysis.identify_suspicious_ports(flows, threshold=7.0)
high_volume = analysis.detect_high_volume_flows(flows, percentile=95)

# 4. ML anomaly detection
from sklearn.preprocessing import StandardScaler
features = ['byte_rate', 'packet_rate', 'duration']
X_scaled = StandardScaler().fit_transform(flows[features])
model = ml.fit_isolation_forest(flows, features, contamination=0.05)
anomaly_scores = ml.score_anomalies(flows, model, features)

# 5. Generate report
findings = {
    'high_volume_flows': high_volume,
    'suspicious_ports': suspicious_ports,
    'anomalies': anomaly_scores
}
reporting.generate_markdown_report(
    flows, 
    suspicious_ports, 
    findings, 
    output_file='investigation_report.md'
)
```

---

## Error Handling

All functions raise descriptive exceptions:
- `SchemaError`: Data schema validation failure
- `DataError`: Malformed or inconsistent data
- `ModelError`: ML model fitting or prediction failure
- `ReportError`: Report generation failure

Wrap calls in try-except blocks for production use:
```python
try:
    flows = data_loader.load_netflow_csv('data.csv')
except FileNotFoundError:
    print("Data file not found")
except SchemaError as e:
    print(f"Invalid schema: {e}")
```
