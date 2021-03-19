import re
import json
import random
import csv
import os

flatten = lambda t: [item for sublist in t for item in sublist]
dict_path = "./Dictionaries"

def find_chinese(file):
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    msg = re.sub(pattern, '', file)
    return msg


def handleMessage(msg):
    msg = find_chinese(msg)
    keywords = parseMessage(msg)
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
            if bpmf == pronunciation:
                puns.insert(0, findPun(keyword, msg, bpmf))
            else:
                puns.append(findPun(keyword, msg, bpmf))
    # puns = flatten(puns)
    # print("puns:", puns)
    if len(flatten(puns)) != 0:
        return randomlyChoose(puns)
    else:
        return "pun not found"

# return msg segments for one pun man to search for puns
def parseMessage(msg):
    keywords = []
    rangeStart = len(msg) - 6
    if rangeStart < 0:
        rangeStart = 0
    
    
    for kwStart in range(rangeStart, len(msg) - 2 + 1):
        keywords.append(msg[kwStart : kwStart + 2])
    return keywords


def randomlyChoose(puns):
    while True:
        for lists in puns:
            if len(lists) > 0:
                if random.randint(0, 10) < 8: 
                    return lists[random.randint(0, len(lists)-1)]
    
    
    
def similarPhonetics(pronunciation):   # phonetic is bpmf type  return bpmf list
    ##################
    def combine(origin, to_append):
        result = list()
        for s in origin:
            for a in to_append:
                result.append(s+'\u3000'+a)
        return result
    
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
                break
            if i == len(tones)-1:
                drop_tone = pronunciation + tones[2]
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

def pronounce(keyword):
    bpmf = ""
    with open(os.path.join(dict_path, "dict4pronounce.csv")) as csvfile:
        dic = csv.reader(csvfile)
        for data in dic:
            if data[0] == keyword:
                bpmf = data[1]
                break
         
    if bpmf != "":
        return bpmf
    else:  
        for character in keyword:
            with open(os.path.join(dict_path, "dict4pronounce.csv")) as csvfile:
                dic = csv.reader(csvfile)
                for data in dic:
                    if data[0] == character:
                        if data[1][0] == "(":
                            bpmf += ('　' + data[1][3:])
                        else:
                            bpmf += ('　' + data[1])
                        break

    if bpmf[0] == '　':
        bpmf = bpmf[1:]
    return bpmf
            


def findPun(keyword, msg, bpmf):
    # print(bpmf)
    puns = []
    # print(bpmf, len(bpmf))
    with open(os.path.join(dict_path, "dict4pun.csv")) as csvfile:
        dic = csv.reader(csvfile)
        for data in dic:
            # print(bpmf)
            if ((bpmf == data[1][:len(bpmf)] and (len(data[1]) == len(bpmf) or data[1][len(bpmf)] == '　')) or (bpmf == data[1][-len(bpmf):] and (len(data[1]) == len(bpmf) or data[1][-len(bpmf) - 1] == '　'))) and len(data[0]) > 2 and data[0] not in msg and keyword not in data[0]:
                # print(data[5], len(data[5]))
                puns.append(data[0])
# (bpmf == data[:len(bpmf)] or bpmf == data[-len(bpmf):]) and 
    return puns
