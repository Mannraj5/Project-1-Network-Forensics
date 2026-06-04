import pandas as pd

from netflow_forensics.ml import run_anomaly_detection
from netflow_forensics.modeling import run_supervised_classification
from netflow_forensics.preprocessing import preprocess


def summarize_dataset(df: pd.DataFrame) -> dict:
    return {
        'total_flows': int(len(df)),
        'unique_source_ips': int(df['source_ip'].nunique()) if 'source_ip' in df.columns else 0,
        'unique_destination_ips': int(df['destination_ip'].nunique()) if 'destination_ip' in df.columns else 0,
        'protocols': df['protocol'].value_counts().to_dict() if 'protocol' in df.columns else {},
        'label_distribution': df['label'].value_counts().to_dict() if 'label' in df.columns else {},
        'internal_source_ratio': float(df['source_internal'].mean()) if 'source_internal' in df.columns else 0.0,
        'internal_destination_ratio': float(df['destination_internal'].mean()) if 'destination_internal' in df.columns else 0.0,
    }


def find_suspicious_ports(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    if 'destination_port' not in df.columns:
        return pd.DataFrame()
    return (
        df['destination_port']
        .value_counts()
        .head(top_n)
        .reset_index(name='count')
        .rename(columns={'index': 'destination_port'})
    )


def find_high_volume_flows(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    if 'total_bytes' not in df.columns:
        return pd.DataFrame()
    return df.sort_values('total_bytes', ascending=False).head(top_n)


def find_port_scanners(df: pd.DataFrame, threshold: int = 10) -> pd.DataFrame:
    if 'source_ip' not in df.columns or 'destination_port' not in df.columns:
        return pd.DataFrame()
    scanner_scores = (
        df.groupby('source_ip')['destination_port']
        .nunique()
        .sort_values(ascending=False)
        .reset_index(name='unique_destination_ports')
    )
    return scanner_scores[scanner_scores['unique_destination_ports'] >= threshold]


def find_outbound_spikes(df: pd.DataFrame, rolling_window: int = 5) -> pd.DataFrame:
    if 'timestamp' not in df.columns or 'total_bytes' not in df.columns:
        return pd.DataFrame()
    df = df.dropna(subset=['timestamp']).sort_values('timestamp')
    bytes_by_time = df.groupby('timestamp')['total_bytes'].sum().rename('bytes')
    spikes = bytes_by_time.rolling(window=rolling_window, min_periods=1).mean().nlargest(10)
    return spikes.reset_index()


def build_correlation(df: pd.DataFrame, features: list[str]) -> pd.DataFrame:
    valid_cols = [col for col in features if col in df.columns]
    return df[valid_cols].corr() if valid_cols else pd.DataFrame()


def run_forensic_analysis(df: pd.DataFrame) -> dict:
    df = preprocess(df)
    summary = summarize_dataset(df)
    suspicious_ports = find_suspicious_ports(df).to_dict(orient='records')
    high_volume_flows = find_high_volume_flows(df, top_n=10).to_dict(orient='records')
    port_scanners = find_port_scanners(df, threshold=8).to_dict(orient='records')
    correlation = build_correlation(df, ['total_bytes', 'total_packets', 'flow_duration', 'byte_rate', 'packet_rate']).fillna(0).to_dict()
    outbound_spikes = find_outbound_spikes(df, rolling_window=5).to_dict(orient='records')

    df, anomaly_summary = run_anomaly_detection(df, contamination=0.1)
    anomaly_flows = (
        df[df['anomaly_flag']]
        .sort_values('anomaly_score')
        .head(10)
        .to_dict(orient='records')
    )

    findings = {
        'summary': summary,
        'suspicious_ports': suspicious_ports,
        'high_volume_flows': high_volume_flows,
        'port_scanners': port_scanners,
        'correlation': correlation,
        'outbound_spikes': outbound_spikes,
        'anomaly_summary': anomaly_summary,
        'anomaly_flows': anomaly_flows,
    }

    if 'label' in df.columns and df['label'].nunique() > 1:
        classification = run_supervised_classification(df)
        findings['classification'] = classification

    return findings
