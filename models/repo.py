def build_repo_document(repo_data: dict, user_id) -> dict:
    return {
        "external_id": repo_data["id"],
        "name": repo_data["name"],
        "full_name": repo_data["full_name"],
        "description": repo_data.get("description"),
        "html_url": repo_data["html_url"],
        "language": repo_data.get("language"),
        "default_branch": repo_data["default_branch"],
        "created_at": repo_data["created_at"],
        "updated_at": repo_data["updated_at"],
        "pushed_at": repo_data["pushed_at"],
        "stargazers_count": repo_data["stargazers_count"],
        "watchers_count": repo_data["watchers_count"],
        "forks_count": repo_data["forks_count"],
        "open_issues_count": repo_data["open_issues_count"],
        "owner_id": user_id,
    }
