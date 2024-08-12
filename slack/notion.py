import os

import requests
import json
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

OTHER_THUMBNAIL_URL = "https://placehold.jp/30/cbcde7/ffffff/300x150.png?text=news"


def get_ogp_image_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        og_image = soup.find('meta', property='og:image')
        if og_image:
            return og_image['content']
        else:
            return OTHER_THUMBNAIL_URL
    except Exception as e:
        print(f"OGP画像の取得中にエラーが発生しました: {e}")
    return OTHER_THUMBNAIL_URL


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

url = "https://x.com/kanpo_blog/status/1822938715599286551"

data = {
    "title": {"title": [{"text": {"content": "AI Agentの論文TOP10"}}]},
    "url": {"url": url},
    "summary": {"rich_text": [{"text": {"content": "AI論文の中身を要約したものです。"}}]},
    "thumbnail": {
        "files": [
            {
                "name": "thumbnail.jpg",
                "external": {
                    "url": get_ogp_image_url(url)
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
