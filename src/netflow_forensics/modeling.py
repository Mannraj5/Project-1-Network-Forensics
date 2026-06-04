from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, f1_score, precision_score,
                             recall_score)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler


def get_classification_features(df: pd.DataFrame) -> List[str]:
    candidates = [
        'total_bytes',
        'total_packets',
        'flow_duration',
        'byte_rate',
        'packet_rate',
        'total_fwd_packets',
        'total_bwd_packets',
    ]
    return [col for col in candidates if col in df.columns]


def encode_labels(df: pd.DataFrame, label_col: str = 'label') -> Tuple[pd.Series, LabelEncoder]:
    labels = df[label_col].astype(str).str.strip().str.lower()
    encoder = LabelEncoder()
    encoded = pd.Series(encoder.fit_transform(labels), index=df.index)
    return encoded, encoder


def train_supervised_model(X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model


def evaluate_classification(y_true: pd.Series, y_pred: pd.Series) -> Dict[str, float]:
    return {
        'accuracy': float(accuracy_score(y_true, y_pred)),
        'precision': float(precision_score(y_true, y_pred, average='weighted', zero_division=0)),
        'recall': float(recall_score(y_true, y_pred, average='weighted', zero_division=0)),
        'f1_score': float(f1_score(y_true, y_pred, average='weighted', zero_division=0)),
    }


def run_supervised_classification(df: pd.DataFrame, label_col: str = 'label', test_size: float = 0.3) -> Dict:
    if label_col not in df.columns:
        return {
            'error': 'No label column found',
            'accuracy': 0.0,
            'f1_score': 0.0,
            'report': {},
            'confusion_matrix': [],
            'features': [],
        }

    features = get_classification_features(df)
    if not features:
        return {
            'error': 'No suitable features available',
            'accuracy': 0.0,
            'f1_score': 0.0,
            'report': {},
            'confusion_matrix': [],
            'features': [],
        }

    X = df[features].fillna(0).astype(float)
    y, encoder = encode_labels(df, label_col)

    if len(set(y)) < 2:
        return {
            'error': 'Not enough label classes for supervised classification',
            'accuracy': 0.0,
            'f1_score': 0.0,
            'report': {},
            'confusion_matrix': [],
            'features': features,
        }

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        stratify=y,
        random_state=42,
    )

    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=features, index=X_train.index)
    X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=features, index=X_test.index)

    model = train_supervised_model(X_train_scaled, y_train)
    predictions = model.predict(X_test_scaled)
    metrics = evaluate_classification(y_test, predictions)
    report = classification_report(y_test, predictions, target_names=list(encoder.classes_), output_dict=True)
    cm = confusion_matrix(y_test, predictions).tolist()

    return {
        'accuracy': metrics['accuracy'],
        'precision': metrics['precision'],
        'recall': metrics['recall'],
        'f1_score': metrics['f1_score'],
        'report': report,
        'confusion_matrix': cm,
        'features': features,
        'label_classes': list(encoder.classes_),
        'test_size': test_size,
    }
