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
from WebMonitor import get_data
# モンゴのクライアント作成
# client = MongoClient('mongodb://localhost:27017/')
client = MongoClient('localhost', 27017)

def discriminator():
    # DB作成
    domdb = client['tweets']
    csmdb = client['dummy']
    # コレクション(Table)作成
    dom_collection = domdb['eq']
    csm_collection = csmdb['eq']

    dum = "/Users/takamasa/Documents/CDSL/Distributed-backup/disaster-list/dummylist.json"
    dummy_list = {}
    # 震災リストから自動で取得する
    with open(f"{dum}", "r") as f:
        dummy_list = json.load(f)

    for name,date in dummy_list.items():
        def get_csm(name):
            timelist = []
            query = {"disaster_name":name}

            for post in csm_collection.find(query).sort('date',-1):
                dt = datetime.strptime(post['date'], '%Y-%m-%d %H:%M:%S')
                dt2 = "{0:%Y-%m-%d %H:%M}".format(dt)
                timelist.append(dt2)
                # ここのみ、seabornを用いて可視化

            from collections import Counter

            count = Counter(timelist)

            countdict = {}
            disdate = datetime.strptime("{0:%Y-%m-%d %H:%M}".format(datetime.strptime(date, '%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M')
            since = disdate + timedelta(hours=-2)
            until = disdate + timedelta(hours=+1)
            for d in range(189):
                if since != until:
                    countdict.update({"{0:%Y-%m-%d %H:%M}".format(since):0})
                    since = since+timedelta(minutes=+1)
                if since == until:
                    break

            data_time = []
            data_counts = []
            for x, y in count.items():
                countdict.update({x: y})
            return countdict.keys(), countdict.values()
        # dom => Disaster Occur Model
        # csm => Current Stream Model
        from scipy.stats import pearsonr

        dom_time,dom_count = get_data("dom")
        csm_time, csm_count = get_csm(name)

        dom = dict(zip(dom_time,dom_count))
        csm = dict(zip(csm_time,csm_count))
        dom_list = []
        csm_list = []

        # 辞書型から配列へ。valueのみを格納。
        for value1 in dom.values():
            dom_list.append(value1)
        for value2 in csm.values():
            csm_list.append(value2)

        correlation, pvalue = pearsonr(dom_list[:180], csm_list[:180])
        thresold = 0.80
        correlation_percent = '{:.2%}'.format(correlation)
        now = datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')
        #print(name)
        if correlation > thresold:
            print(name+"&"+correlation_percent+"&災害 \\\\")
        if -thresold < correlation < thresold:
            print(name+"&"+correlation_percent+"&Not災害 \\\\")
        if -thresold > correlation:
            print(name+"&"+correlation_percent+"&災害後 \\\\")
        # if correlation > thresold:
        #     print(name": Disaster happen!! Start Backup",correlation_percent)
        # if -thresold < correlation < thresold:
        #     print(now,": Recording",correlation_percent)
        # if -thresold > correlation:
        #     print(now, ": Disaster calm. Recording",correlation_percent)

        #print(correlation)  # -0.8360556025697304

discriminator()