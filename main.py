import json
import time
import os
import requests
from dotenv import load_dotenv
from apify_client import ApifyClient

# Load .env
load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
PAGE_URL = os.getenv("PAGE_URL")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

LAST = json.load(open("last_post.json"))

# Initialize the Apify client
client = ApifyClient(APIFY_TOKEN)

def get_latest_post():
    """Fetch latest post from Apify Facebook Page Scraper"""
    actor = client.actor("apify/facebook-pages-scraper")
    run = actor.call(run_input={
        "pageUrls": [PAGE_URL],
        "resultsLimit": 1
    })

    # Get dataset items
    dataset_items = list(client.dataset(run["defaultDatasetId"]).list_items().items)
    if not dataset_items:
        return None
    return dataset_items[0]

def send_telegram(message):
    """Send message to Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, data=payload)

def main():

    print("Testing Apify connection...")
    client.user().get()
    print("✅ Connected to Apify successfully")

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
