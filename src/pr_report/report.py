from collections import defaultdict
from contextlib import contextmanager
from datetime import date, datetime
from typing import Dict, List

import requests_cache
from github import Github
from logzero import logger
from tqdm import tqdm

from pr_report.display import print_report
from pr_report.types import PullRequest


@contextmanager
def use_cache(disable):
    if disable:
        logger.debug("Cache disabled...")
        yield
    else:
        # cache_name = "pr-report"
        requests_cache.install_cache()
        yield
        requests_cache.uninstall_cache()


def pr_report(client: Github, author: str, since: datetime, disable_cache: bool):

    logger.debug("Pulling PRs for %s since %s", author, since)

    all_prs = []
    in_progress: Dict[str, List[PullRequest]] = defaultdict(list)
    closed: Dict[date, Dict[str, List[PullRequest]]] = defaultdict(
        lambda: defaultdict(list)
    )

    # with use_cache(disable_cache):
    issues = client.search_issues(
        "", author=author, type="pr", updated=f">{since.date()}"
    )
    for pr in (
        PullRequest.from_raw(client, iss)
        for iss in tqdm(issues, total=issues.totalCount)
    ):
        all_prs.append(pr)
        if pr.state == "open":
            in_progress[pr.repository].append(pr)
        else:
            closed[pr.closed_at][pr.repository].append(pr)

    print_report(in_progress, closed)

    # with open("pull_requests.json", "w") as fp:
    #     json.dump([asdict(pr) for pr in all_prs], fp, indent=4, default=str)
