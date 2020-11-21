from flask import Flask, request, abort
import json
import re
import csv

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

app = Flask(__name__)

config_file = open('config.json')
config = json.load(config_file)

access_token = config['channel_access_token']
secret = config['channel_secret']

line_bot_api = LineBotApi(access_token)
handler = WebhookHandler(secret)

import datetime 
import random


flatten = lambda t: [item for sublist in t for item in sublist]


def find_chinese(file):
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    msg = re.sub(pattern, '', file)
    return msg


def handleMessage(msg):
    msg = find_chinese(msg)
    keywords = parseMessage(msg)
    puns = []
    for keyword in keywords:
        puns.append(findPun(keyword))
    puns = flatten(puns)
    if len(puns):
        return randomlyChoose(puns)
    else:
        return "pun not found"


def parseMessage(msg):
    keywords = []
    for kwLen in range(2, len(msg)):
        for kwStart in range(len(msg) - kwLen + 1):
            keywords.append(msg[kwStart : kwStart + kwLen])
    return keywords


def randomlyChoose(puns):
    return puns[random.randint(0,len(puns)-1)]
    
    
def Idk(strr):
    ## parse 注音
    strr.split('ˋˊˇ˙')
    return 123


def findPun(keyword):
    # with open("dict.csv") as dic:
        


    pass


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
    
    # if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        
    #     # Phoebe 愛唱歌
    #     pretty_note = '♫♪♬'
    #     pretty_text = ''
        
    #     for i in event.message.text:
        
    #         pretty_text += i
    #         pretty_text += random.choice(pretty_note)
    
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(text=pretty_text)
    #     )

    responseMessage = handleMessage(event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=responseMessage)
    )




import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)