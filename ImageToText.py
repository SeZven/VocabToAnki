import cv2, pytesseract
import os
import random

random.seed(0)

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

    print(result)

if __name__ == '__main__':
    for image in IMAGES:
        text = imageToText(image)
