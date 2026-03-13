import time
from typing import Callable

from core.logger import setup_logger
from core.report_generator import TestReport, TestResult


class TestRunner:
    def __init__(self):
        self.logger = setup_logger(__name__)
        self.report = TestReport()

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
        self.logger.info("Test suite execution finished")

        return self.report 