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
import sqlite3
import re

#conn = sqlite3.connect('my_db.db')
find_this = "\(:/"

#c = conn.cursor()
#c.execute('''DROP TABLE LINK''')
#conn.commit()
#c.execute('''CREATE TABLE LINK (ID_NOTE text, ID_RESOURCE text, CHECKSUM_MD5 text)''')
#conn.commit()

#IP
ip = "127.0.0.1"
port = "41184"
token = "Put token here"
nb_request = 0
my_body = ""
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
url_notes = (
    "http://"+ip+":"+port+"/notes?"
    "token="+token
)
nb_total_ressource = 0
nb_local_ressource = 0
ALL_ID = {}
try:
    resp = requests.get(url_notes, headers=headers)
    nb_request += 1
    resp.raise_for_status()
    resp_dict = resp.json()
    #print(resp_dict)
    for my_note in resp_dict:
        nb_local_ressource = 0
        my_body = my_note.get('body')
        my_ressource = [m.start() for m in re.finditer(find_this, my_body)]
        for my_ressource_x in my_ressource:
             nb_total_ressource += 1
             nb_local_ressource += 1
             my_ressource_id = my_body[my_ressource_x+3:my_ressource_x+32+3]
             print(nb_local_ressource,":",my_note.get('id'),":",my_ressource_id)
             ALL_ID[my_ressource_id]=my_note.get('id')
             
             #c.execute(sql_request)
             #conn.commit()
except requests.exceptions.HTTPError as e:
    print("Bad HTTP status code:", e)
except requests.exceptions.RequestException as e:
    print("Network error:", e)

nb_keep = 0
nb_remove = 0
url_resources = (
    "http://"+ip+":"+port+"/resources?"
    "token="+token
)
try:
    resp = requests.get(url_resources, headers=headers)
    nb_request += 1
    resp.raise_for_status()
    resp_dict = resp.json()
    #print(resp_dict)
    for my_resource in resp_dict:
        my_id = my_resource.get('id')
        if my_id in ALL_ID:
            print("Keep for notes",ALL_ID[my_id])
            nb_keep += 1
        else:
            print("Remove");
            nb_remove += 1
            url_resources_delete = (
    "http://"+ip+":"+port+"/resources/"+my_id+"?"
    "token="+token
)
            try:
                 resp2 = requests.delete(url_resources_delete, headers=headers)
                 resp.raise_for_status()
                 nb_request += 1
            except requests.exceptions.HTTPError as e:
                 print("Bad HTTP status code:", e)
            except requests.exceptions.RequestException as e:
                 print("Network error:", e)
except requests.exceptions.HTTPError as e:
    print("Bad HTTP status code:", e)
except requests.exceptions.RequestException as e:
    print("Network error:", e)

#conn.close()
print("nb_request",nb_request,"nb_total_ressource : ",nb_total_ressource," nb_local_ressource : ",nb_local_ressource)
print("nb_keep",nb_keep,"nb_remove",nb_remove);
