#!/usr/bin/python

# -*- coding: utf-8 -*-
#mlbot.py : Generic English to Malayalam Dictionary Class
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



import sqlite3
from dictdlib import DictDB


class MLDictBot(object):
    
    def __init__(self):        
        self.db_connection = None
        self.en_ml_db = DictDB("freedict-eng-mal")

        
    def process_requests(self,status,dict_pos):
        if self.db_connection == None:
            self.__initialize_db__()

        if not self.__is_processed__(str(status.id)):
            # len('dict')+space = 5
            word = status.text[dict_pos + 5:]
            try:
                definition = self.en_ml_db.getdef(word)[0]
            except:
                definition = "No definition!"
                self.__mark_undefined__(word)

            self.__update_ledger__(status)
            return definition


    def __initialize_db__(self):

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
frequency integer not null) 
        ''')
        
        self.db_connection.commit()
        c.close()

    def  __is_processed__(self,tweet_id):

        c = self.db_connection.cursor()
        c.execute('select count(*) from ml_bot_ledger where tweet_id = ?',(tweet_id,))
        count = c.fetchone()
        if count[0] == 0:
            return False
        else:
            return True
        c.close()

    def __mark_undefined__(self,word):
        if len(word.split(' ')) == 1:
            # If request has mutliple word
            # discard it
            c = self.db_connection.cursor()
            c.execute('select count(*) from ml_bot_undefined where word = ?',(word,))
            count = c.fetchone()
            if count[0] == 0:
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
        



        

