__all__ = (
    "check_for_cycle",
    "check_for_duplicated_dags",
    "check_dag_id_prefix",
    "check_for_empty_dag",
    "CheckResult",
)

from typing import NamedTuple

from airflow.exceptions import AirflowDagCycleException
from airflow.models import DAG
from airflow.utils.dag_cycle_tester import check_cycle


class CheckResult(NamedTuple):
    check_successful: bool
    err_msg: str | None = None


def check_for_cycle(dag: DAG) -> CheckResult:
    try:
        check_cycle(dag)
        return CheckResult(check_successful=True)
    except AirflowDagCycleException as exp:
        return CheckResult(False, err_msg=str(exp))


def check_for_duplicated_dags(dags: list[DAG]) -> CheckResult:
    seen = set()

    for dag in dags:
        if dag.dag_id in seen:
            return CheckResult(False, err_msg=f"DAG '{dag.dag_id}' has duplicates")

        seen.add(dag.dag_id)

    return CheckResult(check_successful=True)


def check_dag_id_prefix(dag: DAG, expected_prefix: str) -> CheckResult:
    if not dag.dag_id.startswith(expected_prefix):
        return CheckResult(
            False,
            err_msg=f"DAG '{dag.dag_id}' does not include required prefix {expected_prefix}",
        )

    return CheckResult(check_successful=True)


def check_for_empty_dag(dag: DAG) -> CheckResult:
    if not dag.tasks:
        return CheckResult(
            False, err_msg=f"DAG '{dag.dag_id}' must have at least one task"
        )
    return CheckResult(check_successful=True)
