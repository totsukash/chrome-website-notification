import os

from dotenv import load_dotenv
from fastapi import HTTPException
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()
slack_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))


def post(
    channel_id: str,
    message: str,
    user_id: str | None = None,
):
    """Notionに保存&Slackにメッセージを送信するエンドポイント"""
    try:
        msg = message
        if user_id:
            msg = f"{message} [from:<@{user_id}>]"

        response = slack_client.chat_postMessage(
            channel=channel_id,
            text=msg
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
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}",
        )
