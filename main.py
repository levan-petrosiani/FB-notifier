import json
import requests
import time

CONFIG = json.load(open("config.json"))
LAST = json.load(open("last_post.json"))

APIFY_TOKEN = CONFIG["apify_token"]
PAGE_URL = CONFIG["facebook_page_url"]
TELEGRAM_TOKEN = CONFIG["telegram_token"]
CHAT_ID = CONFIG["telegram_chat_id"]

def get_latest_post():
    """Fetch latest post from Apify Facebook Page Scraper"""
    actor_url = "https://api.apify.com/v2/acts/apify~facebook-pages-scraper/run-sync-get-dataset-items"
    params = {
        "token": APIFY_TOKEN,
        "pageUrls": [PAGE_URL],
        "resultsLimit": 1
    }
    response = requests.post(actor_url, json=params)
    response.raise_for_status()
    data = response.json()
    if not data:
        return None
    return data[0]

def send_telegram(message):
    """Send message to Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, data=payload)

def main():
    while True:
        try:
            post = get_latest_post()
            if not post:
                print("No posts found.")
                time.sleep(600)
                continue

            latest_id = post.get("url") or post.get("id")

            if latest_id != LAST["id"]:
                message = f"📢 <b>New Facebook Post</b>\n\n{post.get('text', '')}\n\n🔗 {post.get('url')}"
                send_telegram(message)
                LAST["id"] = latest_id
                json.dump(LAST, open("last_post.json", "w"))
                print("✅ New post detected and notified!")
            else:
                print("No new posts yet.")

        except Exception as e:
            print("Error:", e)

        time.sleep(600)  # check every 10 minutes

if __name__ == "__main__":
    main()
