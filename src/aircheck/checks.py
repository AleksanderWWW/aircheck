from airflow.exceptions import AirflowDagInconsistent, AirflowException
from airflow.models import DAG


class AirflowDuplicatedDagIdException(AirflowException):
    def __init__(self, dag_id: str) -> None:
        self._dag_id = dag_id

    def __str__(self) -> str:
        return f"DAG {self._dag_id} has duplicates"


def check_for_duplicated_dags(dags: list[DAG]) -> None:
    seen = set()

    for dag in dags:
        if dag.dag_id in seen:
            raise AirflowDuplicatedDagIdException(dag.dag_id)

        seen.add(dag.dag_id)


def check_dag_id_prefix(dag: DAG, expected_prefix: str) -> None:
    if not dag.dag_id.startswith(expected_prefix):
        raise AirflowDagInconsistent(
            f"DAG {dag.dag_id} does not include required prefix {expected_prefix}"
        )


def check_for_whitespace_in_id(dag: DAG) -> None:
    if " " in dag.dag_id:
        raise AirflowDagInconsistent(f"DAG {dag.dag_id} must not contain whitespaces")


def check_for_empty_dag(dag: DAG) -> None:
    if not dag.tasks:
        raise AirflowDagInconsistent(f"DAG {dag.dag_id} must have at least one task")
