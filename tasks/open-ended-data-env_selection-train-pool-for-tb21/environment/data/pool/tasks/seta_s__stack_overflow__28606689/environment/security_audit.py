#!/usr/bin/env python3
"""Android Security Compliance Audit Tool

Scans Android project source code for proper FLAG_SECURE usage
across all Activity classes and generates a compliance report.
"""

import os
import re
import json
import sys
import yaml
from datetime import datetime


class SecurityAuditor:
    def __init__(self, config_path):
        self.config = self._load_config(config_path)
        self.violations = []
        self.scanned_activities = []
        self.exempt_activities = self.config.get('exempt_activities', [])

    def _load_config(self, config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def scan(self):
        """Scan all configured paths for Activity files."""
        for scan_path in self.config['scan_paths']:
            if not os.path.exists(scan_path):
                print(f"Warning: scan path {scan_path} does not exist")
                continue
            self._scan_directory(scan_path)

    def _scan_directory(self, directory):
        """Recursively scan directory for Java and Kotlin files."""
        for root, dirs, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                if filename.endswith('.java'):
                    self.scan_java_file(filepath)
                elif filename.endswith('.kt'):
                    self.scan_java_file(filepath)

    def scan_java_file(self, filepath):
        """Scan a Java file for Activity classes and FLAG_SECURE usage."""
        with open(filepath, 'r') as f:
            content = f.read()

        activity_match = re.search(r'class\s+(\w+)\s+extends\s+Activity', content)
        if not activity_match:
            return

        activity_name = activity_match.group(1)

        if activity_name in self.exempt_activities:
            return

        self.scanned_activities.append(activity_name)
        self._check_flag_secure(content, activity_name, filepath)

    def scan_kotlin_file(self, filepath):
        """Scan a Kotlin file for Activity classes and FLAG_SECURE usage."""
        with open(filepath, 'r') as f:
            content = f.read()

        activity_match = re.search(r'class\s+(\w+)\s*:\s*\w*Activity\s*\(', content)
        if not activity_match:
            return

        activity_name = activity_match.group(1)

        if activity_name in self.exempt_activities:
            return

        self.scanned_activities.append(activity_name)
        self._check_flag_secure_kotlin(content, activity_name, filepath)

    def _check_flag_secure(self, content, activity_name, filepath):
        """Check FLAG_SECURE usage in a Java Activity file."""
        has_flag_secure = 'FLAG_SECURE' in content

        if not has_flag_secure:
            self.violations.append({
                'activity': activity_name,
                'file': filepath,
                'type': 'missing_flag_secure',
                'message': f'{activity_name} does not apply FLAG_SECURE'
            })
            return

        oncreate_match = re.search(
            r'void\s+onCreate\s*\([^)]*\)\s*\{(.*?)(?=\n\s*(?:protected|public|private|void|\})\s)',
            content, re.DOTALL
        )
        if oncreate_match:
            oncreate_body = oncreate_match.group(1)
            if 'FLAG_SECURE' not in oncreate_body:
                onresume_match = re.search(
                    r'void\s+onResume\s*\([^)]*\)\s*\{(.*?)(?=\n\s*(?:protected|public|private|void|\})\s)',
                    content, re.DOTALL
                )
                if onresume_match and 'FLAG_SECURE' in onresume_match.group(1):
                    self.violations.append({
                        'activity': activity_name,
                        'file': filepath,
                        'type': 'wrong_lifecycle_method',
                        'message': f'{activity_name} applies FLAG_SECURE in onResume instead of onCreate'
                    })
                    return

        conditional_pattern = re.search(
            r'if\s*\(.*(?:BuildConfig|DEBUG|isDebug).*\)\s*\{[^}]*FLAG_SECURE',
            content, re.DOTALL
        )
        if conditional_pattern:
            self.violations.append({
                'activity': activity_name,
                'file': filepath,
                'type': 'conditional_flag_secure',
                'message': f'{activity_name} applies FLAG_SECURE conditionally (debug guard detected)'
            })

    def _check_flag_secure_kotlin(self, content, activity_name, filepath):
        """Check FLAG_SECURE usage in a Kotlin Activity file."""
        has_flag_secure = 'FLAG_SECURE' in content

        if not has_flag_secure:
            self.violations.append({
                'activity': activity_name,
                'file': filepath,
                'type': 'missing_flag_secure',
                'message': f'{activity_name} does not apply FLAG_SECURE'
            })
            return

        oncreate_match = re.search(
            r'override\s+fun\s+onCreate\s*\([^)]*\)\s*\{(.*?)(?=\n\s*(?:override|fun|private|public|\})\s)',
            content, re.DOTALL
        )
        if oncreate_match:
            oncreate_body = oncreate_match.group(1)
            if 'FLAG_SECURE' not in oncreate_body:
                self.violations.append({
                    'activity': activity_name,
                    'file': filepath,
                    'type': 'wrong_lifecycle_method',
                    'message': f'{activity_name} applies FLAG_SECURE outside of onCreate'
                })
                return

        conditional_pattern = re.search(
            r'if\s*\(.*(?:BuildConfig|DEBUG|isDebug).*\)\s*\{[^}]*FLAG_SECURE',
            content, re.DOTALL
        )
        if conditional_pattern:
            self.violations.append({
                'activity': activity_name,
                'file': filepath,
                'type': 'conditional_flag_secure',
                'message': f'{activity_name} applies FLAG_SECURE conditionally (debug guard detected)'
            })

    def generate_report(self):
        """Generate compliance report as JSON."""
        report_path = self.config['report_output']

        report = {
            'scan_timestamp': datetime.now().isoformat(),
            'scanned_activities': sorted(self.scanned_activities),
            'exempt_activities': sorted(self.exempt_activities),
            'violations': self.violations,
            'total_scanned': len(self.scanned_activities),
            'total_violations': len(self.violations),
            'compliant': len(self.violations) == 0
        }

        with open(report_path, 'a') as f:
            json.dump(report, f, indent=2)

        return report


def main():
    config_path = '/project/tools/audit_config.yaml'

    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}")
        sys.exit(1)

    auditor = SecurityAuditor(config_path)
    auditor.scan()
    report = auditor.generate_report()

    print(f"Scan complete. Scanned {report['total_scanned']} activities.")
    print(f"Found {report['total_violations']} violations.")

    if report['compliant']:
        print("STATUS: COMPLIANT - All activities properly secured.")
    else:
        print("STATUS: NON-COMPLIANT - Violations found:")
        for v in report['violations']:
            print(f"  - [{v['type']}] {v['message']}")

    sys.exit(0 if report['compliant'] else 1)


if __name__ == '__main__':
    main()
