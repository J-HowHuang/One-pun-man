import csv
import os

dict_path = "../Dictionaries"

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
    if bpmf == "":
        return bpmf
    if bpmf[0] == '　':
        bpmf = bpmf[1:]
    return bpmf

while True:
    newWord = input("新增單詞：")
    if newWord == "exit":
        break
    pronunciation = pronounce(newWord)

    print("唸法：", pronunciation, "是否正確？")

    correct = input("[y/n]:")
    if(correct == "n"):
        pronunciation = input("請輸入正確唸法：")
        pronunciation = pronunciation.replace(' ', '\u3000')

    with open(os.path.join(dict_path, 'dict4pun.csv'), 'a') as csvfile:
        writer = csv.writer(csvfile)
        w1 = newWord
        w2 = pronunciation
        writer.writerow([w1,w2])


# ---------------------------- #
    ######
   #####
  ####
 ###
#########
    ####
   ###
  ##
 #

 #####    ###
  ### #    #
  ###  #   #
  ###   #  #
  ###    # #
  ###     ##
 #####    ###

 ############
 #    ##    #
      ##
      ##
      ##
     ####
############
 
 
