from pathlib import Path


def get_dag_modules(dag_path: str, modules: list[str]) -> list[str]:
    dp = Path(dag_path).resolve()

    return [
        mod
        for mod in modules
        if Path(mod).resolve().is_relative_to(dp) and Path(mod).suffix == ".py"
    ]


def concat_errors(errors: list[str]) -> str:
    return """\n""".join(errors)
