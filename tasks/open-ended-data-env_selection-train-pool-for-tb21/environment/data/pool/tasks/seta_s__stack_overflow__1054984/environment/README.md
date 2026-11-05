Schema Report Tool
Generates a JSON report of database schema metadata.
Usage: python3 schema_report.py
Output: output/report.json
Report structure: { "<schema>": { "<table_or_view>": { "type": "table"|"view", "columns": [ {"name": ..., "type": ..., "nullable": bool, "default": ...} ], "primary_key": [...], "foreign_keys": [ {"column": ..., "references_table": ..., "references_column": ...} ] } } }
