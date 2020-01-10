import get_from_twitter
import tweet_database.Mongo as Mongo
import json
from multiprocessing import Process
import show_data

def main():


    path = "/Users/takamasa/Documents/CDSL/Distributed-backup/disaster-list/earthquakelist.json"
    disaster_list = {}
    # 震災リストから自動で取得する
    with open(f"{path}","r") as f:
        disaster_list = json.load(f)

    process_list = []

    for disaster_name, disaster_date in disaster_list.items():
        process = Process(
            target=get_from_twitter.get_data_process,
            kwargs={'disaster_name': disaster_name,"disaster_date":disaster_date,"maxTweet":None}
        )
        show_data.show_dom(disaster_name)
        process.start()
        process_list.append(process)

    for process in process_list:
        process.join()

        # twitterからデータ取得 csv作成
    #get_from_twitter.get_data()



if __name__ == '__main__':

    main()


