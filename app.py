import os
from flask import Flask, request, abort
from datetime import datetime
from openai import OpenAI

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

app = Flask(__name__)

@app.route("/")
def home():
    return "OK"
# ⭐ 填入你的信息
CONF = Configuration(access_token='tQ6QIqD/vrMtQ6fsfGXh4SSDwKgxyzlAV5gU1ZnPo8tdywUCXwgE9M28gIia0tdewGHAUUXvIMTOyolz41fJYLXuSunD9u2EkwMsJZsaIJhZTrPz2pbh5nHocIXQT8c835JxfG2+0OJ2tsmZ8uGEYgdB04t89/1O/w1cDnyilFU=')

api_client = ApiClient(CONF)
messaging_api = MessagingApi(api_client)

handler = WebhookHandler("8866330bc54690de80d9cf3d64e3012b")

# ⭐ 填入你的 OpenAI Key
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):

    reply_text = None   # ⭐ 先定义

    try:
        user_message = event.message.text

if user_message.startswith(("翻译：", "翻译:")):
    text = user_message.replace("翻译：", "", 1).replace("翻译:", "", 1).strip()
    system_prompt = "翻译成自然日语。"
else:
    text = user_message
    system_prompt = "像朋友一样自然聊天。"

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                max_tokens=100,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ]
            )

            reply_text = response.choices[0].message.content

        except Exception as e:
            print("OpenAI error:", e)
            reply_text = "AI有点慢，请再发一次 🙏"

    except Exception as e:
        print("整体错误:", e)
        reply_text = "系统错误，请稍后再试"

    # ⭐ 终极保险
    if not reply_text:
        reply_text = "系统异常，请稍后再试"

    messaging_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=reply_text)]
        )
    )




    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)












