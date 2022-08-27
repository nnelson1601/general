from distutils.log import debug
from time import sleep
from wordleConfig import clear_word, get_five_letter_words, load_driver, set_game, guess_word, check_win, get_letter_scores, validate_guess, write_five_letter_words
from WordleHelper import WordleHelper
import requests

import datetime
import logging
import sys
import os
import azure.functions as func

from flask import Flask, Response
# import uwsgi

LOGIC_APP_URL = 'https://prod-04.centralus.logic.azure.com:443/workflows/ba702c58db334b86bbd490eed1a9c898/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=1vH0g_Yi-YLkxtM9W2pykxDE29uMZHGAGnQYCSMSa7M'

app = Flask("general")

logger = logging.getLogger("")
logger.setLevel(logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
# logger.info("OS name - " + os.name)

import wordle
# import creighton

if __name__ == '__main__' : app.run(host="0.0.0.0", port=80)