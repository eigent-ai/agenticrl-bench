import os


class ExperimentReport:
    def __init__(self, name, epochs, final_loss, val_loss, row_count, column_means, config_type):
        self.name = name
        self.epochs = epochs
        self.final_loss = final_loss
        self.val_loss = val_loss
        self.row_count = row_count
        self.column_means = column_means
        self.config_type = config_type

    def __repr__(self):
        lines = [
            f"=== Experiment Report: {self.name} ===",
            f"Epochs: {self.epochs}",
            f"Final Loss: {self.final_loss}",
            f"Validation Loss: {self.val_loss}",
            f"Dataset Rows: {self.row_count}",
            f"Column Means: {self.column_means}",
            f"Config Type: {self.config_type}",
            "=" * 40,
        ]
        return "\n".join(lines)

    def __str__(self):
        return f"ExperimentReport({self.name}, loss={self.final_loss})"


class ReportCollection:
    def __init__(self):
        self.reports = []

    def add(self, report):
        self.reports.append(report)

    def write_to_file(self, filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f:
            f.write("ML Experiment Tracking Report\n")
            f.write("=" * 40 + "\n\n")
            for report in self.reports:
                f.write(str(report) + "\n\n")
