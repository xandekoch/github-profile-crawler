import os
import json
from services.github_api import fetch_user_repos, fetch_repo_branches, fetch_branch_commits
from models.user import build_user_document
from models.repo import build_repo_document
from models.branch import build_branch_document
from models.commit import build_commit_document

DATA_DIR = "github_data"
os.makedirs(DATA_DIR, exist_ok=True)

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def run_github_user_crawl(username: str, mongo_client):
    db = mongo_client["github_ai"]
    users_col = db["users"]
    repos_col = db["repos"]
    branches_col = db["branches"]
    commits_col = db["commits"]

    existing_user = users_col.find_one({"login": username})
    if existing_user:
        print(f"🔁 Usuário {username} já existe. Chamando update_user()...")
        return update_user(existing_user, mongo_client)

    print(f"🚀 Iniciando crawler para {username}")
    repos = fetch_user_repos(username)
    if not repos:
        print("⚠️ Nenhum repositório encontrado.")
        return

    owner_data = repos[0]["owner"]
    user_doc = build_user_document(owner_data)
    user_id = users_col.insert_one(user_doc).inserted_id

    save_json(repos, os.path.join(DATA_DIR, "repos.json"))

    for repo in repos:
        repo_doc = build_repo_document(repo, user_id)
        repo_id = repos_col.insert_one(repo_doc).inserted_id
        repo_name = repo["name"]

        try:
            branches = fetch_repo_branches(username, repo_name)
            branch_docs = [build_branch_document(b, repo_id) for b in branches]
            if branch_docs:
                branches_col.insert_many(branch_docs)
            save_json(branches, os.path.join(DATA_DIR, f"{repo_name}_branches.json"))

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
                commits_col.insert_many(commit_docs)
            save_json(commit_docs, os.path.join(DATA_DIR, f"{repo_name}_commits.json"))

        except Exception as e:
            print(f"❌ Erro ao processar {repo_name}: {e}")

    print("✅ Crawl finalizado.")

def update_user(user_doc, mongo_client):
    # To-Do: get Delta and insert in DB
    pass
