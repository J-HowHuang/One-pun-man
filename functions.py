import json
import re
import csv
import random

flatten = lambda t: [item for sublist in t for item in sublist]

def test():
    print("import successed")

def find_chinese(file):
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    msg = re.sub(pattern, '', file)
    return msg


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
    return puns[random.randint(0, len(puns)-1)]


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
        # ^^ 
        # || 上面那三小
        # || 下面那三小
        # vv


def pronounce(keyword):
    bpmf = ""
    with open("dict4pronounce.csv") as csvfile:
        dic = csv.reader(csvfile)
        for data in dic:
            if data[0] == keyword:
                bpmf = data[1]
                break
         
    if bpmf != "":
        return bpmf
    else:  
        for character in keyword:
            with open("dict4pronounce.csv") as csvfile:
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
    with open("dict4pun.csv") as csvfile:
        dic = csv.reader(csvfile)
        for data in dic:
            # print(bpmf)
            if ((bpmf == data[1][:len(bpmf)] and (len(data[1]) == len(bpmf) or data[1][len(bpmf)] == '　')) or (bpmf == data[1][-len(bpmf):] and (len(data[1]) == len(bpmf) or data[1][-len(bpmf) - 1] == '　'))) and len(data[0]) > 2 and data[0] not in msg and keyword not in data[0]:
                # print(data[5], len(data[5]))
                puns.append(data[0])
# (bpmf == data[:len(bpmf)] or bpmf == data[-len(bpmf):]) and 
    return puns


# def classified_flatten(puns, kwNum):
#     puns1 = puns[:kwNum]
#     puns2 = puns[kwNum:]
#     return [flatten(puns1), flatten(puns2)]


def handleMessage(msg, debug=False, special_case=False):

    msg = find_chinese(msg)
    if debug:
        print("msg:", msg)

    keywords = parseMessage(msg)
    if debug:
        print("keywords:", keywords)

    puns = []
    # ----test---- #
    # k = True
    # ------------ #
    # for keyword in keywords:
    #     pronunciation = pronounce(keyword)
    #     bpmf_list = similarPhonetics(pronunciation)
    #     # ----test---- #
    #     #if k:
    #     #    print(similarPhonetics(bpmf))
    #     #    k = False
    #     # ------------ #
    #     for bpmf in bpmf_list:
    #         if bpmf == pronunciation:
    #             puns.insert(0, findPun(keyword, msg, bpmf))
    #         else:
    #             puns.append(findPun(keyword, msg, bpmf))

    default = random.randint(0, 10) < 8
    if special_case:
        default = False

    if default:
        if debug:
            print("default:")
        for keyword in keywords:
            pronunciation = pronounce(keyword)
            bpmf_list = similarPhonetics(pronunciation)[:1]
            for bpmf in bpmf_list:
                puns.append(findPun(keyword, msg, bpmf))
        puns = flatten(puns)
        if debug:
            print(puns)
        if len(puns) != 0:
            print("print default")
            return randomlyChoose(puns)

    if debug:
        print("special case:")
    for keyword in keywords:
        pronunciation = pronounce(keyword)
        bpmf_list = similarPhonetics(pronunciation)[1:]
        for bpmf in bpmf_list:
            puns.append(findPun(keyword, msg, bpmf))
    puns = flatten(puns)
    if debug:
        print(puns)
    if len(puns) != 0:
        return randomlyChoose(puns)
        
    return "pun not found"