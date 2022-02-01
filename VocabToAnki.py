from distutils.command.config import config
import cv2, pytesseract
import os
import genanki
import random

"""
Turn vocabulary sheet image into text.
One row consists of an english and the corresponding german vocabulary.
"""

# Directory of the programm
scriptDirectory = os.path.dirname(os.path.abspath(__file__))
# Set directory to directory of the programm location + subfolder \Images, where the images 
# are stored to read image
os.chdir(scriptDirectory + "\Images")

img = cv2.imread("img(0).png")

pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract-OCR\tesseract.exe"


custom_config = r'--oem 3 --psm 6' #read line by line ( or row by row)
result = pytesseract.image_to_string(img, lang="deu", config=custom_config)

result = result.splitlines()



#print(result)

cards = []
line0 = "bedroom ['bedru:m] Schlafzimmer"

def findQuestionAndAnswer(row):
    """
    The function takes in a row of the vocabulary sheet and returns
    the question and answer.
    """

    answer = ""
    question = ""
    card = []

    position = 0
    for char in row:

        if char == "[":
            answer = row[0:position-1]
        if char == "]":
            question = row[position+2:]
            card = [question,answer]
            break

        position += 1
    
    return card


#print(findQuestionAndAnswer(line0))

def creatAnkiData(data):
    """
    The fuction take in the vocabulary sheet and turns it into
    a list of [question, answer] and removes empty rows.
    """
    cards = []
    for row in data:
        #print(row)
        cards.append(findQuestionAndAnswer(row))
    cards = [x for x in cards if x != []] #remove empty lines
    return cards

cards = creatAnkiData(result)

print(cards)

def creatAnkiDeck(cards):
    pass
