class AircheckException(Exception):
    def __init__(self, dag_id: str, lineno: int) -> None:
        self.dag_id = dag_id
        self.lineno = lineno


class DeprecatedParamsFound(AircheckException):
    def __init__(self, dag_id: str, lineno: int, deprecated_params) -> None:
        super().__init__(dag_id, lineno)
        self.dp = deprecated_params

    def __str__(self) -> str:
        return f"DAG '{self.dag_id}' defined on line {self.lineno} has deprecated params: {self.dp}"


class DAGIDNotPresent(AircheckException):
    def __str__(self) -> str:
        return f"DAG defined on line {self.lineno} does not have ID"
