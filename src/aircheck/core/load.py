__all__ = ("get_dag_ids",)

import ast
import pathlib
from _ast import stmt

from aircheck.core.exceptions import DAGIDNotPresent, DeprecatedParamsFound
from aircheck.core.parse import parse_module
from aircheck.core.utils import get_dag_modules


def get_dag_ids(
    dag_path: str, files: list[str], check_deprecated_params: bool
) -> list[str]:
    dags: list[str] = []
    for module in get_dag_modules(dag_path, files):
        mb = get_module_body(module)

        parsed = parse_module(mb)

        dags += get_dag_ids_in_module(parsed.dag_stmts, check_deprecated_params)

    return dags


def get_module_body(module_path: str | bytes | pathlib.Path) -> list[stmt]:
    with open(module_path, "r", encoding="utf-8") as fp:
        return ast.parse(fp.read()).body


def get_dag_ids_in_module(
    dag_stmts: list[ast.With], check_deprecated_params: bool
) -> list[str]:
    return [
        get_dag_id_from_dag_stmt(dag_stmt, check_deprecated_params)
        for dag_stmt in dag_stmts
    ]


def get_dag_id_from_dag_stmt(dag_stmt: ast.With, check_deprecated_params: bool) -> str:
    keywords = dag_stmt.items[0].context_expr.keywords

    try:
        dag_id = next(kw.value.value for kw in keywords if kw.arg == "dag_id")
    except StopIteration:
        args = dag_stmt.items[0].context_expr.args
        if not args:
            raise DAGIDNotPresent(dag_id="", lineno=dag_stmt.lineno)

        dag_id = args[0].value

    if check_deprecated_params:
        deprecated = [kw.arg for kw in keywords if kw.arg in ("schedule_interval",)]
        if deprecated:
            raise DeprecatedParamsFound(
                dag_id, dag_stmt.lineno, deprecated_params=deprecated
            )
    return dag_id
