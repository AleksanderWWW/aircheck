import pathlib
import sys

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
@click.option(
    "--check-dangling-tasks", is_flag=True, help="Check for dangling tasks in DAGs."
)
def main(
    files: list[str],
    dag_path: str,
    dag_id_prefix: str,
    check_empty_dags: bool,
    check_dangling_tasks: bool,
) -> None:
    """CLI entry point for DAG integrity validation."""
    result = check_dags_integrity(
        files=files,
        dag_path=dag_path,
        dag_id_prefix=dag_id_prefix,
        check_empty_dags=check_empty_dags,
        check_dangling_tasks=check_dangling_tasks,
    )

    if not result.check_successful:
        click.echo("[AIRCHECK] Checks failed!")
        click.echo("Error: " + result.err_msg, err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
