from typing import List

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


def get_ml_feature_columns(df: pd.DataFrame) -> List[str]:
    candidates = [
        'total_bytes',
        'total_packets',
        'flow_duration',
        'total_fwd_packets',
        'total_bwd_packets',
    ]
    return [col for col in candidates if col in df.columns]


def build_feature_matrix(df: pd.DataFrame, features: List[str]) -> pd.DataFrame:
    X = df[features].fillna(0).astype(float)
    scaler = StandardScaler()
    return pd.DataFrame(scaler.fit_transform(X), columns=features, index=df.index)


def train_isolation_forest(X: pd.DataFrame, contamination: float = 0.05) -> IsolationForest:
    model = IsolationForest(contamination=contamination, random_state=42)
    model.fit(X)
    return model


def detect_anomalies(df: pd.DataFrame, model: IsolationForest, features: List[str]) -> pd.DataFrame:
    X = build_feature_matrix(df, features)
    df = df.copy()
    df['anomaly_score'] = model.decision_function(X)
    df['anomaly_flag'] = model.predict(X) == -1
    return df


def run_anomaly_detection(df: pd.DataFrame, contamination: float = 0.05) -> tuple[pd.DataFrame, dict]:
    features = get_ml_feature_columns(df)
    if not features:
        return df.copy(), {
            'anomaly_count': 0,
            'anomaly_ratio': 0.0,
            'features': [],
        }

    feature_matrix = build_feature_matrix(df, features)
    model = train_isolation_forest(feature_matrix, contamination)
    scored_df = detect_anomalies(df, model, features)
    anomaly_count = int(scored_df['anomaly_flag'].sum())
    anomaly_ratio = float(anomaly_count / len(scored_df)) if len(scored_df) else 0.0

    return scored_df, {
        'anomaly_count': anomaly_count,
        'anomaly_ratio': anomaly_ratio,
        'features': features,
    }
