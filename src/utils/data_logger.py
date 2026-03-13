import csv
from pathlib import Path
from datetime import datetime


class DataLogger:
    def __init__(self, file_path: str = "reports/test_data_log.csv"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(exist_ok=True)

        if not self.file_path.exists():
            with open(self.file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([
                    "timestamp",
                    "test_name",
                    "device",
                    "target",
                    "actual",
                    "status",
                    "message"
                ])

    def log(
        self,
        test_name: str,
        device: str,
        target: str | float,
        actual: str | float,
        status: str,
        message: str = "",
    ) -> None:
        with open(self.file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now().isoformat(),
                test_name,
                device,
                target,
                actual,
                status,
                message,
            ])