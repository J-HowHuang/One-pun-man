import csv


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

    with open('dict2.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        w1 = newWord
        w2 = pronunciation
        writer.writerow(['_', w1, '_', '_', '_', w2, '_', '_', '_', '_', '_'])


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
  ##########
 
 
