import pathlib

import click

from airflow.utils.dag_cycle_tester import check_cycle

from aircheck.checks import check_dag_id_prefix, check_for_empty_dag, check_for_whitespace_in_id, check_for_duplicated_dags
from aircheck.load import load_dags


DEFAULT_DAG_PATH = str(pathlib.Path.cwd() / "dags")


@click.command()
@click.option("--dag_path", type=click.Path(exists=True), default=DEFAULT_DAG_PATH)
@click.option("--check-prefix", is_flag=True, help="Check if DAG ID starts with a given prefix.")
@click.option("--dag-id-prefix", default="", help="DAG ID prefix to check against.")
@click.option("--check-whitespace", is_flag=True, help="Check for whitespace in DAG ID.")
@click.option("--check-empty-dags", is_flag=True, help="Check for empty DAGs.")
def main(
        dag_path: str, check_prefix: bool, dag_id_prefix: str, check_whitespace: bool, check_empty_dags: bool,
) -> None:
    """CLI entry point for DAG validation."""
    dags = load_dags(dag_path)

    check_for_duplicated_dags(dags)

    for dag in dags:

        check_cycle(dag)

        if check_prefix:
            check_dag_id_prefix(dag, dag_id_prefix)

        if check_whitespace:
            check_for_whitespace_in_id(dag)

        if check_empty_dags:
            check_for_empty_dag(dag)


if __name__ == "__main__":
    main()
