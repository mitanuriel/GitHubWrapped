"""
Helper functions for interacting with GitHub API
"""
import requests
import time
from config import HEADERS, SINCE_DATE


def fetch_org_repos(org_name):
    """Fetch all repositories for an organization."""
    url = f"https://api.github.com/orgs/{org_name}/repos"
    params = {"per_page": 100}
    repos = []
    while url:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        repos.extend(response.json())
        url = response.links.get("next", {}).get("url")  # Handle pagination
    return repos


def fetch_comments(repo, endpoint):
    """Fetch comments for a given repository and endpoint."""
    url = f"https://api.github.com/repos/{repo}/{endpoint}"
    params = {"since": SINCE_DATE, "per_page": 100}
    comments = []
    while url:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        comments.extend(response.json())
        url = response.links.get("next", {}).get("url")  # Handle pagination
    return comments


def fetch_comments_url(url):
    """Fetch comments or commits from a given url."""
    params = {"since": SINCE_DATE, "per_page": 100}
    comments = []
    while url:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        comments.extend(response.json())
        url = response.links.get("next", {}).get("url")  # Handle pagination
    return comments


def fetch_prs(repo):
    """Fetch pull requests for a repository."""
    url = f"https://api.github.com/repos/{repo}/pulls"
    params = {"state": "all", "since": SINCE_DATE,
              "sort": "created", "direction": "desc", "per_page": 100}
    prs = []
    while url:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        response_prs = response.json()
        prs.extend(response_prs)
        if len(response_prs) > 0 and response_prs[-1]["created_at"] < SINCE_DATE:
            break
        url = response.links.get("next", {}).get("url")  # Handle pagination
    return prs


def filter_prs_by_date(prs):
    """Filter pull requests created after starting date."""
    return [pr for pr in prs if pr["created_at"] >= SINCE_DATE]


def filter_prs_by_collaboarators(prs, team_members):
    """Filter pull requests by team members."""
    return [pr for pr in prs if pr["user"]["login"] in team_members]


def get_commit_details(repo, commit_sha):
    """Fetch commit details."""
    commit_url = f"https://api.github.com/repos/{repo}/commits/{commit_sha}"
    response = requests.get(commit_url, headers=HEADERS)
    return response.json()


def get_gh_repo_commit_stats(repo):
    """Returns the last year of commit activity grouped by week.
       This implementation fixes a bug with Github API returning empty list 
       for data that has not been cached yet."""
    stats_url_ui = f"https://github.com/{repo}/graphs/code-frequency"
    stats_url_api = f"https://api.github.com/repos/{repo}/stats/code-frequency"
    _ = requests.get(stats_url_ui, headers=HEADERS)
    time.sleep(1)

    stats = {}
    while len(stats) == 0:
        response = requests.get(stats_url_api, headers=HEADERS)
        stats = response.json()
        time.sleep(1)
    return stats
