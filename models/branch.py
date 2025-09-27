def build_branch_document(branch_data: dict, repo_id) -> dict:
    return {
        "name": branch_data["name"],
        "commit_sha": branch_data["commit"]["sha"],
        "protected": branch_data.get("protected", False),
        "repository_id": repo_id,
    }
