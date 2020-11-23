import csv
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

while True:
    newWord = input("查詢讀音：")
    if newWord == "exit":
        break
    pronunciation = pronounce(newWord)

    print("唸法：", pronunciation, "end", sep = "")
