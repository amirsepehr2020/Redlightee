import requests
import base64
import json
import os
import hashlib
from datetime import datetime

# ===============================
# ENV VARIABLES (از Render)
# ===============================
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
USERNAME = os.environ.get("GITHUB_USERNAME")
REPO = os.environ.get("GITHUB_REPO")

# ===============================
# کمک‌کننده: هش کردن IP
# ===============================
def hash_ip(ip):
    if not ip:
        return None
    return hashlib.sha256(ip.encode("utf-8")).hexdigest()

# ===============================
# لاگ کردن چت در GitHub
# ===============================
def push_chat_to_github(user_msg, ai_msg, meta=None):
    """
    user_msg : پیام کاربر
    ai_msg   : پاسخ هوش مصنوعی
    meta     : اطلاعات اضافی کاربر (dict)
    """

    if not GITHUB_TOKEN or not USERNAME or not REPO:
        print("❌ GitHub ENV vars missing")
        print(GITHUB_TOKEN, USERNAME, REPO)
        return

    if meta is None:
        meta = {}

    # اسم فایل لاگ روزانه
    filename = f"logs/{datetime.now().strftime('%Y-%m-%d')}.json"
    api_url = f"https://api.github.com/repos/{USERNAME}/{REPO}/contents/{filename}"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    print("📡 GitHub API:", api_url)

    # ===============================
    # گرفتن فایل قبلی (اگه وجود داشت)
    # ===============================
    r = requests.get(api_url, headers=headers)
    print("🔍 GET status:", r.status_code)

    if r.status_code == 200:
        old_content = json.loads(
            base64.b64decode(r.json()["content"]).decode("utf-8")
        )
        sha = r.json()["sha"]
    else:
        old_content = []
        sha = None

    # ===============================
    # ساخت لاگ جدید
    # ===============================
    log_entry = {
        "time": datetime.now().isoformat(),
        "session_id": meta.get("session_id"),
        "platform": meta.get("platform"),
        "language": meta.get("language"),
        "user_agent": meta.get("user_agent"),
        "model": meta.get("model"),
        "ip_hash": hash_ip(meta.get("ip")),
        "user": {
            "message": user_msg,
            "length": len(user_msg)
        },
        "ai": {
            "message": ai_msg,
            "length": len(ai_msg)
        }
    }

    old_content.append(log_entry)

    # ===============================
    # تبدیل به base64 برای GitHub
    # ===============================
    new_content = base64.b64encode(
        json.dumps(old_content, ensure_ascii=False, indent=2).encode("utf-8")
    ).decode("utf-8")

    payload = {
        "message": "new chat log",
        "content": new_content
    }

    if sha:
        payload["sha"] = sha

    # ===============================
    # ارسال به GitHub
    # ===============================
    res = requests.put(api_url, headers=headers, json=payload)

    print("🚀 PUT status:", res.status_code)
    print("📨 Response:", res.text)
