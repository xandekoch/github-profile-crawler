from datetime import datetime

def build_branch_document(branch_data: dict, repository) -> dict:
    return {
        "name": branch_data["name"],
        "repository": repository,
        "protected": branch_data.get("protected", False),
        "last_commit_sha": branch_data.get("commit", {}).get("sha"),
        "crawled_at": datetime.utcnow().isoformat()
    }
