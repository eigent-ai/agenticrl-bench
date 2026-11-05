import os
import subprocess

from django.core.management.base import BaseCommand, CommandError

from pipeline.data_loader import load_csv
from pipeline.models import DataRecord


class Command(BaseCommand):
    help = 'Import data from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        filepath = options['filepath']

        if not os.path.exists(filepath):
            raise CommandError(f'File not found: {filepath}')

        self.stdout.write(f'Importing from: {filepath}')

        header_line = subprocess.check_output(
            f"head -1 {filepath}", shell=True
        ).decode().strip()

        self.stdout.write(f'Header: {header_line}')

        required_cols = {'name', 'price', 'quantity'}
        actual_cols = set(c.strip() for c in header_line.split(','))
        if not required_cols.issubset(actual_cols):
            raise CommandError(
                f'CSV missing required columns. Found: {actual_cols}'
            )

        count = 0
        for row in load_csv(filepath):
            DataRecord.objects.create(
                source_file=filepath,
                row_data=row,
                processed=True,
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} records'))
