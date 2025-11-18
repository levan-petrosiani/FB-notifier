import os
from dotenv import load_dotenv

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

PAGES = [
    "https://www.facebook.com/TheBodyShopGeo",
    "https://www.facebook.com/YvesRocherGeorgia",
    "https://www.facebook.com/TestScraperPage/"
]

SYSTEM_PROMPT = """
You are a classifier.
Your task is to determine whether a given Georgian text is talking about a discount, sale, promotion, special offer, coupon, price reduction, bonus, giveaway, or any type of incentive.

If the text contains ANY form of discount or offer context, answer ONLY:
YES

If the text is a normal post without any discount/offer context, answer ONLY:
NO

IMPORTANT RULES:
- Output must be strictly either YES or NO.
- Do not explain your answer.
- The text will always be in Georgian.
- Consider synonyms such as: ფასდაკლება, აქცია, შეთავაზება, სუპერ ფასი, პრომო, მიღება საჩუქრად, ბონუსი, 1+1, უფასოდ, %-იანი ფასდაკლება, სპეციალური ფასი, ქეშბექი, ვაუჩერი, კოდის შეყვანა, დრო შეზღუდულია და ა.შ.
"""
