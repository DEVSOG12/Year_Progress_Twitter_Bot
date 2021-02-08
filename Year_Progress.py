#!/usr/bin/env python3

import numpy as np
import cv2
import random
from datetime import datetime
import tweepy
import schedule
import time

def code1():
    #creating a img
    img = np.zeros((130, 425, 3), np.uint8)
    value = 0
    if datetime.now().year % 4 == 0:
        daysinyear = 366
    else:
        daysinyear = 365
    today_date = datetime.now().date()
    day_count = datetime.now().timetuple().tm_yday
    percent = round((day_count * 100) / daysinyear,2)
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
                img[x,y] = [1,1,1]

    # save our image as a "png" image
    cv2.imwrite("progress_bar.png", img)

    twitter_auth_keys = {
        "consumer_key": "ENTER API KEY",
        "consumer_secret": "ENTER API SECRET KEY",
        "access_token": "ENTER ACCESS TOKEN",
        "access_token_secret": "ENTER ACCESS TOKEN SECRET"
    }

    auth = tweepy.OAuthHandler(
        twitter_auth_keys['consumer_key'],
        twitter_auth_keys['consumer_secret']
    )
    auth.set_access_token(
        twitter_auth_keys['access_token'],
        twitter_auth_keys['access_token_secret']
    )
    api = tweepy.API(auth)

    # Upload image
    media = api.media_upload("progress_bar.png")

    # Post tweet with image
    tweet = "2021 Progress\nDate: " + str(today_date.strftime("%b %d %Y")) + "      Progress: " + str(percent) + "%\n #2021 #yearprogress"
    print(tweet)
    post_result = api.update_status(status=tweet, media_ids=[media.media_id])



def main():
    schedule.every().day.at("00:00").do(code1)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
