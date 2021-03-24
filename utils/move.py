import csv
import os

dict_path = "../Dictionaries/"
character = input("請輸入欲更改的破音字：")
bpmf = []

with open(os.path.join(dict_path, "dict4pronounce.csv")) as csvfile:
    dic = csv.reader(csvfile)
    for data in dic:
        if data[0] == character:
            print(data[1])
            bpmf.append(data[1])


select = int(input())

# with open("dict2.csv") as csvfile:
#     dic = csv.reader(csvfile)
#     for data in dic:
#         if data[1] == character and data[5] == bpmf[0]:
#             data[5] = bpmf[select]
#             continue
#         if data[1] == character and data[5] == bpmf[select]:
#             data[5] = bpmf[0]
#             continue



lines = []
delete = []
with open(os.path.join(dict_path, 'dict4pronounce.csv'), 'r') as readFile:
    reader = csv.reader(readFile)
    for row in reader:
        lines.append(row) 
        if row[0] == character and row[1] != bpmf[select]:
            # print(row)
            delete.append(row)
            lines.remove(row)



with open(os.path.join(dict_path, 'dict4pronounce.csv'), 'w') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(lines)
    writer.writerows(delete)
    


with open(os.path.join(dict_path, "dict4pronounce.csv")) as csvfile:
    dic = csv.reader(csvfile)
    for data in dic:
        if data[0] == character:
            print(data[1])
            bpmf.append(data[1])