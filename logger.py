import json
import os
from datetime import datetime
from pathlib import Path


class HealthLogger:
    """Handles logging system metrics to a JSON-formatted log file."""

    def __init__(self, log_file="logs/health.log"):
        self.log_file = Path(log_file)

        # Ensures the parent directory exists
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def log_metrics(
        self,
        metrics,
    ):
        """Append a new log entry as a JSON object to the file."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics,
        }

        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")
        except IOError as e:
            print(f"Failed to write to log file: {e}")
