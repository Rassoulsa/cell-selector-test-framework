from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import json


@dataclass
class TestResult:
    name: str
    status: str  # PASSED / FAILED / ERROR
    duration: float
    message: str = ""


@dataclass
class TestReport:
    results: list[TestResult] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.now)
    finished_at: datetime | None = None

    def add_result(self, result: TestResult) -> None:
        self.results.append(result)

    def finalize(self) -> None:
        self.finished_at = datetime.now()

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def passed(self) -> int:
        return sum(r.status == "PASSED" for r in self.results)

    @property
    def failed(self) -> int:
        return sum(r.status == "FAILED" for r in self.results)

    @property
    def errors(self) -> int:
        return sum(r.status == "ERROR" for r in self.results)

    def to_dict(self) -> dict:
        return {
            "started_at": self.started_at.isoformat(),
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "summary": {
                "total": self.total,
                "passed": self.passed,
                "failed": self.failed,
                "errors": self.errors,
            },
            "results": [
                {
                    "name": r.name,
                    "status": r.status,
                    "duration": r.duration,
                    "message": r.message,
                }
                for r in self.results
            ],
        }

    def save_json(self, path: str | Path = "reports/test_report.json") -> None:
        path = Path(path)
        path.parent.mkdir(exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)