import time
from config import PAGES
from scraper import get_latest_post
from classifier import is_offer_post
from notifier import send_telegram
from storage import load_last_posts, save_last_posts

CHECK_INTERVAL = 43200  # 12 hours

def main():
    last_posts = load_last_posts()

    while True:
        for page in PAGES:
            try:
                post = get_latest_post(page)
                if not post:
                    continue

                post_id = post.get("url") or post.get("id")
                if post_id != last_posts.get(page, ""):
                    if is_offer_post(post.get("text", "")):
                        last_posts[page] = post_id
                        message = f"📢 <b>New offer post on {page}</b>\n\n{post.get('text', '')}\n\n🔗 {post.get('url')}"
                        send_telegram(message)

            except Exception as e:
                print(f"Error checking {page}: {e}")

        save_last_posts(last_posts)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
