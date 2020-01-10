import json
import csv
import os
from datetime import datetime

def csv2json(csv_path):
    # 20191012-hagivis.csv　の形式
    basename = os.path.basename(csv_path)
    disaster_kind = basename.split('-')[0]
    disaster_date = basename.split('-')[1]
    disaster_name = basename.split('-')[2].replace('.csv','')

    data = {}
    with open(csv_path) as csvfile:
        csvReader = csv.DictReader(csvfile, delimiter=";")
        for fieldname in csvReader.fieldnames:
            for rows in csvReader:
                text = rows['text']
                data[text] = rows
                data[text]["disaster_date"] = datetime.strptime(disaster_date,"%Y%m%d%H:%M:%S")
                data[text]["disaster_name"] = disaster_name

    #print(kind,data)

    # print the rows in json format
    return disaster_kind,data
