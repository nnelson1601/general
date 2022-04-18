from time import sleep
import random
from wordleConfig import clear_word, get_five_letter_words, load_driver, set_game, guess_word, check_win, get_letter_scores, validate_guess, write_five_letter_words
from WordleHelper import WordleHelper

def main():
  words = get_five_letter_words()
  letter_scores = get_letter_scores()
  driver = load_driver()
  keyboard, game_board = set_game(driver)

  wordleHelper = WordleHelper(words, letter_scores)

  wordleHelper.filter_out_impossible_words()
  wordleHelper.generate_guess_words(guessIndex=0, tolerant=False) 
  
  i = 0
  while i < 6:
    print("\n")
    print("{: >20} {: <20}".format("Guess:", str(i + 1)))
    print("{: >20} {: <20}".format("Remaining words:", len(wordleHelper.possible_words)))
    print("{: >20} {: <20}".format("Guess words left:", len(wordleHelper.guess_words)))

    guess = ''
    while len(guess) == 0:

      bestPossibleWord = wordleHelper.possible_words[0]
      print("{: >20} {: <20}".format("Possible word:", bestPossibleWord))

      if len(wordleHelper.guess_words) > 0:
        suggestedGuess = wordleHelper.guess_words[0]
        print("{: >20} {: <20}".format("Suggestion:", suggestedGuess))
      else:
        print("{: >20} {: <20}".format("Suggestion:", "None remaining"))

      guess = input("{: >20} ".format('Guess a word:'))
      if guess == "q":
        break
      elif guess == "a":
        print(wordleHelper.possible_words)
        guess = ''
      

    guess_word(guess, keyboard)

    if not validate_guess(game_board, i):
      clear_word(keyboard)
      wordleHelper.remove_word(guess)
      write_five_letter_words(wordleHelper.all_words)
      print("{: >20} {: <20}".format("Invalid guess:", "Try again"))
      continue

    if check_win(driver):
      print("\nWHOOP! " + guess.upper() + " was the correct word!")
      sleep(1)
      break

    i += 1
    wordleHelper.update_letter_possibilities(game_board, guess, prevGuessIndex=i-1)
    wordleHelper.score_words()
    wordleHelper.filter_out_impossible_words()
    wordleHelper.generate_guess_words(guessIndex=i, tolerant=True)
    

  # screenshot capture
  driver.get_screenshot_as_file("image.png")
  driver.close()

if __name__ == '__main__' : main()
