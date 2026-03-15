import time
from typing import Callable

from core.logger import setup_logger
from core.report_generator import TestReport, TestResult
from database.db_manager import DatabaseManager


class TestRunner:
    def __init__(self):
        self.logger = setup_logger(__name__)
        self.report = TestReport()
        self.db = DatabaseManager()

    def run_test(self, test_func: Callable, name: str | None = None) -> None:
        test_name = name or test_func.__name__
        self.logger.info(f"Running test: {test_name}")

        start = time.perf_counter()

        try:
            test_func()
            duration = time.perf_counter() - start

            self.report.add_result(
                TestResult(
                    name=test_name,
                    status="PASSED",
                    duration=duration,
                )
            )
            self.logger.info(f"Test PASSED: {test_name}")

        except AssertionError as e:
            duration = time.perf_counter() - start

            self.report.add_result(
                TestResult(
                    name=test_name,
                    status="FAILED",
                    duration=duration,
                    message=str(e),
                )
            )
            self.logger.warning(f"Test FAILED: {test_name} | {e}")

        except Exception as e:
            duration = time.perf_counter() - start

            self.report.add_result(
                TestResult(
                    name=test_name,
                    status="ERROR",
                    duration=duration,
                    message=str(e),
                )
            )
            self.logger.error(f"Test ERROR: {test_name} | {e}")

    def run_suite(self, tests: list[Callable]) -> TestReport:
        self.logger.info("Starting test suite execution")

        for test in tests:
            self.run_test(test)

        self.report.finalize()
        self._save_report_to_database()
        self.logger.info("Test suite execution finished")

        return self.report

    def _save_report_to_database(self) -> None:
        run_id = self.db.insert_test_run(
            run_date=self.report.started_at.isoformat(),
            total=self.report.total,
            passed=self.report.passed,
            failed=self.report.failed,
            errors=self.report.errors,
        )

        for result in self.report.results:
            self.db.insert_test_result(
                run_id=run_id,
                test_name=result.name,
                status=result.status,
                duration=result.duration,
                message=result.message,
            )

        self.logger.info(f"Saved test report to database with run_id={run_id}")