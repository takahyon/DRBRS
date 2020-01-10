from pymongo import MongoClient
import numpy as np
import seaborn as sns
sns.set()
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from tqdm import tqdm
import json
from matplotlib.dates import drange
from matplotlib import pyplot as plt
#plt.rcParams['font.family'] = 'IPAPGothic'

# モンゴのクライアント作成
# client = MongoClient('mongodb://localhost:27017/')
client = MongoClient('localhost', 27017)

def show_dom(disaster_name):
    print(disaster_name)
    # DB作成
    db = client['tweets']
    # コレクション(Table)作成
    collection = db['eq']

    timelist = []
    query = {"disaster_name":disaster_name}
    for post in tqdm(collection.find(query)):
        dt = datetime.strptime(post['date'], '%Y-%m-%d %H:%M')
        timelist.append(dt)
        # ここのみ、seabornを用いて可視化

    from collections import Counter

    count = Counter(timelist)

    delta = timedelt a(days=1)

    data_x = []
    data_y = []

    for x,y in count.items():
        data_x.append(x)
        data_y.append(y)

    sns.lineplot(data_x,data_y)
    plt.title(disaster_name)
    plt.show()

if __name__ == '__main__':
    print("disastername?")
    input = input()
    if input == "all":
        path = "/Users/takamasa/Documents/CDSL/Distributed-backup/disaster-list/earthquakelist.json"
        with open(f"{path}", "r") as f:
            disaster_list = json.load(f)
        for disaster_name, disaster_date in disaster_list.items():
            show_dom(disaster_name)
    else:
        show_dom(input)
