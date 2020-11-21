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

    if bpmf[0] == '　':
        bpmf = bpmf[1:]
    return bpmf

while True:
    newWord = input("查詢讀音：")
    if newWord == "exit":
        break
    pronunciation = pronounce(newWord)

    print("唸法：", pronunciation, "end", sep = "")
