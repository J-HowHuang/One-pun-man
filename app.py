from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

from one_pun import handleMessage

import json
import os
from time import time

app = Flask(__name__)

if os.path.isfile('config.json'):
    config_file = open('config.json')
    config = json.load(config_file)
else:
    config = os.environ


access_token = config['channel_access_token']
secret = config['channel_secret']

line_bot_api = LineBotApi(access_token)
handler = WebhookHandler(secret)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def respond_pun(event):
    pun_start=time()
    responseMessage = handleMessage(event.message.text)
    pun_end=time()
    if responseMessage != "pun not found":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=responseMessage)
        )
    send_end=time()
    print("pun finding: %.3f s, sending: %.3f s" % (pun_end-pun_start, send_end-pun_end))


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)