import requests
import base64
import json
import os
from datetime import datetime

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
USERNAME = os.environ.get("GITHUB_USERNAME")
REPO = os.environ.get("GITHUB_REPO")

def push_chat_to_github(user_msg, ai_msg):
    filename = f"logs/{datetime.now().strftime('%Y-%m-%d')}.json"
    api_url = f"https://api.github.com/repos/{USERNAME}/{REPO}/contents/{filename}"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # گرفتن فایل قبلی
    r = requests.get(api_url, headers=headers)
    if r.status_code == 200:
        old_content = json.loads(
            base64.b64decode(r.json()["content"]).decode("utf-8")
        )
        sha = r.json()["sha"]
    else:
        old_content = []
        sha = None

    old_content.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "user_message": user_msg,
        "ai_message": ai_msg
    })

    new_content = base64.b64encode(
        json.dumps(old_content, ensure_ascii=False, indent=2).encode("utf-8")
    ).decode("utf-8")

    payload = {
        "message": "new chat log",
        "content": new_content
    }

    if sha:
        payload["sha"] = sha

    requests.put(api_url, headers=headers, json=payload)
