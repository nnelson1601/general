from selenium.webdriver.common.by import By

CORRECT = "correct"
PRESENT = "present"
ABSENT = "absent"

# 5 allows you to guess words with 5 letters previously proven absent 
# 0 does not allow you to reuse absent letters for guessing
GUESS_TOLERANCE = 1 

# Determines how many unique letters must be in the word
GUESS_UNIQUE_LETTERS = 4

class WordleHelper:
  def __init__(self, words, letterScores):
    self.incorrect = ['', '', '', '', '']
    self.present_letters = ''
    self.correct = ['', '', '', '', '']
    self.all_words = words
    self.letter_scores = letterScores
    self.possible_words = [word for word in words]
    self.guess_words = [word for word in words]
    self.score_words()

  # Update the possible letter locations
  def update_letter_possibilities(self, gameBoard, word, prevGuessIndex):
    for i in range(len(word)):
      letter = word[i]
      letterElem = gameBoard[prevGuessIndex][i]
      letterState = letterElem.get_attribute('evaluation')

      if (letterState == CORRECT):
        self.correct[i] = letter
        self.present_letters += letter if letter not in self.present_letters else ''
        self.incorrect[i] = self.incorrect[i].replace(letter, '')
      elif (letterState == PRESENT):
        self.present_letters += letter if letter not in self.present_letters else ''
        self.incorrect[i] += letter if letter not in self.incorrect[i] else ''
      elif (letterState == ABSENT):
        if letter in self.present_letters:
          self.incorrect[i] += letter if letter not in self.incorrect[j] and self.correct[j] != letter else ''
        else:
          for j in range(len(word)):
            self.incorrect[j] += letter if letter not in self.incorrect[j] and self.correct[j] != letter else ''

    return

  # Filter out impossible words
  def filter_out_impossible_words(self):
    newPossibleWords = []

    for word in self.possible_words:
      possibleWord = True
      if not all([letter in word for letter in self.present_letters]):
        possibleWord = False
        continue 
      for i in range(len(word)):
        letter = word[i]
        if letter in self.incorrect[i]:
          possibleWord = False
          break
        if self.correct[i] != '' and self.correct[i] is not letter:
          possibleWord = False
          break

      if possibleWord:
        newPossibleWords.append(word)

    newPossibleWords.sort(key=lambda word: self.word_scores[word], reverse=True)
    self.possible_words = newPossibleWords
    return

  # Generate good words to guess
  def generate_guess_words(self, guessIndex, tolerant=False):
    newGuessWords = []

    if len(self.possible_words) == 1:
      self.guess_words = [self.possible_words[0]]
      return

    for word in self.all_words:
      guessWord = True if len(set(word)) >= (GUESS_UNIQUE_LETTERS if tolerant else 5) else False
      if not guessWord:
        continue

      # Make the guessing a little fuzzy
      # correctLetters = 0
      incorrectLetters = 0
      presentLetters = 0
      for i in range(len(word)):
        letter = word[i]
        if len(self.present_letters) != 5:
          if letter in self.present_letters:
            if presentLetters >= guessIndex + 1:
              guessWord = False
              break
            else:
              presentLetters += 1
          if letter in self.correct:
            guessWord = False
            break
          elif letter in self.incorrect[i]:
            if incorrectLetters >= (GUESS_TOLERANCE if tolerant else 0):
              guessWord = False
              break
            else:
              incorrectLetters += 1

      if guessWord:
        newGuessWords.append(word)

    newGuessWords.sort(key=lambda word: self.word_scores[word], reverse=True)
    self.guess_words = newGuessWords

    return

  def score_words(self):
    scores = {}
    for word in self.all_words:
      score = 0
      lettersUsed = ''
      for letter in word:
        if letter in lettersUsed or any([letter in incorrect for incorrect in self.incorrect]):
          continue
        else:
          lettersUsed += letter
          score += self.letter_scores[letter]
      scores[word] = score
    self.word_scores = scores
    return

  def remove_word(self, word):
    if word in self.all_words:
      self.all_words.remove(word)
    if word in self.possible_words:
      self.possible_words.remove(word)
    if word in self.guess_words:
      self.guess_words.remove(word)
    return
