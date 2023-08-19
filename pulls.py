from client import client


def get_pulls(repo, base, closed_at):
    pulls = client.get_repo(repo).get_pulls(base=base, state="closed")
    for pull in pulls:
        if pull.closed_at <= closed_at:
            break
        yield pull


def get_size(pull):
    return pull.additions + pull.deletions


def delta_to_days(delta):
    return delta.total_seconds() / 60 / 60 / 24


def get_time_open(pull):
    delta = pull.closed_at - pull.created_at
    days = delta_to_days(delta)
    return days
