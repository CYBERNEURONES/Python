#
# Version 1 
# for Python 3
# 
#   ARIAS Frederic
#   Sorry ... It's difficult for me the python :)
#

import feedparser
from os import listdir
from pathlib import Path
import glob
import csv
import locale
import os
import time
from datetime import datetime
import json
import requests

#Token
ip = "127.0.0.1"
port = "41184"
token = "Put your token here"
nb_import = 0;
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

url_notes = (
    "http://"+ip+":"+port+"/notes?"
    "token="+token
)
url_folders = (
    "http://"+ip+":"+port+"/folders?"
    "token="+token
)
url_tags = (
    "http://"+ip+":"+port+"/tags?"
    "token="+token
)
url_ressources = (
    "http://"+ip+":"+port+"/ressources?"
    "token="+token
)

#Init
Wordpress_UID = "12345678901234567801234567890123"
UID = {}

payload = {
    "id":Wordpress_UID,
    "title":"Wordpress Import"
}

try:
    resp = requests.post(url_folders, data=json.dumps(payload, separators=(',',':')), headers=headers)
    resp.raise_for_status()
    resp_dict = resp.json()
    print(resp_dict)
    print("My ID")
    print(resp_dict['id'])
    Wordpress_UID_real = resp_dict['id']
    save = str(resp_dict['id'])
    UID[Wordpress_UID]= save
except requests.exceptions.HTTPError as e:
    print("Bad HTTP status code:", e)
except requests.exceptions.RequestException as e:
    print("Network error:", e)

feed = feedparser.parse("http://www.cyber-neurones.org/feed/")

feed_title = feed['feed']['title']
feed_entries = feed.entries

numero = -2
nb_entries = 1
nb_metadata_import = 1

while nb_entries > 0 : 
  print ("----- Page ",numero,"-------")
  numero += 2
  url = "http://www.cyber-neurones.org/feed/?paged="+str(numero)
  feed = feedparser.parse(url)
  feed_title = feed['feed']['title']
  feed_entries = feed.entries
  nb_entries = len(feed['entries'])
  for entry in feed.entries:
     nb_metadata_import += 1
     my_title = entry.title
     my_link = entry.link
     article_published_at = entry.published # Unicode string
     article_published_at_parsed = entry.published_parsed # Time object
     article_author = entry.author
     timestamp = time.mktime(entry.published_parsed)*1000
     print("Published at "+article_published_at)
     my_body = entry.description
     payload_note = {
         "parent_id":Wordpress_UID_real,
         "title":my_title,
         "source":"Wordpress",
         "source_url":my_link,
         "order":nb_metadata_import,
         "user_created_time":timestamp,
         "user_updated_time":timestamp,
         "author":article_author,
         "body_html":my_body
         }
     payload_note_put = {
         "source":"Wordpress",
         "order":nb_metadata_import,
         "source_url":my_link,
         "user_created_time":timestamp,
         "user_updated_time":timestamp,
         "author":article_author
         }

     try:
         resp = requests.post(url_notes, json=payload_note)
         resp.raise_for_status()
         resp_dict = resp.json()
         print(resp_dict)
         print(resp_dict['id'])
         myuid= resp_dict['id']
     except requests.exceptions.HTTPError as e:
         print("Bad HTTP status code:", e)
     except requests.exceptions.RequestException as e:
         print("Network error:", e)

     url_notes_put = (
    "http://"+ip+":"+port+"/notes/"+myuid+"?"
    "token="+token
)
     try:
         resp = requests.put(url_notes_put, json=payload_note_put)
         resp.raise_for_status()
         resp_dict = resp.json()
         print(resp_dict)
     except requests.exceptions.HTTPError as e:
         print("Bad HTTP status code:", e)
     except requests.exceptions.RequestException as e:
         print("Network error:", e)


