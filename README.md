# aircheck

A tool for airflow DAG integrity validation.

## Motivation
The process in which a locally developed DAG is picked up, parsed and validated by the `airflow` instance can often be lengthy. So is the feedback cycle, which can be especially frustrating in case mistakes are made in the development phase.
This tool can make it much, much shorter and therefore more efficient - why wait possibly hours to see your DAG have cycle errors in the UI, when you could see that even before you commit to the repository?

The aim of the project is two-fold:

- enable the users to run checks that would fail locally, before they fail in the airflow UI
- allow to enforce standards related to certain DAG properties.

The first part involves:
- checking if modules containing DAGs are properly loaded (i.e. no `ImportErrors` etc.)
- checking for cycles in DAGs
- checking for duplicated DAG ids
- checking for duplicated task ids within a DAG

The latter allows users to enforce that:
- all DAGs have IDs starting with a certain prefix (e.g. indicating the team developing the DAG)
- DAG IDs don't contain whitespaces (those can confuse the airflow UI)
- every DAG has at least one task associated with it (i.e. there are no 'empty' DAGs).
- tasks in DAGs are not dangling (i.e. they have at least one down- or upstream dependency)

## Installation

### PyPI

`aircheck` can be installed with `pip`.

```bash
pip install aircheck
```

Link to the project: [PyPI aircheck](https://pypi.org/project/aircheck/)

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
aircheck ./dags/dag1.py ./dags/dag2.py --check-whitespace --dag-id-prefix <prefix>
```

### Pre-commit hook

```yaml
- repo: https://github.com/AleksanderWWW/aircheck
  rev: v0.1.2
  hooks:
    - id: aircheck
      args: ["--check-empty-dags", "--dag-path", "<non-standard path>"]
```

### Python package

```python
from aircheck.core.checks import check_for_duplicated_dags, check_for_empty_dag
from aircheck.core.load import load_dags

dag_info = load_dags(dag_path="dag_folder/dags")

if dag_info.import_errors:
    # handle import errors
    ...

dags = dag_info.dags
dag_ids = dag_info.dag_ids
check_for_duplicated_dags(dag_ids)

for dag in dags:
    check_for_empty_dag(dag)
```

### Arguments

| Name                     | Type   | Description                                                                 |
|--------------------------|--------|-----------------------------------------------------------------------------|
| `--dag-path`             | `str`  | Path to the DAG folder. Default: `./dags`                                   |
| `--dag-id-prefix`        | `str`  | Prefix that all DAG ids should have for the check to succeed. Default: `""` |
| `--check-empty-dags`     | `flag` | Pass to fail for DAGs with no tasks                                         |
| `--check-dangling-tasks` | `flag` | Pass to fail for DAGs with tasks that have no dependencies                  |

**Notes**
- if the files provided to the command are not present in the `--dag-path`, they will be ignored
- when the `--dag-id-prefix` is left as default, then this part of the hook will always succeed
- in case your DAG files have additional dependencies, see [this guide](https://pre-commit.com/#config-additional_dependencies).
