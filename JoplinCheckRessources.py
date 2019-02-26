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
from tqdm import tqdm
import hashlib

strftime("%Y-%m-%d %H:%M:%S", gmtime())
start = time.time()

#Token
ip = "127.0.0.1"
port = "41184"
token = "Put the token here"
nb_request = 0
nb_file = 0
nb_double = 0
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
url_resources = (
    "http://"+ip+":"+port+"/resources?"
    "token="+token
)
ALL_MD5 = {}
try:
    resp = requests.get(url_resources, headers=headers)
    nb_request += 1
    resp.raise_for_status()
    resp_dict = resp.json()
    #print(resp_dict)
    for my_resource in resp_dict:
        print(my_resource.get('id'))
        my_id = my_resource.get('id')
        url_one_resources = (
    "http://"+ip+":"+port+"/resources/"+my_resource.get('id')+"/file?"
    "token="+token
)
        try:
            resp2 = requests.get(url_one_resources, headers=headers, stream=True)
            nb_request += 1
            nb_file += 1
            with open("myfile", "wb") as handle:
                for data in tqdm(resp2.iter_content()):
                      handle.write(data)
            my_md5 = hashlib.md5(open('myfile','rb').read()).hexdigest()
            print("MD5:",my_md5)
            if my_id in ALL_MD5:
                 print("Aie")
                 nb_double += 1
                 ALL_MD5[my_id] = my_md5
            else:
                 ALL_MD5[my_id] = my_md5
        except requests.exceptions.HTTPError as e:
            print("Bad HTTP status code:", e)
        except requests.exceptions.RequestException as e:
            print("Network error:", e)
except requests.exceptions.HTTPError as e:
    print("Bad HTTP status code:", e)
except requests.exceptions.RequestException as e:
    print("Network error:", e)

print ("Number total of request",nb_request," Number of file ",nb_file," Number of same file ",nb_double)
