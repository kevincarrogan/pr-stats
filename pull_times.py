import argparse
import numpy

from tabulate import tabulate

from pulls import get_pulls
from utils import get_closed_at, get_repos_with_bases


def delta_to_days(delta):
    return delta.total_seconds() / 60 / 60 / 24


def get_times(repos, closed_at):
    deltas = []
    for repo, base in repos:
        pulls = get_pulls(repo, base, closed_at)
        for pull in pulls:
            if not pull.is_merged():
                continue
            delta = pull.closed_at - pull.created_at
            days = delta_to_days(delta)
            deltas.append(days)

    deltas = numpy.array(deltas)

    return [(
        deltas.min(),
        deltas.max(),
        deltas.mean(),
        numpy.median(deltas),
        numpy.percentile(deltas, 90),
        numpy.percentile(deltas, 95),
        deltas.std(),
    )]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pull times")
    parser.add_argument(
        "--last-days",
        type=int,
        nargs="?",
        default=10,
        help="PRs closed in last n days",
    )
    parser.add_argument(
        "repos",
        type=str,
        nargs="+",
        help="Repo and base branch names to collect statistics e.g. org_name/repo_name:base_branch_name",
    )
    args = parser.parse_args()
    closed_at = get_closed_at(args.last_days)
    repos = get_repos_with_bases(args.repos)
    print(f"Pull open to closed times in {args.last_days} days")
    times = get_times(repos, closed_at)
    print(tabulate(times, headers=[
        "Shortest (days)",
        "Longest (days)",
        "Average (days)",
        "Median (days)",
        "90th",
        "95th",
        "Std dev",
    ]))
