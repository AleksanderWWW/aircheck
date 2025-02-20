import ast
from _ast import stmt
from dataclasses import dataclass, field


@dataclass
class ParsedModule:
    airflow_impts: list[ast.ImportFrom] = field(default_factory=list)
    op_impts: list[stmt] = field(default_factory=list)
    op_names: set[str] = field(default_factory=set)
    dag_stmts: list[ast.With] = field(default_factory=list)


def parse_module(body: list[stmt]) -> ParsedModule:
    parsed = ParsedModule()

    for elem in body:
        if isinstance(elem, ast.ImportFrom) and elem.module == "airflow":
            parsed.airflow_impts.append(elem)

        elif isinstance(elem, ast.ImportFrom) and elem.module.startswith(
            "airflow.operators"
        ):
            parsed.op_impts.append(elem)

        elif isinstance(elem, ast.With):
            parsed.dag_stmts.append(elem)

    dag_class_imported_as = get_dag_imported_name(parsed.airflow_impts)

    parsed.dag_stmts = [
        elem
        for elem in parsed.dag_stmts
        if elem.items[0].context_expr.func.id == dag_class_imported_as
    ]

    op_names = []
    for op_imp in parsed.op_impts:
        op_names += [name.asname or name.name for name in op_imp.names]
    parsed.op_names = set(op_names)

    return parsed


def get_dag_imported_name(imports: list[ast.ImportFrom]) -> str:
    dag_class_imported_as = "DAG"

    for imp_stmt in imports:
        for imp_name in imp_stmt.names:
            if imp_name.name == "DAG" and imp_name.asname is not None:
                dag_class_imported_as = imp_name.asname

    return dag_class_imported_as
