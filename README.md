# aircheck

A tool for airflow DAG integrity validation.

The aim of the project is two-fold:

- enable the users to run checks that would fail locally, before they fail in the airflow UI
- allow to enforce standards related to certain DAG properties.

The first part involves:
- checking for cycles in DAGs
- checking for duplicated DAGs

The latter allows users to enforce that:
- all DAGs have IDs starting with a certain prefix (e.g. indicating the team developing the DAG)
- DAG IDs don't contain whitespaces (those can confuse the airflow UI)
- every DAG has at least one task associated with it (i.e. there are no 'empty' DAGs).

## Installation

### PyPI

`aircheck` can be installed with `pip`.

```bash
pip install aircheck
```

### From source

Another option is to install `aircheck` from the source GitHub repo.

```bash
git clone https://github.com/AleksanderWWW/aircheck.git
cd aircheck && pip install .
```

Optionally install `dev` requirements, like `pytest`, `ruff` etc.
```bash
cd aircheck && pip install .[dev]
```

## Usage

After a successful installation, the project can be used in three main ways.

### Commandline tool

```bash
aircheck ./dags/dag1.py ./dags/dag2.py --check-whitespace --check-prefix --dag-id-prefix <prefix>
```

### Pre-commit hook

```yaml
- repo: https://github.com/AleksanderWWW/aircheck
  rev: v0.1.0
  hooks:
    - id: aircheck
      args: ["--check-whitespace", "--check-empty-dags", "--dag-path" "<non-standard path>"]
```

### Python package

```python
from aircheck.core.checks import check_for_duplicated_dags, check_for_empty_dag
from aircheck.core.load import load_dags

dags = load_dags(["./dags/dag1.py", "./dags/dag2.py"])

check_for_duplicated_dags(dags)

for dag in dags:
    check_for_empty_dag(dag)
```
