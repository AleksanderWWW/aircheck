__all__ = ("check_dags_integrity",)

from aircheck.core.checks import (
    CheckResult,
    check_dag_id_prefix,
    check_for_cycle,
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
) -> CheckResult:
    dags = load_dags(dag_modules=get_dag_modules(dag_path, files))

    result = check_for_duplicated_dags(dags)
    if not result.check_successful:
        return result

    for dag in dags:
        result = check_for_cycle(dag)
        if not result.check_successful:
            return result

        if dag_id_prefix:
            result = check_dag_id_prefix(dag, dag_id_prefix)
            if not result.check_successful:
                return result

        if check_empty_dags:
            result = check_for_empty_dag(dag)
            if not result.check_successful:
                return result

    return result
