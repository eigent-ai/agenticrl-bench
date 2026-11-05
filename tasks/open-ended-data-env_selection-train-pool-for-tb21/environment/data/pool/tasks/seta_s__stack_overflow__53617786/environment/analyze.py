import pandas as pd
import json
import os
import numpy as np

METRIC_COLS = ['cpu_util', 'mem_util', 'disk_io', 'net_in', 'net_out',
               'latency_ms', 'packet_loss', 'error_rate', 'uptime_pct',
               'temp_celsius', 'voltage']
NULL_THRESHOLD = 5


def load_data(path):
    return pd.read_csv(path)


def filter_nulls(df):
    return df[df.isnull().sum(axis=1) < NULL_THRESHOLD]


def filter_status(df):
    return df.loc[df['status'].isin(['active', 'idle'])]


def compute_summary(df, original_df):
    by_type = df.groupby('device_type')[METRIC_COLS].mean().round(2)
    return {
        'total_devices': len(original_df),
        'by_type': by_type.to_dict('index')
    }


def main():
    df = load_data('/data/device_readings.csv')
    original_df = df.copy()
    df = filter_nulls(df)
    df = filter_status(df)
    report = compute_summary(df, original_df)
    os.makedirs('/output', exist_ok=True)
    with open('/output/report.json', 'w') as f:
        json.dump(report, f, indent=2)
    print(f"Wrote report: {report['total_devices']} devices")


if __name__ == '__main__':
    main()
