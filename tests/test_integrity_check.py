from pathlib import Path

import pytest
from airflow.exceptions import AirflowDagCycleException, AirflowDagInconsistent

from aircheck.core.checks import AirflowDuplicatedDagIdException
from aircheck.integrity_check import check_dags_integrity


@pytest.mark.integration
class TestCheckDagsIntegrity:
    def _run_integrity(self, dag_path: Path, filename: str) -> None:
        path = dag_path / filename
        check_dags_integrity(
            files=[str(path)],
            dag_path=str(dag_path),
            dag_id_prefix="ABC",
            check_empty_dags=True,
        )

    def test_correct_dags(self, dag_path: Path):
        self._run_integrity(dag_path, "correct_dags.py")

        assert True  # the integrity check passed

    def test_incorrect_prefix(self, dag_path):
        with pytest.raises(AirflowDagInconsistent):
            self._run_integrity(dag_path, "invalid_id_dags.py")

    def test_empty_dags(self, dag_path):
        with pytest.raises(AirflowDagInconsistent):
            self._run_integrity(dag_path, "empty_dags.py")

    def test_duplicated_dags(self, dag_path):
        with pytest.raises(AirflowDuplicatedDagIdException):
            self._run_integrity(dag_path, "duplicated_dags.py")

    def test_cycle_dags(self, dag_path):
        with pytest.raises(AirflowDagCycleException):
            self._run_integrity(dag_path, "cycle_dags.py")
