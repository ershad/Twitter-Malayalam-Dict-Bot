#!/usr/bin/python

import time
from mlbot import MLDictBot

bot = MLDictBot()

if __name__ == "__main__":
    while True:
        bot.process_requests()
        time.sleep(2)
