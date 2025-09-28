from datetime import datetime

def build_branch_document(branch_data: dict, repository, user_id) -> dict:
    return {
        "name": branch_data["name"],
        "owner_id": user_id,
        "repository": repository,
        "protected": branch_data.get("protected", False),
        "last_commit_sha": branch_data.get("commit", {}).get("sha"),
        "crawled_at": datetime.utcnow().isoformat()
    }
