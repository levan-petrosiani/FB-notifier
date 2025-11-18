from apify_client import ApifyClient
from config import APIFY_TOKEN

client = ApifyClient(APIFY_TOKEN)

def get_latest_post(page_url):
    actor = client.actor("apify/facebook-posts-scraper")
    run = actor.call(run_input={
        "startUrls": [{"url": page_url}],
        "resultsLimit": 1
    })
    dataset_items = list(client.dataset(run["defaultDatasetId"]).list_items().items)
    return dataset_items[0] if dataset_items else None
