from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


sns.set(style='whitegrid', palette='muted')


def plot_port_distribution(df: pd.DataFrame, path: Path) -> None:
    if 'destination_port' not in df.columns:
        return
    port_counts = df['destination_port'].value_counts().nlargest(20)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=port_counts.index.astype(str), y=port_counts.values)
    plt.xticks(rotation=45)
    plt.title('Top 20 Destination Ports')
    plt.xlabel('Destination Port')
    plt.ylabel('Flow Count')
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def plot_label_distribution(df: pd.DataFrame, path: Path) -> None:
    if 'label' not in df.columns:
        return
    label_counts = df['label'].value_counts()
    plt.figure(figsize=(8, 5))
    sns.barplot(x=label_counts.index, y=label_counts.values)
    plt.title('Traffic Label Distribution')
    plt.xlabel('Label')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def plot_correlation_heatmap(df: pd.DataFrame, features: list[str], path: Path) -> None:
    valid = [f for f in features if f in df.columns]
    if not valid:
        return
    corr = df[valid].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Feature Correlation Heatmap')
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def plot_time_series_bytes(df: pd.DataFrame, path: Path) -> None:
    if 'timestamp' not in df.columns or 'total_bytes' not in df.columns:
        return
    df = df.dropna(subset=['timestamp']).sort_values('timestamp')
    bytes_by_time = df.groupby('timestamp')['total_bytes'].sum()
    plt.figure(figsize=(12, 5))
    plt.plot(bytes_by_time.index, bytes_by_time.values, marker='o')
    plt.title('Total Bytes Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Bytes')
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def plot_anomaly_scores(df: pd.DataFrame, path: Path) -> None:
    if 'anomaly_score' not in df.columns or 'timestamp' not in df.columns:
        return
    df = df.dropna(subset=['timestamp']).sort_values('timestamp')
    score_by_time = df.groupby('timestamp')['anomaly_score'].mean()
    plt.figure(figsize=(12, 5))
    plt.plot(score_by_time.index, score_by_time.values, marker='o')
    plt.title('Anomaly Score Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Anomaly Score')
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def save_visualizations(df: pd.DataFrame, output_dir: Path) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    plot_port_distribution(df, output_dir / 'destination_ports.png')
    plot_label_distribution(df, output_dir / 'label_distribution.png')
    plot_correlation_heatmap(df, ['total_bytes', 'total_packets', 'flow_duration'], output_dir / 'correlation_heatmap.png')
    plot_time_series_bytes(df, output_dir / 'bytes_over_time.png')
    plot_anomaly_scores(df, output_dir / 'anomaly_score_over_time.png')
