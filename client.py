import os

from github import Github

GITHUB_PAT = os.environ["GITHUB_PAT"]

client = Github(login_or_token=GITHUB_PAT)
