# -*- coding: utf-8 -*-
import codecs

import GetOldTweets3 as got
from datetime import datetime,timedelta
import tweet_database.Mongo as Mongo
import json
import codecs
from datetime import datetime, timedelta


# def print_tweets(tweets):
#     print("取得件数：", len(tweets))
#     for tweet in tweets:
#         print("---------------------------------")
#         print("ツイートID：", tweet.id)
#         print("ツイートURL：", tweet.permalink)
#         print("アカウントの文字列：", tweet.username)
#         print(tweet.text)
#         print("投稿日：", tweet.date)
#         print("リツイート数：", tweet.retweets)
#         print("いいねの数：", tweet.favorites)
#         if tweet.mentions:
#             print("メンションの内容：", tweet.mentions)
#         if tweet.hashtags:
#             print("ハッシュタグの内容", tweet.hashtags)

# # アカウントの文字列で取得
# tweetCriteria = got.manager.TweetCriteria().setUsername("sugoiyamanaka").setMaxTweets(5)
# tweets = got.manager.TweetManager.getTweets(tweetCriteria)
# print("---------------------------------")
# print("①アカウントの文字列で取得")
# print_tweets(tweets)
#
# # キーワードで取得
# tweetCriteria = got.manager.TweetCriteria().setQuerySearch("ポケモン").setMaxTweets(5)
# tweets = got.manager.TweetManager.getTweets(tweetCriteria)
# print("---------------------------------")
# print("②キーワードで取得")
# print_tweets(tweets)
#
# # 複雑なクエリで取得
# tweetCriteria = got.manager.TweetCriteria().setQuerySearch("西武 AND (ソフトバンク OR 楽天) -失点 #野球").setMaxTweets(5)
# tweets = got.manager.TweetManager.getTweets(tweetCriteria)
# print("---------------------------------")
# print("③複雑なクエリで取得")
# print_tweets(tweets)

# 期間を指定して取得


def get_data(disasterlistpath, maxTweet=None):
    import json
    import codecs
    from datetime import datetime, timedelta


def get_data_process(disaster_name,disaster_date,maxTweet):
    disaster_date = datetime.strptime(disaster_date,"%Y-%m-%d %H:%M:%S")
    since = disaster_date + timedelta(days=-3)
    until = disaster_date + timedelta(hours=+9)

    sincestr = since.strftime("%Y-%m-%d")
    untilstr = until.strftime("%Y-%m-%d")

    if maxTweet is not None:
        tweetCriteria = got.manager.TweetCriteria().setSince(sincestr).setUntil(untilstr).setMaxTweets(maxTweet).setQuerySearch("地震")
    if maxTweet is None:
        tweetCriteria = got.manager.TweetCriteria().setSince(sincestr).setUntil(untilstr).setQuerySearch("沢尻エリカ")

    #tweets = got.manager.TweetManager.getTweets(tweetCriteria)

    outputFileName = f"/Users/takamasa/Documents/CDSL/Distributed-backup/get_data/csv/eq-{disaster_date.strftime('%Y%m%d%H:%M:%S')}-{disaster_name}.csv"

    outputFile = codecs.open(outputFileName, "w+", "utf-8")

    outputFile.write('username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink')

    print('Searching...\n')


    def receiveBuffer(tweets):
        for t in tweets:
            outputFile.write(('\n%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s' % (
            t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions, t.hashtags,
            t.id, t.permalink)))
            res = {
                "username" :t.username,
                "date" :t.date.strftime("%Y-%m-%d %H:%M"),
                "retweets" :t.retweets,
                "favorites" :t.favorites,
                "text" :t.text,
                "geo" :t.geo,
                "mentions" :t.mentions,
                "hashtags" :t.hashtags,
                "id" :t.id,
                "permalink" :t.permalink,
                "disaster_name":disaster_name,
                "disaster_date":disaster_date
            }
            Mongo.json2db(res,"tweets","eq")

        outputFile.flush()
        print('More %d saved on file...\n' % len(tweets))


    got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)
    Mongo.save2db(outputFileName,"tweet")
    #print("---------------------------------")
    #print("④期間を指定して取得")
    #print_tweets(tweets)
