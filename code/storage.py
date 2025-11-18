import json
from config import PAGES

FILENAME = "last_post.json"

def load_last_posts():
    try:
        with open(FILENAME) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {page: "" for page in PAGES}

def save_last_posts(last_posts):
    with open(FILENAME, "w") as f:
        json.dump(last_posts, f, indent=4)
