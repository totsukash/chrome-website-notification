from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import slack
import notion

load_dotenv(verbose=True)
app = FastAPI()


@app.on_event("startup")
async def startup():
    """アプリの起動時の処理"""
    pass


@app.get("/healthcheck")
def healthcheck():
    return "OK"


class ArticlesReq(BaseModel):
    channel_id: str
    url: str
    user_id: str | None = None


@app.post("/articles")
async def retrieve_articles(req: ArticlesReq):
    # Notionに保存
    notion.store(req.url)

    # Slackに送信
    slack.post(
        channel_id=req.channel_id,
        message=req.url,
        user_id=req.user_id
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
