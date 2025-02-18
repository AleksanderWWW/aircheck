__all__ = ("check_dags_integrity",)

from airflow.utils.dag_cycle_tester import check_cycle

from aircheck.core.checks import (
    check_dag_id_prefix,
    check_for_duplicated_dags,
    check_for_empty_dag,
)
from aircheck.core.load import load_dags
from aircheck.core.utils import get_dag_modules


def check_dags_integrity(
    files: list[str],
    dag_path: str,
    dag_id_prefix: str,
    check_empty_dags: bool,
) -> None:
    dags = load_dags(dag_modules=get_dag_modules(dag_path, files))

    check_for_duplicated_dags(dags)

    for dag in dags:
        check_cycle(dag)

        if dag_id_prefix:
            check_dag_id_prefix(dag, dag_id_prefix)

        if check_empty_dags:
            check_for_empty_dag(dag)
