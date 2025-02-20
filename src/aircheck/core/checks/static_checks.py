from aircheck.core.checks.check_result import CheckResult


def check_for_duplicated_dags(dag_ids: list[str]) -> CheckResult:
    seen = set()

    for di in dag_ids:
        if di in seen:
            return CheckResult(False, err_msg=f"DAG '{di}' has duplicates")

        seen.add(di)

    return CheckResult(check_successful=True)


def check_dag_id_prefix(dag_id: str, expected_prefix: str) -> CheckResult:
    if not dag_id.startswith(expected_prefix):
        return CheckResult(
            False,
            err_msg=f"DAG '{dag_id}' does not include required prefix {expected_prefix}",
        )

    return CheckResult(check_successful=True)
