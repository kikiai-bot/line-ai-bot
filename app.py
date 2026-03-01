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

    user_message = event.message.text   # ← 必须先有这一行

    if user_message.startswith("翻译："):
        text = user_message.replace("翻译：", "")

        reply_text = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "把用户输入翻译成自然的日语，只返回翻译结果。"},
                {"role": "user", "content": text}
            ]
        ).choices[0].message.content

    else:
        reply_text = client_ai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是在日本生活的中国朋友，说话自然、有亲和力，像真人聊天一样。"},
                {"role": "user", "content": user_message}
            ]
        ).choices[0].message.content

    messaging_api.reply_message(
    ReplyMessageRequest(
        reply_token=event.reply_token,
        messages=[TextMessage(text=reply_text)]
    )
)


    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)



