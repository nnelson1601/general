from time import sleep
from wordleConfig import clear_word, get_five_letter_words, load_driver, set_game, guess_word, check_win, get_letter_scores, validate_guess, write_five_letter_words
from WordleHelper import WordleHelper
import requests

import datetime

from flask import Response

from __main__ import app

@app.route("/api/wordle/solve")
def main():
  utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

  app.logger.info('Wordle script ran at %s', utc_timestamp)


  words = get_five_letter_words()
  letter_scores = get_letter_scores()
  driver = load_driver()
  keyboard, game_board = set_game(driver)

  wordleHelper = WordleHelper(words, letter_scores)

  wordleHelper.filter_out_impossible_words()
  wordleHelper.generate_guess_words(guessIndex=0, tolerant=False) 
  
  try:
    i = 0
    while i < 6:
      app.logger.info("\n")
      app.logger.info("{: >20} {: <20}".format("Guess:", str(i + 1)))
      app.logger.info("{: >20} {: <20}".format("Remaining words:", len(wordleHelper.possible_words)))
      app.logger.info("{: >20} {: <20}".format("Guess words left:", len(wordleHelper.guess_words)))

      # guess = ''
      # while len(guess) == 0:

      bestPossibleWord = wordleHelper.possible_words[0]
      app.logger.info("{: >20} {: <20}".format("Possible word:", bestPossibleWord))

      if len(wordleHelper.guess_words) > 0:
        suggestedGuess = wordleHelper.guess_words[0]
        app.logger.info("{: >20} {: <20}".format("Suggestion:", suggestedGuess))
      else:
        app.logger.info("{: >20} {: <20}".format("Suggestion:", "None remaining"))

        # guess = input("{: >20} ".format('Guess a word:'))
        # if guess == "q":
        #   break
        # elif guess == "a":
        #   app.logger.info(wordleHelper.possible_words)
        #   guess = ''
        
      guess = suggestedGuess
      guess_word(guess, keyboard)

      if not validate_guess(game_board, i):
        clear_word(keyboard)
        wordleHelper.remove_word(guess)
        write_five_letter_words(wordleHelper.all_words)
        app.logger.info("{: >20} {: <20}".format("Invalid guess:", "Game Over!"))
        break

      i += 1
      wordleHelper.update_letter_possibilities(game_board, guess, prevGuessIndex=i-1)
      wordleHelper.score_words()
      wordleHelper.filter_out_impossible_words()
      wordleHelper.generate_guess_words(guessIndex=i, tolerant=True)

      if check_win(driver):
        app.logger.info("Game Over!")
        sleep(1)
        break

    results = wordleHelper.result_text.replace("Wordle Score", f"Wordle Score {i}/6")
    results += "<br>~Nila~"

    # screenshot capture
    driver.get_screenshot_as_file("image.png")
    driver.close()

  except:
    results = "Uh oh! I made a mistake and couldn't solve today's Wordle!<br>~Nila~"
    
  app.logger.info(results)
  # app.logger.info(results.encode('utf-8'))


  # app.logger.info(payload)

  # x = requests.post(LOGIC_APP_URL,
  #                 data=results.encode('utf-8'),
  #                 headers={'Content-type': 'text/plain; charset=utf-8'})

  return Response(
    headers={'Content-type': 'text/plain; charset=utf-8'},
    response=results,
    status=200
  )
