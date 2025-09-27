from services.github_crawler import run_github_user_crawl
from db.mongo import init_mongo

if __name__ == "__main__":
    mongo_client = init_mongo()
    run_github_user_crawl("xandekoch", mongo_client)
