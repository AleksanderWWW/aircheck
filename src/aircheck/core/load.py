import dataclasses
from unittest.mock import patch

from airflow.models import DAG, DagBag, Variable


@dataclasses.dataclass
class DAGImportError:
    file: str
    msg: str


@dataclasses.dataclass
class DAGInfo:
    dags: list[DAG]
    dag_ids: list[str]
    import_errors: list[DAGImportError]


def load_dags(dag_path: str) -> DAGInfo:
    DagBag.logger().disabled = True

    with patch.object(Variable, "get"):
        dagbag = DagBag(dag_folder=dag_path, include_examples=False, safe_mode=True)

    if dagbag.import_errors:
        import_errors = []
        for k, v in dagbag.import_errors.items():
            if v.startswith("Traceback (most recent call last)"):
                v = v.split("\n")[-2]
            import_errors.append(
                DAGImportError(
                    file=k,
                    msg=v,
                )
            )
        return DAGInfo(
            dags=[],
            dag_ids=[],
            import_errors=import_errors,
        )

    dag_objects = [dag for dag in dagbag.dags.values()]

    dag_ids = []
    for stats in dagbag.dagbag_stats:
        dag_ids += _parse_str_list(stats.dags)

    return DAGInfo(dags=dag_objects, dag_ids=dag_ids, import_errors=[])


def _parse_str_list(str_list: str) -> list[str]:
    str_list = str_list[1:-1]  # remove the '[' and ']' at the beginning and end
    if not str_list:
        return []

    ids = str_list.replace("'", "").split(",")

    for idx in range(1, len(ids)):
        # account for the whitespace resulting in splitting a string like 'id1, id2, id3'
        ids[idx] = ids[idx][1:]

    return ids
