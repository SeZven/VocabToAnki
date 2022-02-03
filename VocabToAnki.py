#from distutils.command.config import config
from json.tool import main
from unittest import result
import cv2, pytesseract
import os
import genanki
import random
#from datetime import datetime



# Directory of the programm
SCRIPTDIRECTORY = os.path.dirname(os.path.abspath(__file__))
# Set directory to directory of the programm location + subfolder \Images, where the images 
# are stored to read image
os.chdir(SCRIPTDIRECTORY + "\Images")

# Add pytesseract.exe location
pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract-OCR\tesseract.exe"

CUSTOM_CONFIG = r'--oem 3 --psm 6' #read line by line ( or row by row)

IMAGES = os.listdir()


def imageToText(image):
    """
    Turn vocabulary sheet image into string.
    One row consists of an english and the corresponding german vocabulary.
    """

    img = cv2.imread(image)

    result = pytesseract.image_to_string(img, lang="deu", config=CUSTOM_CONFIG)

    return result.splitlines()


"""
Creat model that defines fields an cards for the type of note (flash card)
"""
model_id = random.randrange(1 << 30, 1 << 31)

#print(model_id)

my_model = genanki.Model(model_id ,
  'Vocabulary',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
  ],
  templates=[
    {
      'name': 'Card type 1',
      'qfmt': '{{Question}}<hr>{{type:Answer}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    },
  ])

#-----------------#

cards = []
#line0 = "bedroom ['bedru:m] Schlafzimmer"

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



#print(cards)

def creatAnkiCard(card):
    """
    Creates an anki card from the given data and retuns it.
    """
    question, answer = card

    note = genanki.Note(
    model=my_model,
    fields=[f'{question}', f'{answer}'])

    return note

    
#creatAnkiCard(cards[0])

def createAnkiDeck(cards):
    """
    Creat anki deck and save it to a file.
    """
    deck_id = random.randrange(1 << 30, 1 << 31) # Every deck needs an id

    #print(deck_id)

    deck = genanki.Deck(deck_id, "Vocabulary")

    for card in cards:

        deck.add_note(creatAnkiCard(card))

    # save card
    anki_folder = SCRIPTDIRECTORY + "\Anki"
    #date = datetime.now()
    anki_questions_file = anki_folder + f"\\vocabulary_{IMAGES[0]}.apkg"
    genanki.Package(deck).write_to_file(anki_questions_file)

result = imageToText(IMAGES[0])
cards = creatAnkiData(result)
createAnkiDeck(cards)

if __name__ == '__main__':
    for image in IMAGES:
        text = i

