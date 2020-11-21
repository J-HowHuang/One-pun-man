from flask import Flask, request, abort
import json
import re
from timeit import default_timer as timer
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
    # print("msg:", msg)
    keywords = parseMessage(msg)
    # print("keywords:", keywords)
    puns = []
    # ----test---- #
    k = True
    # ------------ #
    for keyword in keywords:
        pronunciation = pronounce(keyword)
        bpmf_list = similarPhonetics(pronunciation)
        # ----test---- #
        #if k:
        #    print(similarPhonetics(bpmf))
        #    k = False
        # ------------ #
        for bpmf in bpmf_list:
            puns.append(findPun(keyword, msg, bpmf))
    # puns = flatten(puns)
    # print("puns:", puns)
    if len(flatten(puns)) != 0:
        return randomlyChoose(puns)
    else:
        return "pun not found"


def parseMessage(msg):
    keywords = []
    # maxLen = len(msg) + 1
    # if maxLen > 4:
    #     maxLen == 4
    rangeStart = len(msg) - 6
    if rangeStart < 0:
        rangeStart = 0
    
    
    for kwStart in range(rangeStart, len(msg) - 2 + 1):
        keywords.append(msg[kwStart : kwStart + 2])
    return keywords


def randomlyChoose(puns):
    while True:
        for list in puns:
            if len(list) > 0:
                if random.randint(0, 10) < 8: 
                    return list[random.randint(0, len(list)-1)]
    
    
    
def similarPhonetics(pronunciation):   # phonetic is bpmf type  return bpmf list
    ##################
    def combine(origin, to_append):
        result = list()
        for s in origin:
            for a in to_append:
                result.append(s+'\u3000'+a)
        return result
        
    def recur(combinations: list, tmpstr, level, pronunciation_list: list, similar_pronunciations: dict):
        if level == len(pronunciation_list):
            combinations.append(tmpstr[:-1])
        else:
            # 這邊是開始接的部分
            for i in similar_pronunciations[pronunciation_list[level]]:
                recur(combinations, tmpstr+i+'\u3000', level+1, pronunciation_list, similar_pronunciations)
    
    tones = '˙\u3000ˊˇˋ'
    #################
    # -------- rule -------- #
    # ㄣㄥ 互通
    # ㄓㄗ
    # ㄔㄘ
    # ㄕㄙ
    # ㄖㄌ
    # ㄦㄜ
    rules = { 'ㄣ': 'ㄥ', 'ㄥ': 'ㄣ', 
              'ㄓ': 'ㄗ', 'ㄗ': 'ㄓ', 
              'ㄔ': 'ㄘ', 'ㄘ': 'ㄔ', 
              'ㄕ': 'ㄙ', 'ㄙ': 'ㄕ', 
              'ㄖ': 'ㄌ', 'ㄌ': 'ㄖ', 
              'ㄦ': 'ㄜ', 'ㄜ': 'ㄦ', }
    def rule_change_consonant(pronunciation):
        similar_pronunciations = list()
        for consonant in pronunciation:
            if consonant in rules:
                tmp = pronunciation.replace(consonant, rules[consonant])
                similar_pronunciations.append(tmp)
        return similar_pronunciations
    def rule_change_tone(pronunciation):
        similar_pronunciations = list()
        for i, tone in enumerate(tones):
            if tone in pronunciation:
                raise_tone = pronunciation.replace(tone,tones[min(i+1,len(tones)-1)])
                drop_tone = pronunciation.replace(tone,tones[max(i-1,0)])
                if raise_tone != pronunciation:
                    similar_pronunciations.append(raise_tone)
                if drop_tone != pronunciation:
                    similar_pronunciations.append(drop_tone)
        
        return similar_pronunciations
    # ---------------------- #

    if pronunciation[0] == "(":
        pronunciation = pronunciation[3:]
    pronunciation_list = pronunciation.split('\u3000')
    # similar sound
    similar_pronunciations = dict()
    for p in pronunciation_list:
        similar_pronunciations[p] = [p]
        # --- rule add here--- #

        # -------------------- #
        similar_pronunciations[p] += rule_change_consonant(p)
        similar_pronunciations[p] += rule_change_tone(p)
    combinations = similar_pronunciations[pronunciation_list[0]]
    for i in range(1,len(pronunciation_list)):
        combinations = combine(combinations, similar_pronunciations[pronunciation_list[i]])
    return combinations
        # ^^ 
        # || 上面那三小
        # || 下面那三小
        # vv

def pronounce(keyword):
    bpmf = ""
    with open("dict2.csv") as csvfile:
        dic = csv.reader(csvfile)
        for data in dic:
            if data[1] == keyword:
                bpmf = data[5]
                break
         
    if bpmf != "":
        return bpmf
    else:  
        for character in keyword:
            with open("dict2.csv") as csvfile:
                dic = csv.reader(csvfile)
                for data in dic:
                    if data[1] == character:
                        if data[5][0] == "(":
                            bpmf += ('　' + data[5][3:])
                        else:
                            bpmf += ('　' + data[5])
                        break

    if bpmf[0] == '　':
        bpmf = bpmf[1:]
    return bpmf
            


def findPun(keyword, msg, bpmf):
    # print(bpmf)
    puns = []
    # print(bpmf, len(bpmf))
    with open("dict2.csv") as csvfile:
        dic = csv.reader(csvfile)
        for data in dic:
            # print(bpmf)
            if ((bpmf == data[5][:len(bpmf)] and (len(data[5]) == len(bpmf) or data[5][len(bpmf)] == '　')) or (bpmf == data[5][-len(bpmf):] and (len(data[5]) == len(bpmf) or data[5][-len(bpmf) - 1] == '　'))) and len(data[1]) > 2 and data[1] not in msg and keyword not in data[1]:
                # print(data[5], len(data[5]))
                puns.append(data[1])
# (bpmf == data[:len(bpmf)] or bpmf == data[-len(bpmf):]) and 
    return puns



# end



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
    print("Finding \"", event.message.text, "\" pun")
    start = timer()
    responseMessage = handleMessage(event.message.text)
    end = timer()
    if responseMessage != "pun not found":
        print("\"", event.message.text, "\" got pun: \"", responseMessage, "\", time:", str(end - start), "sec")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=responseMessage)
        )
    else:
        print("\"", event.message.text, "\"find no puns, time:", str(end - start), "sec")




import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)