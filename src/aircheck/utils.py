from pathlib import Path


def get_dag_modules(dag_path: str, modules: list[str]) -> list[str]:
    dp = Path(dag_path).resolve()

    return [mod for mod in modules if Path(mod).is_relative_to(dp)]
