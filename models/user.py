from datetime import datetime

def build_user_document(user_data: dict) -> dict:
    return {
        "external_id": user_data["id"],
        "login": user_data["login"],
        "name": user_data.get("name"),
        "bio": user_data.get("bio"),
        "company": user_data.get("company"),
        "location": user_data.get("location"),
        "blog": user_data.get("blog"),
        "twitter_username": user_data.get("twitter_username"),
        "avatar_url": user_data.get("avatar_url"),
        "html_url": user_data.get("html_url"),
        "type": user_data.get("type"),  # User or Organization
        "public_repos": user_data.get("public_repos", 0),
        "public_gists": user_data.get("public_gists", 0),
        "followers": user_data.get("followers", 0),
        "following": user_data.get("following", 0),
        "site_admin": user_data.get("site_admin", False),
        "created_at": user_data.get("created_at"),
        "updated_at": user_data.get("updated_at"),
        "crawled_at": datetime.utcnow().isoformat()
    }