import sys
from pathlib import Path

import pytest

from aircheck.core.checks import CheckResult
from aircheck.integrity_check import check_dags_integrity


@pytest.mark.integration
class TestCheckDagsIntegrity:
    def _run_integrity(
        self, dag_path: Path, filename: str, prefix: str | None = None
    ) -> CheckResult:
        path = dag_path / filename.strip(".py") / filename
        prefix = prefix or ""
        return check_dags_integrity(
            files=[str(path)],
            dag_path=str(dag_path / filename.strip(".py")),
            dag_id_prefix=prefix,
            check_empty_dags=True,
            check_dangling_tasks=True,
        )

    def test_correct_dags(self, dag_path: Path):
        result = self._run_integrity(dag_path, "correct_dags.py", prefix="ABC")

        assert result.check_successful

        assert result.err_msg is None

    def test_incorrect_prefix(self, dag_path):
        result = self._run_integrity(dag_path, "invalid_id_dags.py", prefix="ABC")

        assert not result.check_successful

        assert "does not include required prefix 'ABC'" in result.err_msg

    def test_empty_dags(self, dag_path):
        result = self._run_integrity(dag_path, "empty_dags.py")

        assert not result.check_successful

        assert "DAG 'empty_dag1' must have at least one task" in result.err_msg

    @pytest.mark.skipif(
        sys.platform == "win32",
        reason="Windows is anyway not supported and it behaves strangely",
    )
    def test_duplicated_dags(self, dag_path):
        result = self._run_integrity(dag_path, "duplicated_dags.py")

        assert not result.check_successful

        assert "DAG 'duplicate_dag' has duplicates" in result.err_msg

    def test_cycle_dags(self, dag_path):
        result = self._run_integrity(dag_path, "cycle_dags.py")

        assert not result.check_successful

        assert (
            "AirflowDagCycleException: Cycle detected in DAG: cycle_dag."
            in result.err_msg
        )

    def test_dangling_tasks(self, dag_path):
        result = self._run_integrity(dag_path, "dangling_tasks.py")

        assert not result.check_successful

        assert "Dangling task" in result.err_msg
