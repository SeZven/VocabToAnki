from distutils.command.config import config
import cv2, pytesseract
import os
import genanki
import random
from datetime import datetime

"""
Turn vocabulary sheet image into string.
One row consists of an english and the corresponding german vocabulary.
"""

# Directory of the programm
scriptDirectory = os.path.dirname(os.path.abspath(__file__))
# Set directory to directory of the programm location + subfolder \Images, where the images 
# are stored to read image
os.chdir(scriptDirectory + "\Images")

img = cv2.imread("img(0).png")

# Add pytesseract.exe location
pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract-OCR\tesseract.exe"

custom_config = r'--oem 3 --psm 6' #read line by line ( or row by row)
result = pytesseract.image_to_string(img, lang="deu", config=custom_config)

result = result.splitlines()

#print(result)

"""
Creat model that defines fields an cards for the type of note (flash card)
"""
model_id = random.randrange(1 << 30, 1 << 31)

print(model_id)

my_model = genanki.Model(model_id ,
  'Knowledge',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
  ],
  templates=[
    {
      'name': 'Card type 1',
      'qfmt': '{{Question}}',
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

cards = creatAnkiData(result)

print(cards)

def creatAnkiCard(card):
    """
    Creates an anki card from the given data.
    """
    question, answer = card

    my_note = genanki.Note(
    model=my_model,
    fields=[f'{question}', f'{answer}'])

    deck_id = random.randrange(1 << 30, 1 << 31)

    print(deck_id)

    my_deck = genanki.Deck(deck_id, "Vocabulary")
    my_deck.add_note(my_note)

    # save card
    anki_folder = scriptDirectory + "\Anki"
    date = datetime.now()
    anki_questions_file = anki_folder + f"\\vocabulary.apkg"
    genanki.Package(my_deck).write_to_file(anki_questions_file)

creatAnkiCard(cards[0])

def createAnkiDeck(cards):
    pass



