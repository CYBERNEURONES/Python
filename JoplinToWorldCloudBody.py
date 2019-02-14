#
# Version 1 
# for Python 3
# 
#   ARIAS Frederic
#   Sorry ... It's difficult for me the python :)
#

from time import gmtime, strftime
import time
import json
import requests
import os
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from wordcloud import WordCloud
import numpy as np
import matplotlib.pyplot as plt

#IP
ip = "127.0.0.1"
#Port
port = "41184"
#Token
token = "Put your token here"
nb_request = 0
my_body = ""
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
url_notes = (
    "http://"+ip+":"+port+"/notes?"
    "token="+token
)
try:
    resp = requests.get(url_notes, headers=headers)
    nb_request += 1
    resp.raise_for_status()
    resp_dict = resp.json()
    #print(resp_dict)
    for my_note in resp_dict:
        #print(my_note.get('id'))
        my_body += my_note.get('body')
except requests.exceptions.HTTPError as e:
    print("Bad HTTP status code:", e)
except requests.exceptions.RequestException as e:
    print("Network error:", e)

# Create a word cloud image
stopwords = stopwords.words('french')
wc = WordCloud(background_color="white", max_words=5000, stopwords=stopwords, contour_width=3, contour_color='firebrick')
wc.generate(my_body)
wc.to_file("jopling_body.png")
plt.figure(figsize=[18,8])
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.show()

