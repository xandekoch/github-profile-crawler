from datetime import datetime

def build_branch_document(branch_data: dict, repo_id) -> dict:
    return {
        "name": branch_data["name"],
        "repository": repo_id,
        "protected": branch_data.get("protected", False),
        "last_commit_sha": branch_data.get("commit", {}).get("sha"),
        "crawled_at": datetime.utcnow().isoformat()
    }
