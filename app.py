from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('uMJNcgpAcIgbIv0/JcBC/5pF8zLsKUK5UU4JDI0goWsFoTfB31pTocPsbZN4NV4XvQul7UFAVtijq444au7MCmYCO+MpQeOlmK9hYcuSU86anbhz8N7QxNI1xJShaiq9SxvnbE4j+wu5ulaE6bo/2gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('52bd2f4c8ebc7f5d5f8106044c5249ed')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()