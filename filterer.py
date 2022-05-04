import math
import os

# Get words from txt file
def get_five_letter_words():
  wordsFile = open("fiveLetterWords.txt", "r")
  fiveLetterWords = [word[0:5] for word in wordsFile]
  wordsFile.close()
  return fiveLetterWords

def get_last_parsed_word():
  wordsFile = open("humanWords.txt", "r")
  fiveLetterWords = [word[0:5] for word in wordsFile]
  wordsFile.close()
  return fiveLetterWords[len(fiveLetterWords) - 1]

def get_progress(words, index):
	currentLetter = words[index][0]
	currentLetterStartIndex = None
	nextLetterStartIndex = len(words)
	
	
	for j in range(0, len(words)):
		if currentLetterStartIndex is None and words[j][0] == currentLetter:
			currentLetterStartIndex = j
		if currentLetterStartIndex is not None and nextLetterStartIndex is None and words[j][0] != currentLetter:
			nextLetterStartIndex = j
			break
	
	progressString = "--------------------------------------------------"
	for k in range(len(progressString)):
		if (index - currentLetterStartIndex) / (nextLetterStartIndex - currentLetterStartIndex) < k / len(progressString):
			progressString = progressString.replace("-", "=", k + 1)
			progressString = progressString[:math.floor(len(progressString)/2)] + " " + str(round(100*(index - currentLetterStartIndex) / (nextLetterStartIndex - currentLetterStartIndex), 1)) + "% " + progressString[math.ceil(len(progressString)/2):]
			break
		elif k == len(progressString) - 1:
			progressString = progressString.replace("-", "=", k + 1)
			progressString = progressString[:math.floor(len(progressString)/2)] + " " + str(round(100*(index - currentLetterStartIndex) / (nextLetterStartIndex - currentLetterStartIndex), 1)) + "% " + progressString[math.ceil(len(progressString)/2):]
	
	totalProgressString = "--------------------------------------------------"
	for k in range(len(totalProgressString)):
		if index / len(words) < k / len(totalProgressString):
			totalProgressString = totalProgressString.replace("-", "=", k + 1)
			totalProgressString = totalProgressString[:math.floor(len(totalProgressString)/2)] + " " + str(round(100*(index / len(words)), 1)) + "% " + totalProgressString[math.ceil(len(totalProgressString)/2):]
			break
		elif k == len(totalProgressString) - 1:
			totalProgressString = totalProgressString.replace("-", "=", k + 1)
			totalProgressString = totalProgressString[:math.floor(len(totalProgressString)/2)] + " " + str(round(100*(index / len(words)), 1)) + "% " + totalProgressString[math.ceil(len(totalProgressString)/2):]

	return "Letter " + currentLetter.upper() + " progress", "(" + progressString + ")", "( " + str(index - currentLetterStartIndex) + " / " + str(nextLetterStartIndex - currentLetterStartIndex) + " )", "Total progress", "(" + totalProgressString + ")", "( " + str(index) + " / " + str(len(words)) + " )"


words = get_five_letter_words()
i = words.index(get_last_parsed_word()) + 1
humanWordsFile = open("humanWords.txt", "a")
while i < len(words):
	word = words[i]
	# os.system("cls")
	progress = get_progress(words, i)
	print("\n\n\n")
	print("{:>20} {:^75} {:^20}".format(progress[0], progress[1], progress[2]))
	print("{:>20} {:^75} {:^20}".format(progress[3], progress[4], progress[5]))
	print("\n\n\n\n\n" + word + "\n\n")
	validation = input("y or empty: ")
	if validation == "w":
		i -= 1
		continue
	elif validation == "exit":
		break
	elif len(validation) > 0:
		humanWordsFile.write(word + "\n")

	i += 1

humanWordsFile.close()
