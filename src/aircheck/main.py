import pathlib

import click

from aircheck.integrity_check import check_dags_integrity

DEFAULT_DAG_PATH = str(pathlib.Path.cwd() / "dags")


@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option("--dag_path", type=click.Path(exists=True), default=DEFAULT_DAG_PATH)
@click.option(
    "--check-prefix", is_flag=True, help="Check if DAG ID starts with a given prefix."
)
@click.option("--dag-id-prefix", default="", help="DAG ID prefix to check against.")
@click.option(
    "--check-whitespace", is_flag=True, help="Check for whitespace in DAG ID."
)
@click.option("--check-empty-dags", is_flag=True, help="Check for empty DAGs.")
def main(
    files: list[str],
    dag_path: str,
    check_prefix: bool,
    dag_id_prefix: str,
    check_whitespace: bool,
    check_empty_dags: bool,
) -> None:
    """CLI entry point for DAG integrity validation."""
    check_dags_integrity(
        files=files,
        dag_path=dag_path,
        check_prefix=check_prefix,
        dag_id_prefix=dag_id_prefix,
        check_whitespace=check_whitespace,
        check_empty_dags=check_empty_dags,
    )


if __name__ == "__main__":
    main()
