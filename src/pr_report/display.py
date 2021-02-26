"""Formats report output.

$ pr-report

In Progress
    schireson/media-activation-platform-actions
        #606 MSE-629: Wrap googleads search in backoff

Closed 2021/02/24
    schireson/media-activation-infrastructure
        #175 Fix: Rename dag and tasks for googleads daily
        #174 MSE-612: Add daily dag for googleads ad daily log video
    schireson/media-activation-platform-actions
        #604 Switch Twitter alerting to use line item daily logs
        #601 MSE-607: Fix typo in metrics recording
"""

import huepy as hp


def print_bold_line(msg):
    print("{}".format(hp.bold(hp.white(msg))))


def print_pr_line(number, title, state):
    if state == "merged":
        print("    {tag} {title}".format(tag=hp.purple(f"#{number}"), title=title))
    elif state == "open":
        print("    {tag} {title}".format(tag=hp.green(f"#{number}"), title=title))
    else:
        print("    {tag} {title}".format(tag=hp.red(f"#{number}"), title=title))


def print_report(in_progress, closed):

    print("")
    print_bold_line("In Progress")
    for repo, prs in in_progress.items():
        print(f"  {repo}")
        for pr in prs:
            print(f"    #{pr.number} {pr.title}")

    if not in_progress:
        print("  {}".format(hp.italic("No open pull requests.")))

    for ds, repos in closed.items():
        print("")
        print_bold_line(f"Closed {str(ds)}")
        for repo, prs in repos.items():
            print(f"  {repo}")
            for pr in prs:
                print_pr_line(pr.number, pr.title, pr.state)

    print("")
