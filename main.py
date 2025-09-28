from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db.mongo import init_mongo
from services.github_crawler import run_github_user_crawl

app = FastAPI()
mongo_client = init_mongo()

class CrawlRequest(BaseModel):
    username: str

@app.post("/crawl")
async def crawl_user(request: CrawlRequest):
    try:
        run_github_user_crawl(request.username, mongo_client)
        return {"status": "success", "message": f"User {request.username} crawled successfully."}
    except HTTPException:
        raise
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
