def build_commit_document(commit_data: dict, repo_id) -> dict:
    return {
        "sha": commit_data["sha"],
        "message": commit_data["commit"]["message"],
        "author": {
            "name": commit_data["commit"]["author"]["name"],
            "email": commit_data["commit"]["author"]["email"],
            "date": commit_data["commit"]["author"]["date"]
        },
        "found_in_branches": commit_data.get("found_in_branches", []),
        "repository_id": repo_id,
    }
