from pathlib import Path

import pytest

from aircheck.core.checks import CheckResult
from aircheck.integrity_check import check_dags_integrity


@pytest.mark.integration
class TestCheckDagsIntegrity:
    def _run_integrity(self, dag_path: Path, filename: str) -> CheckResult:
        path = dag_path / filename.strip(".py") / filename
        return check_dags_integrity(
            files=[str(path)],
            dag_path=str(dag_path / filename.strip(".py")),
            dag_id_prefix="ABC",
            check_empty_dags=True,
        )

    def test_correct_dags(self, dag_path: Path):
        assert self._run_integrity(dag_path, "correct_dags.py").check_successful

    def test_incorrect_prefix(self, dag_path):
        assert not self._run_integrity(dag_path, "invalid_id_dags.py").check_successful

    def test_empty_dags(self, dag_path):
        assert not self._run_integrity(dag_path, "empty_dags.py").check_successful

    def test_duplicated_dags(self, dag_path):
        assert not self._run_integrity(dag_path, "duplicated_dags.py").check_successful

    def test_cycle_dags(self, dag_path):
        assert not self._run_integrity(dag_path, "cycle_dags.py").check_successful
