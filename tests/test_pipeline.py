from pathlib import Path

import pandas as pd

from netflow_forensics.data_loader import load_flow_data
from netflow_forensics.ml import run_anomaly_detection
from netflow_forensics.modeling import run_supervised_classification
from netflow_forensics.preprocessing import preprocess


def test_load_and_preprocess_sample_data():
    data_path = Path('data/sample_netflow.csv')
    df = load_flow_data(data_path)
    df_preprocessed = preprocess(df)

    assert not df_preprocessed.empty
    assert 'total_bytes' in df_preprocessed.columns
    assert 'total_packets' in df_preprocessed.columns
    assert df_preprocessed['total_bytes'].dtype.name in ('int64', 'int32', 'float64', 'Int64')


def test_anomaly_detection_returns_flags():
    data_path = Path('data/sample_netflow.csv')
    df = load_flow_data(data_path)
    df_preprocessed = preprocess(df)
    df_scored, summary = run_anomaly_detection(df_preprocessed, contamination=0.1)

    assert 'anomaly_flag' in df_scored.columns
    assert 'anomaly_score' in df_scored.columns
    assert summary['anomaly_count'] >= 0


def test_supervised_classification_on_sample_data():
    data_path = Path('data/sample_netflow.csv')
    df = load_flow_data(data_path)
    df_preprocessed = preprocess(df)
    classification = run_supervised_classification(df_preprocessed)

    assert 'accuracy' in classification
    assert classification['features']
    assert classification['accuracy'] >= 0.0
