import argparse

from collections import defaultdict

from tabulate import tabulate

from reviews import get_comments, get_reviews
from utils import get_closed_at, get_repos_with_bases


def get_quality(repos, closed_at):
    totals = defaultdict(lambda: {"reviews": 0, "comments": 0})

    for repo, base in repos:
        review_count_by_username = get_reviews(repo, base, closed_at)
        for username, count in review_count_by_username.items():
            totals[username]["reviews"] += count
        
        comment_count_by_username = get_comments(repo, base, closed_at)
        for username, count in comment_count_by_username.items():
            totals[username]["comments"] += count

    averages = []
    for username, total in totals.items():
        if total["reviews"] == 0:
            continue
        averages.append((
            username, 
            total["comments"],
            total["reviews"],
            total["comments"] / total["reviews"],
        ))

    return sorted(averages, key=lambda x: x[1], reverse=True)


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
    print(f"Average comments per review for PRs closed in the last {args.last_days} days")
    closed_at = get_closed_at(args.last_days)
    repos = get_repos_with_bases(args.repos)
    quality = get_quality(repos, closed_at)
    print(tabulate(quality, headers=["Username", "Comments", "Reviews", "Comments per review"]))
