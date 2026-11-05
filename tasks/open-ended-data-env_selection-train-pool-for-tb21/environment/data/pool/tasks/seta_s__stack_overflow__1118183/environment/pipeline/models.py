from django.db import models


class DataRecord(models.Model):
    source_file = models.CharField(max_length=255)
    row_data = models.JSONField()
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"DataRecord({self.source_file}, processed={self.processed})"
