````markdown
# FB-notifier

Automatically checks selected Facebook pages for **promotion / discount** posts written in Georgian and sends notifications to a Telegram chat.

This tool is useful if you want to track sales campaigns from specific brands without manually refreshing Facebook.

---

## How It Works

1. **Scrapes** the latest post from each configured Facebook page using **Apify**
2. **Classifies** the post text using a local LLM (**Ollama / Llama 3.2**)  
   - If the model judges the content to be a promotion offer → proceed
3. **Checks** whether this post is new (tracked via `last_post.json`)
4. **Sends** the post text and link to a Telegram channel/chat
5. **Stores** the latest processed post and repeats on schedule

Only posts including discounts, sales, promotions, giveaways, etc. are sent.

---

## Requirements

- Python 3.9+
- Ollama installed locally (model: `llama3.2`)
- Apify account + API token
- Telegram bot token + chat ID

Dependencies are defined in `environment.yml`.

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/levan-petrosiani/FB-notifier.git
cd FB-notifier
```

### 2. Create environment

```bash
conda env create -f environment.yml
conda activate fb-notifier
```

Or use your own venv and install dependencies manually.

### 3. Install and run Ollama model

```bash
ollama pull llama3.2
```

### 4. Configure environment variables

Create `.env` file in the project root:

```
APIFY_TOKEN=your_apify_api_token
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### 5. Configure page list (optional)

Modify `PAGES` in `config.py` to add/remove Facebook pages:

```python
PAGES = [
    "https://www.facebook.com/TheBodyShopGeo",
    "https://www.facebook.com/YvesRocherGeorgia",
]
```

---

## Run

```bash
python main.py
```

The script will run indefinitely and check pages every interval.

Default check interval:

```python
CHECK_INTERVAL = 43200  # currently mislabeled; this equals 12 hours
```

Adjust the value if you want faster monitoring.

---

## Classification Logic

The model receives `SYSTEM_PROMPT` defined in `config.py`.
Response must be **strictly `YES` or `NO`**.

Discount-related keywords and synonyms in Georgian are recognized, such as:
ფასდაკლება, აქცია, შეთავაზება, ბონუსი, 1+1, საჩუქარი, %-იანი ფასდაკლება, უფასოდ, ქეშბექი, ვაუჩერი, სუპერ ფასი, etc.

Only posts classified as offers trigger notifications.

---

## Notification Delivery

Messages are posted to Telegram using Bot API:

Example message:

```
📢 New offer post on <Facebook Page URL>

<Post text content>

🔗 <Post URL>
```

HTML formatting supported.

---

## Data Storage

`storage.py` tracks latest processed post per page:

```
last_post.json:
{
    "https://www.facebook.com/Page": "<last_post_id>"
}
```

Safe to delete if you want to reprocess posts.

---

## File Overview

```
classifier.py     # LLM-based offer detection
scraper.py        # Facebook scraping via Apify
notifier.py       # Telegram messaging
storage.py        # State persistence
main.py           # Execution loop
config.py         # Environment + settings
last_post.json    # Auto-generated store of processed posts
```

---

## Notes / Caveats

* Apify scraping depends on Facebook layout; breakage is always possible
* Ollama must run locally and remain available while script runs
* Telegram messages may fail silently if tokens/IDs are wrong
* This is not a high-volume scraper; personal monitoring use case only

---

## License

პროექტი ვრცელდება MIT ლიცენზიით.MIT License.


