import os

import requests
import json
from dotenv import load_dotenv

load_dotenv()


def insert_notion_record(database_id, api_key, data):
    url = f"https://api.notion.com/v1/pages"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    payload = {
        "parent": {"database_id": database_id},
        "properties": data
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        print("レコードが正常に挿入されました。")
        return response.json()
    else:
        print(f"エラーが発生しました。ステータスコード: {response.status_code}")
        print(response.text)
        return None


# 使用例

data = {
    "title": {"title": [{"text": {"content": "AI Agentの論文TOP10"}}]},
    "url": {"url": "https://deepgram.com/learn/top-arxiv-papers-about-ai-agents"},
    "summary": {"rich_text": [{"text": {"content": "AI論文の中身を要約したものです。"}}]},
    "thumbnail": {
        "files": [
            {
                "name": "thumbnail.jpg",
                "external": {
                    "url": "https://img2.lancers.jp/portfolio/580888/2943702/d6b298fe22d17b1dcd6f0f52c6a88eeae39f74b6e22d807a7b9a434ff0187a5e/31399748_1000_0.jpg"
                }
            }
        ]
    }
}

result = insert_notion_record(
    os.getenv("NOTION_DATABASE_ID"),
    os.getenv("NOTION_API_KEY"),
    data,
)
