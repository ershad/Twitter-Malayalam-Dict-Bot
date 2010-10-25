#!/usr/bin/python
# -*- coding: utf-8 -*-
#bot_driver.py
#      
#Copyright 2010 Vasudev Kamath <kamathvasudev@gmail.com>
#               Ershad K <ershad92@gmail.com>
#      
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU  General Public License as published by
#the Free Software Foundation; either version 3 of the License, or
#(at your option) any later version.
#     
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#      
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#MA 02110-1301, USA.
#



import time
import tweepy
from mlbot import MLDictBot
from secrets import *

bot = MLDictBot()

CONSUMER_KEY = consumer_key
CONSUMER_SECRET = consumer_secret
ACCESS_KEY = access_key
ACCESS_SECRET = access_secret

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


def get_mentions():
    mentions = api.mentions()

    for status in mentions:
        dict_pos = status.text.find("dict")

        if dict_pos != -1:
            definition = bot.process_requests(status,dict_pos)
            if definition:
                send_update(status,definition)


                
def send_update(status,definition):
    print definition
    update = '@' + status.user.screen_name + " " + definition.decode("utf-8")
    if len(update) > 140:
        update = update[0:140]
    api.update_status(update)




if __name__ == "__main__":
    while True:
        get_mentions()
        time.sleep(200)
