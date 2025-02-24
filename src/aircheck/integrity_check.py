__all__ = ("check_dags_integrity",)

from aircheck.core.checks import (
    CheckResult,
    check_dag_id_prefix,
    check_for_duplicated_dags,
    check_for_empty_dag,
)
from aircheck.core.load import load_dags
from aircheck.core.utils import get_dag_modules


def check_dags_integrity(
    files: list[str],
    dag_path: str,
    dag_id_prefix: str,
    check_empty_dags: bool,
) -> CheckResult:
    dag_modules = get_dag_modules(dag_path, files)

    del files  # no need to keep them anymore and in case of `pre-commit run --all-files` this could get big

    if not dag_modules:
        # no changes made to DAGs - no need to run integrity check
        return CheckResult(check_successful=True)

    dag_info = load_dags(dag_path=dag_path)
    if dag_info.import_errors:
        errors = [f"{err.file}: {err.msg}" for err in dag_info.import_errors]
        err_msg = """\n""".join(errors)
        return CheckResult(False, err_msg=err_msg)

    result = check_for_duplicated_dags(dag_info.dag_ids)
    if not result.check_successful:
        return result

    if dag_id_prefix:
        result = check_dag_id_prefix(dag_info.dag_ids, dag_id_prefix)
        if not result.check_successful:
            return result

    for dag in dag_info.dags:
        if check_empty_dags:
            result = check_for_empty_dag(dag)
            if not result.check_successful:
                return result

    return result
