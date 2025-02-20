__all__ = (
    "check_for_cycle",
    "check_for_empty_dag",
)

from airflow.exceptions import AirflowDagCycleException
from airflow.models import DAG
from airflow.utils.dag_cycle_tester import check_cycle

from aircheck.core.checks.check_result import CheckResult


def check_for_cycle(dag: DAG) -> CheckResult:
    try:
        check_cycle(dag)
        return CheckResult(check_successful=True)
    except AirflowDagCycleException as exp:
        return CheckResult(False, err_msg=str(exp))


def check_for_empty_dag(dag: DAG) -> CheckResult:
    if not dag.tasks:
        return CheckResult(
            False, err_msg=f"DAG '{dag.dag_id}' must have at least one task"
        )
    return CheckResult(check_successful=True)
