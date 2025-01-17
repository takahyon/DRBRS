import flask
import plotly
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
def get_data(model):


    path = "/Users/takamasa/Documents/CDSL/Distributed-backup/disaster-list/earthquakelist.json"
    disaster_list = {}
    # 震災リストから自動で取得する
    with open(f"{path}","r") as f:
        disaster_list = json.load(f)

    process_list = []
    timelist = []
    countdict = {}
    if(model=="dom"):
        db = client["tweets"]
        # コレクション(Table)作成
        collection = db['eq']
        for post in collection.find({"disaster_name":"東日本大震災"}).sort('date',-1):
            dt = datetime.strptime(post['date'], '%Y-%m-%d %H:%M:%S')
            dt2 = "{0:%Y-%m-%d %H:%M}".format(dt)
            timelist.append(dt2)
            # ここのみ、seabornを用いて可視化

        disdate = datetime.strptime("{0:%Y-%m-%d %H:%M}".format(datetime.strptime(disaster_list["東日本大震災"], '%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M')
        since = disdate + timedelta(hours=-2)
        until = disdate + timedelta(hours=+1)
        for d in range(189):
            if since != until:
                countdict.update({"{0:%Y-%m-%d %H:%M}".format(since):0})
                since = since+timedelta(minutes=+1)
            if since == until:
                break

    if (model == "csm"):
        db = client["csm"]
        # コレクション(Table)作成
        collection = db['eq']

        for post in tqdm(collection.find().sort('date', -1)):
            dt = datetime.strptime(post['date'], '%Y-%m-%d %H:%M:%S')
            dt2 = "{0:%Y-%m-%d %H:%M}".format(dt)
            timelist.append(dt2)
            # ここのみ、seabornを用いて可視化


        disdate = datetime.strptime("{0:%Y-%m-%d %H:%M}".format(datetime.strptime(date, '%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M')
        since = disdate + timedelta(hours=-2)
        until = disdate + timedelta(hours=+1)
        for d in range(189):
            if since != until:
                countdict.update({"{0:%Y-%m-%d %H:%M}".format(since):0})
                since = since+timedelta(minutes=+1)
            if since == until:
                break

    from collections import Counter

    count = Counter(timelist)

    data_x = []
    data_y = []

    for x, y in count.items():
        countdict.update({x: y})
    return countdict.keys(),countdict.values()

def make_graph():
    # Using graph_objects
    import plotly.graph_objects as go
    data_x, data_y = get_data()
    #plt.ylim([0,10])
    sns.lineplot(data_x,data_y)
    import pandas as pd
    #df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
    fig = go.Figure([go.Scatter(x=data_x, y=data_y)])
    fig.show()

if __name__ == '__main__':
    make_graph()