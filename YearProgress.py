#!/usr/bin/env python3

import numpy as np
import cv2
from datetime import datetime
import tweepy
import schedule
import time
import os.path
from keys import keys

def create_image():
    # creating a img
    img = np.zeros((130, 425, 3), np.uint8)
    value = 0
    if datetime.now().year % 4 == 0:
        daysinyear = 366
    else:
        daysinyear = 365
    today_date = datetime.now().date()
    day_count = datetime.now().timetuple().tm_yday
    percent = round((day_count * 100) / daysinyear, 2)
    for x in range(130):
        for y in range(425):
            if (0 <= x <= 15 or 115 <= x <= 130 or 0 <= y <= 30 or (day_count + 30) <= y <= 425):
                value = 0
            else:
                value = 1
            if (7 <= x <= 8 or 122 <= x <= 123 or 12 <= y <= 13 or 412 <= y <= 413):
                value = 1
            if (0 <= x <= 6 or 124 <= x <= 130 or 0 <= y <= 11 or 414 <= y <= 425):
                value = 0
            if value == 0:
                img[x, y] = [1, 200, 255]
            else:
                img[x, y] = [1, 1, 1]

    # save our image as a "png" image
    cv2.imwrite("progress_bar.png", img)
    itweet = "2021 Progress\nDate: " + str(today_date.strftime("%b %d %Y")) + "      Progress: " + str(percent) + "%\n #2021 #yearprogress"
    return itweet

def read_last(FILE_NAME):
    file_read = open(FILE_NAME, 'r')
    last_seen_id = int(file_read.read().strip())
    file_read.close()
    return last_seen_id

def write_last(FILE_NAME, last_seen_id):
    file_write = open(FILE_NAME, 'w')
    file_write.write(str(last_seen_id))
    file_write.close()
    return

def create_file(FILE_NAME):
    if os.path.isfile(FILE_NAME):
        return
    else:
        f = open(FILE_NAME, 'w')
        f.write(str('ENTER LAST USER STATUS ID'))
        f.close()
        return

def authenticate():
    auth = tweepy.OAuthHandler(
        keys['consumer_key'],
        keys['consumer_secret']
    )
    auth.set_access_token(
        keys['access_token'],
        keys['access_token_secret']
    )
    api = tweepy.API(auth)
    return api

def code1():
    api = authenticate()
    tweet = create_image()

    # Upload image
    media = api.media_upload("progress_bar.png")

    # Post tweet with image
    post_result = api.update_status(status=tweet, media_ids=[media.media_id])
    print("posted" + post_result.text)

def reply():
    api = authenticate()
    itweet = create_image()
    FILE_NAME = 'last_id.txt'
    create_file(FILE_NAME)
    media = api.media_upload("progress_bar.png")

    tweets = api.mentions_timeline(read_last(FILE_NAME), tweet_mode='extended')
    #reply to the tweets
    for tweet in reversed(tweets):
        if '@yearprogressbot' in tweet.full_text.lower():
            print('replied to' + str(tweet.id)+ ' - ' + tweet.full_text)
            api.update_status(status = "@"+ tweet.user.screen_name + ' ' + itweet, media_ids = [media.media_id], in_reply_to_status_id = tweet.id)
            api.create_favorite(tweet.id)
            write_last(FILE_NAME, tweet.id)

def main():
    schedule.every().day.at("00:01").do(code1)
    schedule.every(5).minutes.do(reply)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
