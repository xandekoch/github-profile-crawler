from chromadb.api.models.Collection import Collection
from typing import List

def vectorize_commits(commits: List[dict], collection: Collection):
    documents = []
    ids = []
    metadatas = []

    for commit in commits:
        sha = commit["sha"]
        message = commit["message"]
        repository = commit["repository"]
        author = commit.get("author", {})
        branches = commit.get("found_in_branches", [])

        if branches:
            branches = ', '.join(branches)

        ids.append(sha)
        documents.append(message)
        metadatas.append({
            "repository": str(repository),
            "sha": sha,
            "author_name": author.get("name"),
            "author_email": author.get("email"),
            "date": author.get("date"),
            "branches": branches,
            "crawled_at": commit.get("crawled_at")
        })

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )
