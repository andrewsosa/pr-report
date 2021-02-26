import logging
import os
from datetime import datetime, timedelta

import click
import github
import logzero
from logzero import logger

from pr_report.report import pr_report

DEFAULT_WINDOW = str((datetime.today() - timedelta(days=7)).date())


@click.command()
@click.option("--author", "-a")
@click.option("--token", "-t")
@click.option(
    "--since",
    "-s",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=DEFAULT_WINDOW,
    show_default=True,
)
@click.option("--disable-cache", "-d", type=bool, default=False)
@click.option("--verbose", "-v", is_flag=True)
def cli(author: str, token: str, since: datetime, disable_cache: bool, verbose: bool):

    logzero.loglevel(logging.DEBUG if verbose else logging.WARNING)

    if not token:
        token = os.getenv("GITHUB_TOKEN")

    logger.debug("Using Github Token %s", token)
    gh = github.Github(token)

    if not author:
        author = gh.get_user().login

    pr_report(gh, author, since, disable_cache)


if __name__ == "__main__":
    cli()
