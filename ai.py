#nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer

#machine learning and natural language processing
from difflib import get_close_matches
import spacy

#other
from bs4 import BeautifulSoup
from collections import Counter
from more_itertools import collapse, chunked
import string, requests, re, tldextract


def preprocess(text):
    stop_words = stopwords.words('english')
    text = [WordNetLemmatizer().lemmatize(w).lower() for w in word_tokenize(text) if w not in stop_words]
    text = list(filter(None, [s.translate(s.maketrans('', '', string.punctuation)) for s in text]))
    return text

def input_preprocess(text):
    text = [w.lower() for w in word_tokenize(text)]
    text = list(filter(None, [s.translate(s.maketrans('', '', string.punctuation)) for s in text]))
    return text

def array(text):
    text = text.replace('\n', '. ')
    return [sent for sent in sent_tokenize(text)]

url_list = [
'https://en.wikipedia.org/wiki/Human',
'https://en.wikipedia.org/wiki/Animal',
'https://en.wikipedia.org/wiki/Science',
'https://en.wikipedia.org/wiki/Ancient_history',
'https://en.wikipedia.org/wiki/Post-classical_history',
'https://en.wikipedia.org/wiki/Technology',
'https://en.wikipedia.org/wiki/Electronics',
'https://en.wikipedia.org/wiki/Media_(communication)',
]

dataset = []
topic_list = {}

for url in url_list:
    text = BeautifulSoup(requests.get(url).text, 'html.parser').get_text()
    topic = list(Counter(preprocess(text)))[0:list(preprocess(text)).index(tldextract.extract(url).domain)]
    if wordnet.synsets(topic[0]):
        for h in list(collapse([s.lemma_names() for s in wordnet.synsets(topic[0])[0].hyponyms()])):
            topic_list[h] = url_list.index(url)
    for t in topic:
        topic_list[t] = url_list.index(url)
    print('I have learned about', ' '.join(topic))
    dataset.append(array(text))

print('Dataset complete. Ready for use.')
print('Keyword list:', list(topic_list.keys()))

def response(user_input):
    print('Gathering data...')
    dataset_sims = {}
    nlp = spacy.load('en_core_web_sm')
    for sent in dataset[list(topic_list.values())[list(topic_list.keys()).index(get_close_matches(user_input, list(topic_list.keys()), cutoff=0)[0])]]:
        dataset_sims[sent] = nlp(sent).similarity(nlp(user_input))        
    return list(dataset_sims.keys())[list(dataset_sims.values()).index(max(dataset_sims.values()))]


questions = {'what': 'is', 'where': 'is located', 'when': 'is in the year'}
question_verbs = ['am', 'are', 'is', 'were', 'was', 'did']


while True:
    user_input = input_preprocess(input('>>> '))
    if user_input[0] in questions:
        print(response(' '.join(user_input[[user_input.index(v) for v in question_verbs if v in user_input][0]+1:])+' '+list(questions.values())[list(questions.keys()).index(user_input[0])]))
    if tuple(['tell', 'me', 'about']) in zip(user_input[:], user_input[1:], user_input[2:]):
        print(response(' '.join(user_input)[2:]+' is'))
    
