import argparse
import numpy

from operator import itemgetter

from tabulate import tabulate

from pulls import (
    get_pulls,
    get_size,
    get_time_open,
)
from utils import (
    get_closed_at,
    get_repos_with_bases,
)


def get_times_by_size(repos, closed_at):
    pull_stats = []
    for repo, base in repos:
        pulls = get_pulls(repo, base, closed_at)
        for pull in pulls:
            if not pull.is_merged():
                continue
            pull_stats.append((
                get_size(pull),
                get_time_open(pull),
            ))

    pull_stats = sorted(
        pull_stats,
        key=itemgetter(0),
    )
    boundaries = numpy.percentile(
        [size for size, _ in pull_stats],
        numpy.arange(0, 101, 10),
    )
    bins = [[] for _ in range(11)]
    for size, time_open in pull_stats:
        for bin_index, boundary in enumerate(boundaries):
            if size <= boundary:
                bins[bin_index].append(time_open)
                break
    
    averages = []
    for boundary_index, bin in enumerate(bins):
        averages.append((
            boundaries[boundary_index],
            numpy.average(bin),
            len(bin),
        ))

    return averages


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
    averages = get_times_by_size(repos, closed_at)

    print(tabulate(
        averages,
        headers=["Size", "Average time to close", "No. of pulls", "Sizes"],
    ))
