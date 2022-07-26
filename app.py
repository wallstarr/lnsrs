from re import S
import requests
import json
import textwrap
from random import randrange
from PIL import Image, ImageFont, ImageDraw, ImageColor

N1_VOCAB_FILE='n1_word_set.json'
N2_VOCAB_FILE='n2_word_set.json'

STORY_WIDTH=1080
STORY_HEIGHT=1920
FONT_PATH='/Users/danblustein/Desktop/folderlol/BIZUDPMincho-Regular.ttf'

DEFAULT_WORD_FONT_SIZE=200
LONG_WORD_FONT_SIZE=150
FURIGANA_FONT_SIZE=60
MEANING_FONT_SIZE=75
SENTENCE_FONT_SIZE=75
MAX_NUM_OF_EN_CHARS_PER_LINE=20
MAX_NUM_OF_JP_CHARS_PER_LINE=12

IMAGE_MODE='RGB'
BACKGROUND_COLOR=(240,240,240)
BLACK_RGB=(0,0,0)

class Word(object):
    def __init__(self, word, furigana, meaning, sentence):
        self.word = word
        self.furigana = furigana
        self.meaning = meaning
        self.sentence = sentence

def instagramPostImageGenerator():
    pass

def instagramStoryImageGenerator(wordObject: Word):
    
    word = wordObject.word
    furigana = wordObject.furigana
    meaning = wordObject.meaning
    sentence = wordObject.sentence

    img = Image.new(IMAGE_MODE, (STORY_WIDTH, STORY_HEIGHT), color = BACKGROUND_COLOR)
    imgDraw = ImageDraw.Draw(img)

    # Related to the kanji at hand
    wordFontSize = DEFAULT_WORD_FONT_SIZE if len(word) < 7 else LONG_WORD_FONT_SIZE 
    wordFont = ImageFont.truetype(FONT_PATH, wordFontSize)
    word_w, word_h = imgDraw.textsize(word, font=wordFont)
    wordWidthPlacement = (STORY_WIDTH-word_w)/2
    wordHeightPlacement = (STORY_HEIGHT-word_h)/3
    wordPlacement = (wordWidthPlacement, wordHeightPlacement)
    imgDraw.text(wordPlacement, word, fill=BLACK_RGB, font=wordFont)

    # Related to it's furigana
    furiganaFont = ImageFont.truetype(FONT_PATH, FURIGANA_FONT_SIZE)
    furigana_w, furigana_h = imgDraw.textsize(furigana, font=furiganaFont)
    furiganaWidthPlacement = (STORY_WIDTH-furigana_w)/2
    furiganaHeightPlacement = wordHeightPlacement + 250
    furiganaPlacement = (furiganaWidthPlacement, furiganaHeightPlacement)
    imgDraw.text(furiganaPlacement, furigana, fill=BLACK_RGB, font=furiganaFont)

    # Related to it's meaning in English
    meaningFont = ImageFont.truetype(FONT_PATH, MEANING_FONT_SIZE)
    meaningHeightPlacement = furiganaHeightPlacement + 150
    meaningLines = textwrap.wrap(meaning, width=MAX_NUM_OF_EN_CHARS_PER_LINE)
    for meaningLine in meaningLines:
        width, height = imgDraw.textsize(meaningLine, font=meaningFont)
        meaningLinePlacement = ((STORY_WIDTH - width)/2, meaningHeightPlacement)
        imgDraw.text(meaningLinePlacement, meaningLine, fill=BLACK_RGB, font=meaningFont)
        meaningHeightPlacement += 100

    # Related to the sentence that uses the word in question
    sentenceFont = ImageFont.truetype(FONT_PATH, SENTENCE_FONT_SIZE)
    sentenceHeightPlacement = meaningHeightPlacement + 50
    sentenceLines = textwrap.wrap(sentence, width=MAX_NUM_OF_JP_CHARS_PER_LINE)
    for sentenceLine in sentenceLines:
        width, height = imgDraw.textsize(sentenceLine, font=sentenceFont)
        sentenceLinePlacement = ((STORY_WIDTH - width)/2, sentenceHeightPlacement)
        imgDraw.text(sentenceLinePlacement, sentenceLine, fill=BLACK_RGB, font=sentenceFont)
        sentenceHeightPlacement += 100

    # Saving the Image
    img.save("story.png", "PNG")

def __instagramImageGenerator():
    pass

def getSentenceFromWord(word: str) -> str:
    # Docs - https://jotoba.de/docs.html#post-/api/search/sentences
    url = 'https://jotoba.de/api/search/sentences'
    body = {'query': word}
    response = requests.post(url, json=body)
    
    if response.status_code != 200:
        raise Exception(f'Error retrieving response from API. Error: {response.status_code}')
    
    json = response.json()
    noSentencesExistForWord = len(json['sentences']) == 0
    
    if noSentencesExistForWord:
        raise Exception(f'Sentence does not exist for word {word}')
    else:
        firstSentence = json['sentences'][0]['content']
        return firstSentence

def randomN1Word() -> Word:
    return __randomWord(N1_VOCAB_FILE)

def randomN2Word() -> Word:
    return __randomWord(N2_VOCAB_FILE)
    
def __randomWord(file_name: str) -> Word:
    file = open(file_name)
    data = json.load(file)
    randomVal = randrange(data['limit'])
    
    wordObject = data['words'][randomVal]
    word = wordObject['word']
    furigana = wordObject['furigana']
    meaning = wordObject['meaning']
    sentence = getSentenceFromWord(word)

    return Word(word, furigana, meaning, sentence)

instagramStoryImageGenerator(randomN1Word())