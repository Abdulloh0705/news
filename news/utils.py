import requests

TOKEN_BOT = "7722985768:AAGaW6FxkuiY7TtExu3F4lMQjwDgB-_QZu4"
CHAT_ID = "-1003935829416"


def send_to_telegram(news):
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendPhoto"

    caption = f"""
📰 <b>{news.title}</b>

{news.content[:100]}

👉 Batafsil: http://127.0.0.1:8000/news/{news.slug}/
"""

    data = {
        "chat_id": CHAT_ID,
        "caption": caption,
        "parse_mode": "HTML"
    }

    files = {}
    if news.image:
        files["photo"] = news.image.open()

    requests.post(url, data=data, files=files)