from datetime import datetime, timedelta


def get_closed_at(closed_in_last_n_days):
    return datetime.now() - timedelta(days=closed_in_last_n_days)


def get_repos_with_bases(repos):
    for repo in repos:
        yield repo.split(":")
