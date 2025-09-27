import requests
from typing import List, Dict

GITHUB_API_BASE = "https://api.github.com"
HEADERS = {"Accept": "application/vnd.github.v3+json"}

def fetch_user_profile(username: str) -> dict:
    url = f"{GITHUB_API_BASE}/users/{username}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def fetch_user_repos(username: str) -> List[Dict]:
    url = f"{GITHUB_API_BASE}/users/{username}/repos?per_page=100"
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    return res.json()

def fetch_repo_branches(owner: str, repo: str) -> List[Dict]:
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/branches"
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    return res.json()

def fetch_branch_commits(owner: str, repo: str, branch: str) -> List[Dict]:
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/commits?sha={branch}&per_page=100"
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    return res.json()
