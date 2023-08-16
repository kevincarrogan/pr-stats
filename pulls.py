from client import client


def get_pulls(repo, base, closed_at):
    pulls = client.get_repo(repo).get_pulls(base=base, state="closed")
    for pull in pulls:
        if pull.closed_at <= closed_at:
            break
        yield pull
