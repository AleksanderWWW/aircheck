from typing import NamedTuple


class CheckResult(NamedTuple):
    check_successful: bool
    err_msg: str | None = None
