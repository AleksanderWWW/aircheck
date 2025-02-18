import pathlib

import click

from aircheck.integrity_check import check_dags_integrity

DEFAULT_DAG_PATH = str(pathlib.Path.cwd() / "dags")


@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option(
    "--dag-path",
    type=click.Path(exists=True),
    default=DEFAULT_DAG_PATH,
    help="Path where DAG files are",
)
@click.option("--dag-id-prefix", default="", help="DAG ID prefix to enforce.")
@click.option("--check-empty-dags", is_flag=True, help="Check for empty DAGs.")
def main(
    files: list[str],
    dag_path: str,
    dag_id_prefix: str,
    check_empty_dags: bool,
) -> None:
    """CLI entry point for DAG integrity validation."""
    check_dags_integrity(
        files=files,
        dag_path=dag_path,
        dag_id_prefix=dag_id_prefix,
        check_empty_dags=check_empty_dags,
    )


if __name__ == "__main__":
    main()
