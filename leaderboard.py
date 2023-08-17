import argparse

from collections import defaultdict

from reviews import get_reviews
from utils import get_closed_at, get_repos_with_bases


def get_leaderboard(repos, closed_at):
    reviews = defaultdict(int)

    for repo, base in repos:
        count_by_username = get_reviews(repo, base, closed_at)
        for username, count in count_by_username.items():
            reviews[username] += count

    return sorted(reviews.items(), key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Leaderboard")
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
    print(f"Approvals for PRs closed in the last {args.last_days} days")
    closed_at = get_closed_at(args.last_days)
    repos = get_repos_with_bases(args.repos)
    for username, score in get_leaderboard(repos, closed_at):
        print(f"{username:<20}: {score}")
