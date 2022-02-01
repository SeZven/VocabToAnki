from distutils.command.config import config
import cv2, pytesseract
import os

# Directory dieses Programms
scriptDirectory = os.path.dirname(os.path.abspath(__file__))
# Setzte Directory auf den diese Programms um Bild aufrufen zu können
os.chdir(scriptDirectory + "\Images")

img = cv2.imread("img(0).png")

pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract-OCR\tesseract.exe"


custom_config = r'--oem 3 --psm 6' #read line by line
result = pytesseract.image_to_string(img, lang="deu", config=custom_config)

result.splitlines()



print(result)


card = "bedroom ['bedru:m] Schlafzimmer"
answer = ""
question = ""
cards = []

position = 0
for char in card:

    if char == "[":
        answer = card[0:position-1]
    if char == "]":
        question = card[position+2:]
        cards.append([question,answer])
        break

    position += 1
    


print(cards)