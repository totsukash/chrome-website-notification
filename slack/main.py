import os
from fastapi import FastAPI, Request, HTTPException
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv(verbose=True)
app = FastAPI()

# Slack WebClientの初期化
slack_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

# Slackにメッセージを送信するチャンネルID
SLACK_CHANNEL = "C011AR9LM7H"


class SlackMessage(BaseModel):
    message: str


@app.get("/healthcheck")
def healthcheck():
    return "OK"


@app.post("/slack/post")
async def slack_post(slack_message: SlackMessage):
    """Slackにメッセージを送信するエンドポイント"""
    try:
        response = slack_client.chat_postMessage(
            channel=SLACK_CHANNEL,
            text=slack_message.message
        )
        return {
            "status": "success",
            "message": "Message sent to Slack",
        }
    except SlackApiError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send message to Slack: {str(e)}",
        )


# FastAPIのイベントハンドラ
@app.on_event("startup")
async def startup():
    """アプリの起動時の処理"""
    if not os.environ.get("SLACK_BOT_TOKEN"):
        raise ValueError("SLACK_BOT_TOKEN must be set in the environment variables")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
