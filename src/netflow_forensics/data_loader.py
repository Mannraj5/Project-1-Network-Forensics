from pathlib import Path

import pandas as pd


COLUMN_ALIASES = {
    'srcip': 'source_ip',
    'dstip': 'destination_ip',
    'src_ip': 'source_ip',
    'dst_ip': 'destination_ip',
    'sip': 'source_ip',
    'dip': 'destination_ip',
    'srcport': 'source_port',
    'dstport': 'destination_port',
    'sport': 'source_port',
    'dport': 'destination_port',
    'fwd_pkts': 'total_fwd_packets',
    'bwd_pkts': 'total_bwd_packets',
    'total_fwd_pkts': 'total_fwd_packets',
    'total_bwd_pkts': 'total_bwd_packets',
    'bytes': 'total_bytes',
    'dur': 'flow_duration',
    'duration': 'flow_duration',
    'labelled': 'label',
}


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(col).strip().lower().replace(' ', '_').replace('-', '_') for col in df.columns]
    return df


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    normalized_columns = {}
    for col in df.columns:
        normalized_columns[col] = COLUMN_ALIASES.get(col, col)
    return df.rename(columns=normalized_columns)


def cast_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for column in df.columns:
        if column in ('source_ip', 'destination_ip', 'protocol', 'label', 'timestamp', 'start_time', 'end_time'):
            continue
        if df[column].dtype == object:
            df[column] = pd.to_numeric(df[column].astype(str).str.replace('[^0-9.-]', '', regex=True), errors='coerce')
    return df


def load_flow_data(csv_path: Path) -> pd.DataFrame:
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f'Flow data file not found: {csv_path}')

    df = pd.read_csv(csv_path)
    df = clean_column_names(df)
    df = normalize_columns(df)
    df = cast_numeric_columns(df)

    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    if 'start_time' in df.columns:
        df['start_time'] = pd.to_datetime(df['start_time'], errors='coerce')
    if 'end_time' in df.columns:
        df['end_time'] = pd.to_datetime(df['end_time'], errors='coerce')

    return df
