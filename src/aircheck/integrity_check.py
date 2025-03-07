__all__ = ("check_dags_integrity",)

from aircheck.core.checks import (
    CheckResult,
    check_dag_id_prefix,
    check_for_dangling_tasks,
    check_for_duplicated_dags,
    check_for_empty_dag,
)
from aircheck.core.load import load_dags
from aircheck.core.utils import concat_errors, get_dag_modules


def check_dags_integrity(
    files: list[str],
    dag_path: str,
    dag_id_prefix: str,
    check_empty_dags: bool,
    check_dangling_tasks: bool,
) -> CheckResult:
    if files:
        dag_modules = get_dag_modules(dag_path, files)

        del files

        if not dag_modules:
            # no changes made to DAGs - no need to run integrity check
            return CheckResult(check_successful=True)

    errors: list[str] = []

    dag_info = load_dags(dag_path=dag_path)
    if dag_info.import_errors:
        errors = [f"{err.file}: {err.msg}" for err in dag_info.import_errors]
        err_msg = concat_errors(errors)
        return CheckResult(False, err_msg=err_msg)

    result = check_for_duplicated_dags(dag_info.dag_ids)
    if not result.check_successful:
        errors.append(result.err_msg)

    for dag in dag_info.dags:
        if dag_id_prefix:
            result = check_dag_id_prefix(dag, dag_id_prefix)
            if not result.check_successful:
                errors.append(result.err_msg)

        if check_empty_dags:
            result = check_for_empty_dag(dag)
            if not result.check_successful:
                errors.append(result.err_msg)

        if check_dangling_tasks:
            result = check_for_dangling_tasks(dag)
            if not result.check_successful:
                errors.append(result.err_msg)

    if errors:
        result = CheckResult(check_successful=False, err_msg=concat_errors(errors))

    return result
