from warnings import catch_warnings
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from time import sleep

WORDLE_URL = 'https://www.nytimes.com/games/wordle/index.html'
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
TEXT_AREA_URL = 'https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_textarea'

# Get letter scores:
def get_letter_scores():
    return {
        'a': 43.31,
        'b': 10.56,
        'c': 23.13,
        'd': 17.25,
        'e': 56.88,
        'f': 9.24,
        'g': 12.59,
        'h': 15.31,
        'i': 38.45,
        'j': 1.00,
        'k': 5.61,
        'l': 27.98,
        'm': 15.36,
        'n': 33.92,
        'o': 36.51,
        'p': 16.14,
        'q': 1.00,
        'r': 38.64,
        's': 29.23,
        't': 35.43,
        'u': 18.51,
        'v': 5.13,
        'w': 6.57,
        'x': 1.48,
        'y': 9.06,
        'z': 1.39
    }

# Get words from txt file
def get_five_letter_words():
  file_name = 'humanWords.txt'
  print(os.getcwd())
  wordsFile = open(os.path.join(os.getcwd(), file_name), "r")
  fiveLetterWords = [word[0:5] for word in wordsFile]
  wordsFile.close()
  return fiveLetterWords

def write_five_letter_words(words):
  file_name = 'humanWords.txt'
  wordsFile = open(os.path.join(os.getcwd(), file_name), "w")
  for i in range(len(words)):
    word = words[i]
    wordsFile.write(word)
    if i < len(words) - 1:
      wordsFile.write("\n")

  wordsFile.close()
  return

# Load Chrome driver
def load_driver():
  chrome_options = Options()
  if str(os.name) != "nt":
    chrome_options.binary_location = "/usr/bin/google-chrome-stable"
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model

  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--window-size=720x480")
  chrome_options.add_argument('--log-level=1')

  # download Chrome Webdriver
  # https://sites.google.com/a/chromium.org/chromedriver/download
  # put driver executable file in the script directory
  file_name = 'chromedriver.exe' if os.name == "nt" else "chromedriver_linux"
  chrome_driver = os.path.join(os.getcwd(), file_name)
  if str(os.name) != "nt":
    os.chmod(chrome_driver, 755)
  chrome_service = Service(chrome_driver)

  driver = webdriver.Chrome(options=chrome_options, service=chrome_service)

  return driver

# Set Wordle game
def set_game(driver):

  driver.get(WORDLE_URL)
  assert "Wordle".lower() in driver.title.lower()

  # Close that beginning modal
  close_elem = driver.find_element(By.CSS_SELECTOR, "div[class^=Modal-module_closeIcon]")
  close_elem.click()

  game_keyboard = driver.find_element(By.CSS_SELECTOR, "div[class^=Keyboard-module_keyboard")

  game_board = []
  for i in range(6):
      game_row = driver.find_elements(By.CSS_SELECTOR, "div[class^=Row-module_row]")[i]
      game_tiles = game_row.find_elements(By.CSS_SELECTOR, "div[class^=Tile-module_tile]")
      game_board.append(game_tiles)

  return game_keyboard, game_board

# Click a letter
def clickLetter(letter, keyboard):
  letterElem = keyboard.find_element(
      By.CSS_SELECTOR, '[data-key="' + letter + '"]')
  letterElem.click()

# Guess a word
def guess_word(word, keyboard):
  for letter in word:
    clickLetter(letter, keyboard)
  clickLetter("↵", keyboard)
  sleep(5)

def clear_word(keyboard):
  for i in range(5):
    clickLetter("←", keyboard)

# Return true for game over
def check_win(driver):
  try:
    driver.find_element(By.CSS_SELECTOR, "div[class^='Stats-module_gameStats'")
    return True
  except:
    return False
  

# Check that guessed word was actually a word
def validate_guess(gameBoard, guessIndex):
    letterElem = gameBoard[guessIndex][0]
    letterState = letterElem.get_attribute('data-state')
    if letterState == "empty":
        return False
    else:
        return True
