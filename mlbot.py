#!/usr/bin/python

import tweepy
import sqlite3
from dictdlib import DictDB
from secrets import *

CONSUMER_KEY = consumer_key
CONSUMER_SECRET = consumer_secret
ACCESS_KEY = access_key
ACCESS_SECRET = access_secret

class MLDictBot(object):
    """
    """
    
    def __init__(self):
        """
        """
        global CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET
        
        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        self.api = tweepy.API(self.auth)
        self.db_connection = None
        self.en_ml_db = DictDB("freedict-eng-mal")

    def process_requests(self):
        """
        
        Arguments:
        - `self`:
        """
        if self.db_connection == None:
            self.__initialize_db__()

        mentions = self.api.mentions()
        for status in mentions:
            dict_pos = status.text.find("dict")

            if dict_pos != -1:
                if not self.__is_processed__(str(status.id)):
                    # len('dict')+space = 5
                    word = status.text[dict_pos + 5:]
                    try:
                        definition = self.en_ml_db.getdef(word)[0]
                        self.__send_update__(status,definition)
                        self.__update_ledger__(status)
                    except:
                        definition = "No definition!"
                        self.__mark_undefined__(word)


    def __send_update__(status,definition):
        """
        
        Arguments:
        - `status`:
        - `word` :
        """
        update = status.user.screen_name + " " + unicode(definition)
        print update
        self.api.update_status(update)

                    
                    

    def __initialize_db__(self):
        """
        
        Arguments:
        - `self`:
        """
        self.db_connection = sqlite3.connect("/tmp/mlbot.db")
        c = self.db_connection.cursor()
        c.execute('''
        create table if not exists ml_bot_ledger(
           _id integer primary key autoincrement,
           tweet_id text not null) 
        ''')
        c.execute('''
        create table if not exists  ml_bot_undefined(
           _id integer primary key autoincrement,
           word text not null,
           frequency integer not null
        ) 
        ''')
        
        self.db_connection.commit()
        c.close()

    def  __is_processed__(self,tweet_id):
        """
        
        Arguments:
        - `id`: Tweet Id to check
        """
        c = self.db_connection.cursor()
        c.execute('select count(*) from ml_bot_ledger where tweet_id = ?',(tweet_id,))
        c.fetchall()
        print c.rowcount

        if c.rowcount == -1:
            return False
        else:
            return True

    def __mark_undefined__(self,word):
        if word.split(' ') == 1:
            # If request has mutliple word
            # discard it
            c = self.db_connection.cursor()
            c.execute('select count(*) from ml_bot_undefined where word = ?',(word,))
            c.fetchall()
            if c.rowcount == -1:
                c.execute('insert into ml_bot_undefined (word,frequency) values (?,?)',(word,1))
            else:
                c.execute('update ml_bot_undefined set frequency = frequency + 1 where word = ?',(word,))

            self.db_connection.commit()
            c.close()

    def __update_ledger__(self,status):
        c = self.db_connection.cursor()
        c.execute("insert into ml_bot_ledger (tweet_id) values (?)",(status.id,))
        self.db_connection.commit()
        c.close()
        



        

