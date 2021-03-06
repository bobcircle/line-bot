# flask django 用來做網頁
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('DsydDmpWpRaqp9+liQBc2WP5Ov+3x/zlvpKhQ9oII5NBKTsUgXoXYN1yGh34iabFtnoP5PtY1xggWVAhMWAlDq5VxMfWCFiulPE7C3VD4dm23B+ijCkw5FHQHR1PhbxCOWwFDM3mL0yeh8hJzYPfZgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('8d4d91c577bb41d3e2073000ddf7df6c')


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
    msg = event.message.text
    reply_message = ''
    sticker = False
    if msg in ['hi', 'Hi']:
        reply_message = '嗨'
    elif msg == '你是誰':
        reply_message = '我是機器人'
    else:
        reply_message = '我暫時還不知道如何回應'
        sticker = True
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message))
    if sticker:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
)


if __name__ == "__main__":
    app.run()