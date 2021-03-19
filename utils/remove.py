import csv
import os

dict_path="../Dictionaries"

with open(os.path.join(dict_path, 'dict4pronounce.csv'), 'w+') as output_file:
    with open(os.path.join(dict_path, "dict2.csv")) as csvfile:
        dic = csv.reader(csvfile)
        for data in dic:
            if len(data[1]) <= 2:
                line = [data[1], data[5]]
                if len(line) < 2:
                    break
                output_file.write(','.join(line))
                output_file.write('\n')

