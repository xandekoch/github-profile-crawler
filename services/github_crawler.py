import json
import requests
from fastapi import HTTPException
from services.github_api import fetch_user_profile, fetch_user_repos, fetch_repo_branches, fetch_branch_commits
from models.user import build_user_document
from models.repo import build_repo_document
from models.branch import build_branch_document
from models.commit import build_commit_document


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def run_github_user_crawl(username: str, mongo_client):
    db = mongo_client["github_crawler"]
    users_col = db["users"]
    repos_col = db["repos"]
    branches_col = db["branches"]
    commits_col = db["commits"]

    existing_user = users_col.find_one({"login": username})
    if existing_user:
        print(f"🔁 User {username} already exists. Calling update_user()...")
        return update_user(existing_user, mongo_client)

    print(f"🚀 Starting crawl for {username}")

    try:
        user_data = fetch_user_profile(username)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=400, detail=f"GitHub user '{username}' not found.")
        else:
            print(e.response.text)
            raise HTTPException(status_code=500, detail="GitHub API error during user fetch.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    repos = fetch_user_repos(username)
    if not repos:
        raise HTTPException(status_code=400, detail=f"GitHub user '{username}' has no public repositories.")

    try:
        with mongo_client.start_session() as session:
            with session.start_transaction():
                user_doc = build_user_document(user_data)

                user_id = users_col.insert_one(user_doc, session=session).inserted_id

                for repo in repos:
                    repo_doc = build_repo_document(repo, user_id)
                    repo_id = repos_col.insert_one(repo_doc, session=session).inserted_id
                    repo_name = repo["name"]

                    branches = fetch_repo_branches(username, repo_name)
                    branch_docs = [build_branch_document(b, repo_id) for b in branches]
                    if branch_docs:
                        branches_col.insert_many(branch_docs, session=session)

                    unique_commits = {}
                    for branch in branches:
                        branch_name = branch["name"]
                        commits = fetch_branch_commits(username, repo_name, branch_name)
                        for commit in commits:
                            sha = commit["sha"]
                            if sha not in unique_commits:
                                commit["found_in_branches"] = [branch_name]
                                unique_commits[sha] = commit
                            else:
                                if branch_name not in unique_commits[sha]["found_in_branches"]:
                                    unique_commits[sha]["found_in_branches"].append(branch_name)

                    commit_docs = [build_commit_document(c, repo_id) for c in unique_commits.values()]
                    if commit_docs:
                        commits_col.insert_many(commit_docs, session=session)

        print("✅ Crawl and transaction committed successfully.")

    except Exception as e:
        raise RuntimeError(f"Transaction failed: {e}")

def update_user(user_doc, mongo_client):
    # To-Do: get Delta and insert in DB
    pass
