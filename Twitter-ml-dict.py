#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Twitterdict.py
# Version 1.0
#
# Copyright (C) 2010 - Ershad K <ershad92@gmail.com>
#
# Licensed under GPL Version 3

import os, sys, codecs
import time
import twitter
from dictdlib import DictDB

# Change the following values
username = 'USERNAME'
password = 'PASSWORD'
sleep_time = 1


fout = open('dataFile', 'a') #to create such a file
fout.close()
api = twitter.Api(username, password)

while True:
	time.sleep(sleep_time)
	word = 'hello'
	timeline = api.GetReplies()
	for s in timeline:
		dict_keyword_find = -1
		check_duplicate = 0;
		#print "%s --> %s" % (s.user.name, s.text)
		tweet = s.user.name + "\t" + s.text
		dict_keyword_find = tweet.find("dict")

		if dict_keyword_find > 0:
			fin = open('dataFile', 'r')
			fin_contents = fin.read()
			check_duplicate = fin_contents.find(str(s.id))
			print check_duplicate
			fin.close()
	
		if check_duplicate < 0:
			print "%s --> %s" % (s.user.name, s.text)
			word = s.text[13:]
			print word #for debugging			
			en_ml_db = DictDB("freedict-eng-mal")
			try:
				definition = en_ml_db.getdef(word)[0]
			except:	
				definition =  "No definitions found"
			print definition
			defi = definition [0:110]
		
			output = '@' + s.user.screen_name + ' ' + defi
			#print len(output)
			print output     
			api.PostUpdate (output.decode("utf-8",'ignore'))
			sleep_time = 30
			fout = open('dataFile', 'a')
			text = str(s.id)
			fout.write(text)
			fout.close()
