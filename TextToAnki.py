import os
import genanki
import random

random.seed(0)

# Directory of the programm
SCRIPTDIRECTORY = os.path.dirname(os.path.abspath(__file__))
# Set directory to directory of the programm location + subfolder \Images, where the images 
# are stored to read image
os.chdir(SCRIPTDIRECTORY + "\Texts")


TEXTS = os.listdir()


def textToList(text):
    """
    Turn vocabulary sheet text into string.
    One row consists of an english and the corresponding german vocabulary, devided by an #.
    """


    # Using readline()
    file = open(text, 'r', encoding='utf-8')
    result = []
    while True:

        # Get next line from file and remove \n from line
        line = file.readline().replace("\n", "")
        
 
        # if line is empty
        # end of file is reached
        if not line:
            break

        result.append(line)
        
 
    file.close()
    return result


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

def findQuestionAndAnswer(row):
    """
    The function takes in a row of the vocabulary sheet and returns
    the question and answer, which are split by an #.
    Data: answer # question
    """
    card = []

    row = row.split("#")
    question = row[1]
    answer = row[0]

    card = [question, answer]
    return card


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


def creatAnkiCard(card):
    """
    Creates an anki card from the given data and retuns it.
    """
    question, answer = card

    note = genanki.Note(
    model=my_model,
    fields=[f'{question}', f'{answer}'])

    return note


def createAnkiDeck(cards, image):
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
    anki_questions_file = anki_folder + f"\\vocabulary_{image}.apkg"
    genanki.Package(deck).write_to_file(anki_questions_file)



if __name__ == '__main__':
    for text in TEXTS:
        list = textToList(text)
        cards = creatAnkiData(list)
        createAnkiDeck(cards,text)






