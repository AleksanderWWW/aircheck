import glob
import importlib.util
from os.path import join
from types import ModuleType
from pathlib import Path

from airflow.models import DAG



def load_dags(dag_modules: list[str | bytes| Path]) -> list[DAG]:
    dags = []

    for module_path in dag_modules:
        module = load_module(module_path)
        dags += [var for var in vars(module).values() if isinstance(var, DAG)]

    return dags


def load_module(module_path: str | bytes| Path) -> ModuleType:
    module_path = Path(module_path)

    module_name = module_path.name

    mod_spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(mod_spec)
    mod_spec.loader.exec_module(module)

    return module
