import argparse
import numpy

from tabulate import tabulate

from pulls import get_pulls
from utils import get_closed_at, get_repos_with_bases


def get_sizes(repos, closed_at):
    sizes = []
    for repo, base in repos:
        pulls = get_pulls(repo, base, closed_at)
        for pull in pulls:
            if not pull.is_merged():
                continue
            size = pull.additions + pull.deletions
            sizes.append(size)

    sizes = numpy.array(sizes)

    return [(
        sizes.min(),
        sizes.max(),
        sizes.mean(),
        numpy.median(sizes),
        numpy.percentile(sizes, 90),
        numpy.percentile(sizes, 95),
        sizes.std(),
    )]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Review quality")
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
    print(f"Pull sizes in last {args.last_days} days")
    times = get_sizes(repos, closed_at)
    print(tabulate(times, headers=[
        "Smallest",
        "Largest",
        "Average",
        "Median",
        "90th",
        "95th",
        "Std dev",
    ]))
