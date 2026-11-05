import os
import json
from datetime import datetime, timezone


def write_report(output_dir, results):
    report = {
        'dataset_count': len(results),
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'datasets': results
    }

    report_path = os.path.join(output_dir, 'report.json')
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f'Report written to {report_path}')
