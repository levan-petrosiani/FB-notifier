import json
import time
import os
import requests
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# List of Facebook pages to monitor
PAGES = [
    "https://www.facebook.com/TheBodyShopGeo",
    "https://www.facebook.com/YvesRocherGeorgia",
]

# Load last post info safely
if os.path.exists("last_post.json"):
    try:
        with open("last_post.json") as f:
            LAST = json.load(f)
    except json.JSONDecodeError:
        # File is empty or invalid, initialize
        LAST = {page: "" for page in PAGES}
else:
    LAST = {page: "" for page in PAGES}

# Make sure file exists and has valid JSON
with open("last_post.json", "w") as f:
    json.dump(LAST, f, indent=4)



client = ApifyClient(APIFY_TOKEN)

def get_latest_post(page_url):
    """Fetch latest post from Apify Facebook Page Scraper"""
    actor = client.actor("apify/facebook-pages-scraper")
    run = actor.call(run_input={
        "pageUrls": [page_url],
        "resultsLimit": 1
    })
    dataset_items = list(client.dataset(run["defaultDatasetId"]).list_items().items)
    if not dataset_items:
        return None
    return dataset_items[0]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, data=payload)

def main():
    global LAST
    while True:
        for page in PAGES:
            try:
                post = get_latest_post(page)
                if not post:
                    print(f"No posts found for {page}.")
                    continue

                latest_id = post.get("url") or post.get("id")
                if latest_id != LAST.get(page, ""):
                    LAST[page] = latest_id
                    message = f"📢 <b>New post on {page}</b>\n\n{post.get('text', '')}\n\n🔗 {post.get('url')}"
                    send_telegram(message)

            except Exception as e:
                print(f"Error checking {page}: {e}")

        # Write once after checking all pages
        with open("last_post.json", "w") as f:
            json.dump(LAST, f, indent=4)

        time.sleep(600)  # check every 10 minutes


if __name__ == "__main__":
    main()
