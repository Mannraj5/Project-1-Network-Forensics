import ipaddress

import pandas as pd


RFC1918_NETWORKS = [
    ipaddress.ip_network('10.0.0.0/8'),
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16'),
]


def fill_missing_numeric(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)
    return df


def standardize_labels(df: pd.DataFrame) -> pd.DataFrame:
    if 'label' in df.columns:
        df['label'] = df['label'].astype(str).str.strip().str.lower()
    return df


def is_private_ip(value: str) -> bool:
    try:
        ip = ipaddress.ip_address(str(value))
    except ValueError:
        return False
    return any(ip in network for network in RFC1918_NETWORKS)


def derive_network_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if 'source_ip' in df.columns:
        df['source_internal'] = df['source_ip'].apply(is_private_ip)
    if 'destination_ip' in df.columns:
        df['destination_internal'] = df['destination_ip'].apply(is_private_ip)
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if 'total_length_of_fwd_packets' in df.columns and 'total_length_of_bwd_packets' in df.columns:
        df['total_bytes'] = df['total_length_of_fwd_packets'] + df['total_length_of_bwd_packets']
    elif 'bytes' in df.columns and 'total_bytes' not in df.columns:
        df['total_bytes'] = df['bytes']

    if 'total_fwd_packets' in df.columns and 'total_bwd_packets' in df.columns:
        df['total_packets'] = df['total_fwd_packets'] + df['total_bwd_packets']
    elif 'packets' in df.columns and 'total_packets' not in df.columns:
        df['total_packets'] = df['packets']

    if 'flow_duration' not in df.columns and 'flow_duration_milliseconds' in df.columns:
        df['flow_duration'] = df['flow_duration_milliseconds']

    if 'total_bytes' in df.columns and 'total_packets' in df.columns:
        df['bytes_per_packet'] = df['total_bytes'] / df['total_packets'].replace(0, 1)

    if 'total_bytes' in df.columns and 'flow_duration' in df.columns:
        df['byte_rate'] = df['total_bytes'] / df['flow_duration'].replace(0, 1)

    if 'total_packets' in df.columns and 'flow_duration' in df.columns:
        df['packet_rate'] = df['total_packets'] / df['flow_duration'].replace(0, 1)

    if 'source_port' in df.columns:
        df['source_port'] = pd.to_numeric(df['source_port'], errors='coerce').astype('Int64')
    if 'destination_port' in df.columns:
        df['destination_port'] = pd.to_numeric(df['destination_port'], errors='coerce').astype('Int64')

    df = derive_network_features(df)
    df = fill_missing_numeric(df)
    df = standardize_labels(df)
    return df


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = engineer_features(df)
    return df
