#!/usr/bin/env python3
import mysql.connector
import csv
import os
import sys

DB_CONFIG = {
    'host': 'localhost',
    'user': 'recon',
    'password': 'recon123',
    'database': 'recon_db'
}

QUERY_DIR = '/opt/reconciliation/queries'
OUTPUT_DIR = '/opt/reconciliation/output'


def execute_query_file(cursor, filepath):
    with open(filepath, 'r') as f:
        query = f.read().strip()
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    return columns, rows


def write_csv(filepath, columns, rows):
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        for row in rows:
            writer.writerow(row)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    query_files = sorted([
        f for f in os.listdir(QUERY_DIR) if f.endswith('.sql')
    ])

    all_results = {}
    for qf in query_files:
        filepath = os.path.join(QUERY_DIR, qf)
        print(f"Executing {qf}...")
        try:
            columns, rows = execute_query_file(cursor, filepath)
            output_file = os.path.join(OUTPUT_DIR, qf.replace('.sql', '.csv'))
            write_csv(output_file, columns, rows)
            all_results[qf] = (columns, rows)
            print(f"  -> {len(rows)} rows written to {output_file}")
        except Exception as e:
            print(f"  ERROR executing {qf}: {e}", file=sys.stderr)
            cursor.close()
            conn.close()
            return 1

    if '01_full_match.sql' in all_results:
        columns, rows = all_results['01_full_match.sql']
        report_path = os.path.join(OUTPUT_DIR, 'report.csv')
        write_csv(report_path, columns, rows)
        print(f"Report written to {report_path} with {len(rows)} rows")

    cursor.close()
    conn.close()
    print("Pipeline completed successfully.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
