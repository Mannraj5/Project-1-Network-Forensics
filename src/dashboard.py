from pathlib import Path

import pandas as pd
import streamlit as st

from netflow_forensics.data_loader import clean_column_names, load_flow_data
from netflow_forensics.modeling import run_supervised_classification
from netflow_forensics.preprocessing import preprocess
from netflow_forensics.ml import run_anomaly_detection


def load_dashboard_data(uploaded_file, default_path: Path) -> pd.DataFrame:
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df = clean_column_names(df)
    else:
        df = load_flow_data(default_path)
    return df


def show_summary_cards(df: pd.DataFrame, anomaly_summary: dict) -> None:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Total flows', len(df))
    col2.metric('Distinct source IPs', df['source_ip'].nunique() if 'source_ip' in df.columns else 0)
    col3.metric('Detected anomalies', anomaly_summary.get('anomaly_count', 0))
    col4.metric('Anomaly ratio', f"{anomaly_summary.get('anomaly_ratio', 0.0):.1%}")


def show_top_ports(df: pd.DataFrame) -> None:
    if 'destination_port' not in df.columns:
        return
    top_ports = df['destination_port'].value_counts().nlargest(10)
    st.subheader('Top Destination Ports')
    st.bar_chart(top_ports)


def show_label_distribution(df: pd.DataFrame) -> None:
    if 'label' not in df.columns:
        return
    label_counts = df['label'].value_counts()
    st.subheader('Label Distribution')
    st.bar_chart(label_counts)


def show_time_series(df: pd.DataFrame) -> None:
    if 'timestamp' not in df.columns or 'total_bytes' not in df.columns:
        return
    time_series = df.dropna(subset=['timestamp']).set_index('timestamp').resample('1T')['total_bytes'].sum()
    st.subheader('Total Bytes Over Time')
    st.line_chart(time_series)


def show_anomaly_table(df: pd.DataFrame) -> None:
    if 'anomaly_flag' not in df.columns:
        return
    st.subheader('Top Anomalous Flows')
    st.dataframe(df.sort_values('anomaly_score').head(15))


def show_top_hosts(df: pd.DataFrame) -> None:
    if 'source_ip' not in df.columns or 'destination_ip' not in df.columns:
        return
    top_sources = df['source_ip'].value_counts().nlargest(10)
    top_destinations = df['destination_ip'].value_counts().nlargest(10)
    st.subheader('Top Talkers and Recipients')
    col1, col2 = st.columns(2)
    col1.bar_chart(top_sources)
    col2.bar_chart(top_destinations)


def show_classification_summary(df: pd.DataFrame) -> None:
    if 'label' not in df.columns:
        return
    classification = run_supervised_classification(df)
    st.subheader('Supervised Classification Summary')
    st.metric('Accuracy', f"{classification['accuracy']:.2%}")
    st.metric('F1 Score', f"{classification['f1_score']:.2f}")
    st.write('**Top classification labels**')
    st.write(pd.DataFrame(classification['report']).transpose())


def main() -> None:
    st.set_page_config(page_title='Network Forensics SIEM Dashboard', layout='wide')
    st.title('Network Forensics SIEM Dashboard')

    st.sidebar.header('Dashboard settings')
    dataset_path = st.sidebar.text_input('Dataset path', 'data/sample_netflow.csv')
    uploaded_file = st.sidebar.file_uploader('Upload a NetFlow CSV', type=['csv'])
    contamination = st.sidebar.slider('Anomaly contamination', 0.01, 0.2, 0.05, 0.01)
    show_raw = st.sidebar.checkbox('Show raw data', value=False)
    show_classification = st.sidebar.checkbox('Run classification', value=True)

    data_path = Path(dataset_path)
    df = load_dashboard_data(uploaded_file, data_path)
    df = preprocess(df)
    df, anomaly_summary = run_anomaly_detection(df, contamination)

    show_summary_cards(df, anomaly_summary)
    show_label_distribution(df)
    show_top_ports(df)
    show_time_series(df)
    show_top_hosts(df)

    if show_classification:
        show_classification_summary(df)

    if show_raw:
        with st.expander('Raw Flow Data'):
            st.dataframe(df)

    show_anomaly_table(df)


if __name__ == '__main__':
    main()
