import json
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from datetime import date, datetime
from typing import Dict, List

import requests_cache
from github import Github, Issue
from logzero import logger
from tqdm import tqdm

from pr_report.display import print_report


@contextmanager
def use_cache(disable):
    if disable:
        logger.debug("Cache disabled...")
        yield
    else:
        cache_name = "pr-report"
        requests_cache.install_cache(cache_name)
        yield
        requests_cache.uninstall_cache()


@dataclass
class PullRequest:
    created_at: date
    closed_at: date
    id: int
    number: int
    repository: str
    state: str
    title: str
    url: str
    user: str

    @classmethod
    def from_raw(cls, gh: Github, raw: Issue):
        pr = gh.get_repo(raw.repository.id).get_pull(raw.number)
        return cls(
            created_at=raw.created_at.date(),
            closed_at=raw.closed_at.date(),
            id=raw.id,
            number=raw.number,
            repository=raw.repository.full_name,
            state="merged" if pr.merged else raw.state,
            title=raw.title,
            url=raw.url,
            user=raw.user.login,
        )


def pr_report(client: Github, author: str, since: datetime, disable_cache: bool):

    logger.debug("Pulling PRs for %s since %s", author, since)

    all_prs = []
    in_progress: Dict[str, List[PullRequest]] = defaultdict(list)
    closed: Dict[date, Dict[str, List[PullRequest]]] = defaultdict(
        lambda: defaultdict(list)
    )

    with use_cache(disable_cache):
        issues = client.search_issues(
            "", author=author, type="pr", closed=f">{since.date()}"
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
