__all__ = (
    "check_for_duplicated_dags",
    "check_dag_id_prefix",
    "check_for_empty_dag",
    "CheckResult",
)

from typing import NamedTuple

from airflow.models import DAG


class CheckResult(NamedTuple):
    check_successful: bool
    err_msg: str | None = None


def check_for_duplicated_dags(dag_ids: list[str]) -> CheckResult:
    seen = set()

    for dag in dag_ids:
        if dag in seen:
            return CheckResult(False, err_msg=f"DAG '{dag}' has duplicates")

        seen.add(dag)

    return CheckResult(check_successful=True)


def check_dag_id_prefix(dag_ids: list[str], expected_prefix: str) -> CheckResult:
    for dag in dag_ids:
        if not dag.startswith(expected_prefix):
            return CheckResult(
                False,
                err_msg=f"DAG '{dag}' does not include required prefix {expected_prefix}",
            )

    return CheckResult(check_successful=True)


def check_for_empty_dag(dag: DAG) -> CheckResult:
    if not dag.tasks:
        return CheckResult(
            False, err_msg=f"DAG '{dag.dag_id}' must have at least one task"
        )
    return CheckResult(check_successful=True)
