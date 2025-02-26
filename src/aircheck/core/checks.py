__all__ = (
    "check_for_duplicated_dags",
    "check_dag_id_prefix",
    "check_for_empty_dag",
    "check_for_dangling_tasks",
    "CheckResult",
)

from typing import TYPE_CHECKING, NamedTuple

from aircheck.core.utils import concat_errors

if TYPE_CHECKING:
    from airflow.models import DAG


class CheckResult(NamedTuple):
    check_successful: bool
    err_msg: str | None = None


def check_for_duplicated_dags(dag_ids: list[str]) -> CheckResult:
    seen = set()
    errors = []

    for dag in dag_ids:
        if dag in seen:
            errors.append(f"DAG '{dag}' has duplicates")

        seen.add(dag)

    if errors:
        return CheckResult(check_successful=False, err_msg=concat_errors(errors))

    return CheckResult(check_successful=True)


def check_dag_id_prefix(dag: "DAG", expected_prefix: str) -> CheckResult:
    if not dag.dag_id.startswith(expected_prefix):
        msg = f"DAG '{dag.dag_id}' does not include required prefix '{expected_prefix}'"
        return CheckResult(
            False,
            err_msg=f"{dag.fileloc}: {msg}",
        )

    return CheckResult(check_successful=True)


def check_for_empty_dag(dag: "DAG") -> CheckResult:
    if not dag.tasks:
        msg = f"DAG '{dag.dag_id}' must have at least one task"
        return CheckResult(False, err_msg=f"{dag.fileloc}: {msg}")
    return CheckResult(check_successful=True)


def check_for_dangling_tasks(dag: "DAG") -> CheckResult:
    for task in dag.tasks:
        if not task.upstream_list and not task.downstream_list:
            msg = f"Dangling task '{task.task_id}' in DAG '{dag.dag_id}' (no upstream or downstream dependencies)"
            err_msg = f"{dag.fileloc}: {msg}"

            return CheckResult(
                False,
                err_msg=err_msg,
            )

    return CheckResult(check_successful=True)
