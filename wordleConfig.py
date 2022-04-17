from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
from time import sleep

WORDLE_URL = 'https://www.nytimes.com/games/wordle/index.html'
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

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
  wordsFile = open("fiveLetterWords.txt", "r")
  fiveLetterWords = [word[0:5] for word in wordsFile]
  wordsFile.close()
  return fiveLetterWords

def write_five_letter_words(words):
	wordsFile = open("fiveLetterWords.txt", "w")
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
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--window-size=720x480")
  chrome_options.add_argument('--log-level=1')

  # download Chrome Webdriver  
  # https://sites.google.com/a/chromium.org/chromedriver/download
  # put driver executable file in the script directory
  chrome_driver = os.path.join(os.getcwd(), "chromedriver")
  chrome_service = Service(chrome_driver)

  driver = webdriver.Chrome(options=chrome_options, service=chrome_service)
  
  return driver

# Set Wordle game
def set_game(driver):

  driver.get(WORDLE_URL)
  assert "Wordle".lower() in driver.title.lower()

  def expand_shadow_element(element):
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
    return shadow_root

  shadow_root_game_app = expand_shadow_element(driver.find_element(By.TAG_NAME, "game-app"))

  # Close that beginning modal
  shadow_root_game_modal = expand_shadow_element(shadow_root_game_app.find_element(By.TAG_NAME, "game-modal"))
  close_elem = shadow_root_game_modal.find_element(By.CLASS_NAME, "close-icon")
  close_elem.click()

  shadow_root_game_keyboard = expand_shadow_element(shadow_root_game_app.find_element(By.TAG_NAME, "game-keyboard"))

  game_board = []
  for i in range(6):
      shadow_root_game_row = expand_shadow_element(shadow_root_game_app.find_elements(By.TAG_NAME, "game-row")[i])
      game_tiles = shadow_root_game_row.find_elements(By.TAG_NAME, "game-tile")
      game_board.append(game_tiles)

  return shadow_root_game_keyboard, game_board

# Click a letter
def clickLetter(letter, keyboard):
  letterElem = keyboard.find_element(By.CSS_SELECTOR, '[data-key="' + letter + '"]')
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

# Check for win
def check_win(driver):
  gameWon = False
  def expand_shadow_element(element):
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
    return shadow_root

  shadow_root_game_app = expand_shadow_element(driver.find_element(By.TAG_NAME, "game-app"))
  shadow_root_game_modal_host = shadow_root_game_app.find_element(By.TAG_NAME, "game-modal")
  if shadow_root_game_modal_host.get_attribute("open"):
    gameWon = True

    # Close end modal
    shadow_root_game_modal = expand_shadow_element(shadow_root_game_app.find_element(By.TAG_NAME, "game-modal"))
    close_elem = shadow_root_game_modal.find_element(By.CLASS_NAME, "close-icon")
    close_elem.click()

  return gameWon

# Check that guessed word was actually a word
def validate_guess(gameBoard, guessIndex):
    letterElem = gameBoard[guessIndex][0]
    letterState = letterElem.get_attribute('evaluation')
    if letterState is None:
        return False
    else:
        return True