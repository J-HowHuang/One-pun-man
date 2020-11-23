import csv
from functions import *

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

    with open('dict4pun.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        w1 = newWord
        w2 = pronunciation
        writer.writerow([w1, w2])


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
 
 
