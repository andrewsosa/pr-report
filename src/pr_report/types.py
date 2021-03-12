from dataclasses import dataclass
from datetime import date

from github import Github, Issue


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
            closed_at=None if not raw.closed_at else raw.closed_at.date(),
            id=raw.id,
            number=raw.number,
            repository=raw.repository.full_name,
            state="merged" if pr.merged else raw.state,
            title=raw.title,
            url=pr.html_url,
            user=raw.user.login,
        )
