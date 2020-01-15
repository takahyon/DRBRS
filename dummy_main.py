import get_from_twitter_dummy
import tweet_database.Mongo as Mongo
import json
from multiprocessing import Process
import show_data

def main():


    path = "/Users/takamasa/Documents/CDSL/Distributed-backup/disaster-list/dummylist.json"
    disaster_list = {}
    # 震災リストから自動で取得する
    with open(f"{path}","r") as f:
        disaster_list = json.load(f)

    process_list = []

    for disaster_name, disaster_date in disaster_list.items():
        get_from_twitter_dummy.get_data_process(disaster_name=disaster_name,disaster_date=disaster_date,maxTweet=100000)
        # twitterからデータ取得 csv作成
    #get_from_twitter.get_data()



if __name__ == '__main__':
    main()


