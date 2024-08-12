import os
import requests
import json
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

OTHER_THUMBNAIL_URL = "https://placehold.jp/30/cbcde7/ffffff/300x150.png?text=news"
DEFAULT_TITLE = "No Title"


def get_ogp_data(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        og_image = soup.find('meta', property='og:image')
        image_url = og_image['content'] if og_image else OTHER_THUMBNAIL_URL

        og_title = soup.find('meta', property='og:title')
        title = og_title['content'] if og_title else DEFAULT_TITLE

        return {
            'image_url': image_url,
            'title': title
        }
    except Exception as e:
        print(f"OGPデータの取得中にエラーが発生しました: {e}")
        return {
            'image_url': OTHER_THUMBNAIL_URL,
            'title': DEFAULT_TITLE
        }


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


def store(url: str):
    ogp_data = get_ogp_data(url)

    data = {
        "title": {"title": [{"text": {"content": ogp_data['title']}}]},
        "url": {"url": url},
        # "summary": {"rich_text": [{"text": {"content": ""}}]},
        "thumbnail": {
            "files": [
                {
                    "name": "thumbnail.jpg",
                    "external": {
                        "url": ogp_data['image_url']
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
