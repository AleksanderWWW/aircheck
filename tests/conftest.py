import pathlib

import pytest


@pytest.fixture(scope="session")
def dag_path() -> pathlib.Path:
    return pathlib.Path(__file__).parents[0] / "testdata"
