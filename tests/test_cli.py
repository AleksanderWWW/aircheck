from pathlib import Path

import pytest
from click.testing import CliRunner

from aircheck.main import main


@pytest.mark.integration
def test_successful_cli_invoke(dag_path: Path):
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            str(dag_path / "correct_dags.py"),
            "--dag-path",
            str(dag_path),
            "--check-empty-dags",
            "--dag-id-prefix",
            "ABC",
        ],
    )
    assert result.exit_code == 0


@pytest.mark.integration
@pytest.mark.parametrize(
    "filename",
    ["cycle_dags.py", "duplicated_dags.py", "empty_dags.py", "invalid_id_dags.py"],
)
def test_failing_cli_invoke(dag_path: Path, filename: str):
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            str(dag_path / filename),
            "--dag-path",
            str(dag_path),
            "--check-empty-dags",
            "--dag-id-prefix",
            "ABC",
        ],
    )

    assert result.exit_code == 1
