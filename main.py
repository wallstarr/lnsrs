import requests
import json
from random import randrange

N1_VOCAB_FILE='n1_word_set.json'
N2_VOCAB_FILE='n2_word_set.json'

def getSentenceFromWord(word: str) -> str:
    url = 'https://jotoba.de/api/search/sentences'
    body = {'query': word}
    response = requests.post(url, json=body)
    
    if response.status_code != 200:
        raise Exception(response.status_code)
    
    json = response.json()
    noSentencesExistForWord = len(json['sentences']) == 0
    
    if noSentencesExistForWord:
        raise Exception('Sentence does not exist for word ' + word)
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

print(getSentenceFromWord(randomN1Word()))

