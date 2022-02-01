from distutils.command.config import config
import cv2, pytesseract
import os

# Directory dieses Programms
scriptDirectory = os.path.dirname(os.path.abspath(__file__))
# Setzte Directory auf den diese Programms um Bild aufrufen zu können
os.chdir(scriptDirectory + "\Images")

img = cv2.imread("img(0).png")

pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract-OCR\tesseract.exe"


custom_config = r'--oem 3 --psm 6' #read line by line ( or row by row)
result = pytesseract.image_to_string(img, lang="deu", config=custom_config)

result.splitlines()



print(result)

cards = []
line0 = "bedroom ['bedru:m] Schlafzimmer"

def findQuestionAndAnswer(row):
    """
    The function takes in a row of the vocabulary sheet and returns
    the question and answer
    """

    answer = ""
    question = ""

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


print(findQuestionAndAnswer(line0))