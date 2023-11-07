from collections import defaultdict

from pulls import get_pulls


def get_reviews(repo, base, closed_at):
    reviews = defaultdict(int)
    pulls = get_pulls(repo, base, closed_at)
    for pull in pulls:        
        for review in pull.get_reviews():
            if review.state != "APPROVED":
                continue
            reviews[review.user.login] += 1
    
    return reviews


def is_comment_below_threshold(comment_body):
    return len(comment_body.split(" ")) <= 5


def get_comments(repo, base, closed_at):
    comments = defaultdict(int)
    pulls = get_pulls(repo, base, closed_at)
    for pull in pulls:        
        for comment in pull.get_comments():
            if comment.in_reply_to_id:
                continue
            if pull.user.login == comment.user.login:
                continue
            if is_comment_below_threshold(comment.body):
                continue
            comments[comment.user.login] += 1
    
    return comments
