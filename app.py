from re import S
import requests
import json
from random import randrange
from PIL import Image, ImageFont, ImageDraw, ImageColor

N1_VOCAB_FILE='n1_word_set.json'
N2_VOCAB_FILE='n2_word_set.json'

STORY_WIDTH=1080
STORY_HEIGHT=1920
FONT_PATH='/Users/danblustein/Desktop/BIZ_UDPMincho/BIZUDPMincho-Regular.ttf'
FONT_SIZE=230
IMAGE_MODE='RGB'
BACKGROUND_COLOR=(240,240,240)

def instagramPostImageGenerator():
    pass

def instagramStoryImageGenerator(word: str):
    img = Image.new(IMAGE_MODE, (STORY_WIDTH, STORY_HEIGHT), color = BACKGROUND_COLOR)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    draw = ImageDraw.Draw(img)
    draw.text((300, 300), word, (0,0,0), font=font)
    img.save("bruhmoment.png")

def __instagramImageGenerator():
    pass

def getSentenceFromWord(word: str) -> str:
    # Docs - https://jotoba.de/docs.html#post-/api/search/sentences

    url = 'https://jotoba.de/api/search/sentences'
    body = {'querry': word}
    response = requests.post(url, json=body)
    
    if response.status_code != 200:
        raise Exception(f'Error retrieving response from API. Error: {response.status_code}')
    
    json = response.json()
    noSentencesExistForWord = len(json['sentences']) == 0
    
    if noSentencesExistForWord:
        raise Exception(f'Sentence does not exist for word {word}')
    else:
        firstSentence = json['sentences'][0]['furigana']
        return firstSentence

def randomN1Word() -> str:
    return __randomWord(N1_VOCAB_FILE)

def randomN2Word() -> str:
    return __randomWord(N2_VOCAB_FILE)
    
def __randomWord(file_name: str) -> str:
    file = open(file_name)
    data = json.load(file)
    randomVal = randrange(data['limit'])
    return data['words'][randomVal]['word']

instagramStoryImageGenerator(randomN1Word())

