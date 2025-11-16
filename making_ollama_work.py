from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)

tests = [
    """ონლაინ შოპინგის დღე 𝐓𝐇𝐄 𝐁𝐎𝐃𝐘 𝐒𝐇𝐎𝐏-ში🌐
        მხოლოდ 11 ნოემბერს, ისარგებლე -𝟓𝟎% ფასდაკლებით სრულ ასორტიმენტზე და -𝟑𝟎% სპა ხაზზე🤎
        ✨ ვებ გვერდიდან გამოწერა შესაძლებელია:  10:00-დან-21:30-მდე:""",

    """გაიცანი ჩვენი ახალი, ლიმიტირებული კარამელის ხაზი✨  ეს არის ტკბილი, 
        სადღესასწაულო სურნელი, რომელიც აუცილებლად შეგაყვარებს თავს🪄
        🫶გაგვიზიარე, რომელია შენი საყვარელი პროდუქტი?""",

    """ზამთარის ლიმიტირებული ხაზები უკვე 𝐓𝐇𝐄 𝐁𝐎𝐃𝐘 𝐒𝐇𝐎𝐏-შია✨
        🤎 კარამელი – ტკბილი და თბილი;
        ❤ მოცხარი – ხალისიანი და ცოცხალი;
        💜ქლიავი – ნაზი და დახვეწილი;
        💛 ეწვიე ჩვენს ფილიალებს და აღმოაჩინე შენი ზამთრის ფავორიტები!"""
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

for test in tests:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": test}
    ]
    print(llm.invoke(messages).content)
