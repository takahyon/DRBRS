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

def discriminator():
    # DB作成
    db = client['tweets']
    # コレクション(Table)作成
    dom_collection = db['eq']
    csm_collection = db['csm']

    def get_dom(disaster_name):
        timelist = []
        query = {"disaster_name":disaster_name}
        for post in tqdm(dom_collection.find(query)):
            dt = datetime.strptime(post['date'], '%Y-%m-%d %H:%M')
            timelist.append(dt)
            # ここのみ、seabornを用いて可視化

        from collections import Counter
        count = Counter(timelist)
        delta = timedelta(days=1)
        data_time = []
        data_counts = []
        for x,y in count.items():
            data_time.append(x)
            data_counts.append(y)
        return data_time,data_counts

    def get_csm():
        timelist = []
        query = {}
        for post in tqdm(csm_collection.find(query)):
            dt = datetime.strptime(post['date'], '%Y-%m-%d %H:%M')
            timelist.append(dt)
            # ここのみ、seabornを用いて可視化

        from collections import Counter
        count = Counter(timelist)
        delta = timedelta(days=1)
        data_time = []
        data_counts = []
        for x,y in count.items():
            data_time.append(x)
            data_counts.append(y)
        return data_time,data_counts
    # dom => Disaster Occur Model
    # csm => Current Stream Model
    from scipy.stats import pearsonr

    dom_time,dom_count = get_dom()
    csm_time, csm_count = get_csm()

    dom = dict(dom_time,dom_count)
    csm = dict(csm_time,csm_count)
    dom_list = []
    csm_list = []

    # 辞書型から配列へ。valueのみを格納。
    for value1 in dom.values():
        dom_list.append(value1)
    for value2 in csm.values():
        csm_list.append(value2)

    correlation, pvalue = pearsonr(dom_list, csm_list)
    thresold = 80.0
    correlation_percent = '{:.2%}'.format(correlation)

    if correlation < thresold:
        print(datetime.now,": Disaster happen!! Start Backup",correlation_percent)
    if -thresold < correlation < thresold:
        print(datetime.now,": Recording",correlation_percent)
    if -thresold > correlation:
        print(datetime.now, ": Disaster calm. Recording",correlation_percent)

    print(correlation)  # -0.8360556025697304
