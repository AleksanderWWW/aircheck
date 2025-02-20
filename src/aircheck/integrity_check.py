__all__ = ("check_dags_integrity",)

from typing import TYPE_CHECKING

from aircheck.core.checks.check_result import CheckResult
from aircheck.core.checks.static_checks import (
    check_dag_id_prefix,
    check_for_duplicated_dags,
)
from aircheck.core.exceptions import DAGIDNotPresent, DeprecatedParamsFound
from aircheck.core.load import get_dag_ids, get_dags_from_dagbag

if TYPE_CHECKING:
    from airflow.models import DAG


def check_dags_integrity(
    files: list[str],
    dag_path: str,
    dag_id_prefix: str,
    check_deprecated_params: bool,
    check_empty_dags: bool,
) -> CheckResult:
    try:
        dag_ids = get_dag_ids(dag_path, files, check_deprecated_params)
    except (DeprecatedParamsFound, DAGIDNotPresent) as dag_id_exc:
        return CheckResult(False, err_msg=str(dag_id_exc))

    result = run_static_checks(dag_ids, dag_id_prefix)
    if not result.check_successful:
        return result

    dag_objs = get_dags_from_dagbag(dag_path, set(dag_ids))

    return run_dynamic_checks(dags=dag_objs, check_empty_dags=check_empty_dags)


def run_static_checks(dag_ids: list[str], dag_id_prefix: str) -> CheckResult:
    result = check_for_duplicated_dags(dag_ids)
    if not result.check_successful:
        return result

    for dag_id in dag_ids:
        if dag_id_prefix:
            result = check_dag_id_prefix(dag_id, dag_id_prefix)
            if not result.check_successful:
                return result

    return CheckResult(check_successful=True)


def run_dynamic_checks(dags: list["DAG"], check_empty_dags: bool) -> CheckResult:
    from aircheck.core.checks.dynamic_checks import check_for_cycle, check_for_empty_dag

    for dag in dags:
        result = check_for_cycle(dag)
        if not result.check_successful:
            return result

        if check_empty_dags:
            result = check_for_empty_dag(dag)
            if not result.check_successful:
                return result

    return CheckResult(check_successful=True)
