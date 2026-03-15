from database.db_manager import DatabaseManager


def test_database_creation_and_insert():
    db = DatabaseManager("temp_test_results.db")

    run_id = db.insert_test_run(
        run_date="2026-03-14T12:00:00",
        total=3,
        passed=3,
        failed=0,
        errors=0,
    )

    assert run_id > 0

    db.insert_test_result(
        run_id=run_id,
        test_name="test_sample",
        status="PASSED",
        duration=0.12,
        message="",
    )

    runs = db.get_all_test_runs()
    assert len(runs) >= 1

    results = db.get_results_for_run(run_id)
    assert len(results) == 1
    assert results[0][0] == "test_sample"