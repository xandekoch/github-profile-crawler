from typing import List
from bson import ObjectId
from datetime import datetime

def build_commit_document(commit_data: dict, repository: ObjectId) -> dict:
    return {
        "sha": commit_data["sha"],
        "message": commit_data["commit"]["message"],
        "author": {
            "name": commit_data["commit"]["author"].get("name"),
            "email": commit_data["commit"]["author"].get("email"),
            "date": commit_data["commit"]["author"].get("date")
        },
        "committer": {
            "name": commit_data["commit"]["committer"].get("name"),
            "email": commit_data["commit"]["committer"].get("email"),
            "date": commit_data["commit"]["committer"].get("date")
        },
        "url": commit_data.get("html_url"),
        "repository": repository,
        "tree_sha": commit_data["commit"]["tree"]["sha"],
        "parents": [
            {
                "sha": p["sha"],
                "url": p.get("html_url")
            } for p in commit_data.get("parents", [])
        ],
        "found_in_branches": commit_data.get("found_in_branches", []),
        "verified": commit_data["commit"]["verification"].get("verified", False),
        "verification_reason": commit_data["commit"]["verification"].get("reason", None),
        "created_at": commit_data["commit"]["author"].get("date"),
        "crawled_at": datetime.utcnow().isoformat()
    }
