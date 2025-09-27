def build_user_document(user_data: dict) -> dict:
    return {
        "external_id": user_data["id"],
        "login": user_data["login"],
        "html_url": user_data["html_url"],
        "avatar_url": user_data["avatar_url"],
        "type": user_data["type"],
    }
