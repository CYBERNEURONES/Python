

import plistlib
import os
import glob

folder = "Put the name of folder"

import requests
import re
import json
from subprocess import Popen, PIPE
import xml.etree.ElementTree
import xml.etree.ElementTree as ET
from xml.dom import minidom
from bpylist import bplist
import base64

###

#IP
ip = "127.0.0.1"
#Port
port = "41184"
#Token
token = "Put the token"
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
Awesome_UID = "12345678901234567801234567890123"
Awesome_UID_real = ""

payload = {
    "id":Awesome_UID,
    "title":"Awesome Note Import"
}

try:
    resp = requests.post(url_folders, data=json.dumps(payload, separators=(',',':')), headers=headers)
    #time.sleep(1)
    resp.raise_for_status()
    resp_dict = resp.json()
    print(resp_dict)
    print("My ID")
    print(resp_dict['id'])
    Awesome_UID_real = resp_dict['id']
    save = str(resp_dict['id'])
except requests.exceptions.HTTPError as e:
    print("Bad HTTP status code:", e)
except requests.exceptions.RequestException as e:
    print("Network error:", e)

###
nb_picture = 0
order = 0

# Convert to XML
files = os.listdir(folder)
for name in files:
  if name.endswith('.anote'):
    #print(name)
    name2 = os.path.splitext(name)[0]
    my_file = folder+"/"+name2+".xml"
    name = name.replace(" ", "\\ ")
    name = name.replace("(", "\\(")
    name = name.replace(")", "\\)")
    name = name.replace("&", "\\&")
    name2 = name2.replace(" ", "\\ ")
    name2 = name2.replace("(", "\\(")
    name2 = name2.replace(")", "\\)")
    name2 = name2.replace("&", "\\&")
    #print (name2)
    commande = "plutil -convert xml1 "+folder+"/"+name+" -o "+folder+"/"+name2+".xml"
    os.system(commande)
    my_dict = {}
    nb_array = 0
    nb_integer = 0
    nb_real = 0
    nb_string = 0
    flag_ok = 0
    nb_data = 0
    liste_picture = []
    my_timestamp = 0
    my_title = ""
    my_body = ""
    my_id = ""
    my_picture_name = ""
    my_lat = ""
    my_long = ""
    my_address = ""
    for event, elem in ET.iterparse(my_file):
        assert event == 'end'
        if elem.tag == 'array':
            key = elem.text
            nb_array += 1;
        elif elem.tag == 'key':
            value = elem.text
            if (value == 'Version'):
               flag_ok = 1
               #print("ok")
               nb_array = 0
               nb_integer = 0
               nb_real = 0
               nb_string = 0
               nb_data = 0
        elif elem.tag == 'integer':
            nb_integer += 1
            value = elem.text
        elif elem.tag == 'real':
            nb_real += 1
            value = elem.text
            if (flag_ok == 1):
                if (nb_real == 1):
                   my_timestamp = float(value)*1000;
        elif elem.tag == 'string':
            nb_string += 1
            value = elem.text
            if (flag_ok == 1):
                if (nb_string == 2):
                   my_key = value
                   if (value is None):
                      nb_string += 0
                   else:
                      if (value.startswith("Apple")):
                         nb_string += 1
                      elif (value.startswith("Times")):
                         nb_string += 1
                      else:
                         split_list = value.split()
                         if len(split_list) == 3:
                              my_long, my_lat, my_address = value.split("|")
                              print("Address",my_long, my_lat, my_address)
                if (nb_string == 4):
                   my_key = value
                   if (value is None):
                      nb_string += 0
                   else:
                      if (value.startswith("Apple")):
                         nb_string -= 1
                      elif (value.startswith("Times")):
                         nb_string -= 1
                if (nb_string == 5):
                   my_key = value
                   if (value is None):
                      nb_string += 0
                   else:
                      if (value.startswith("Apple")):
                         nb_string -= 2 
                      elif (value.startswith("Times")):
                         nb_string -= 2 
                if (nb_string == 5):
                   my_body = value
                   if (my_body is None):
                       my_body = ""
                   else:
                       my_body = re.sub(r"<@b>", "**", my_body)
                       my_body = re.sub(r"</@b>", "**", my_body)
                       my_body = re.sub(r"<@u>", "*", my_body)
                       my_body = re.sub(r"</@u>", "*", my_body)
                if (nb_string == 6):
                   my_title = value
                   if (my_title is None):
                       my_title = ""
                   elif (len(my_title) == 36 and (' ' not in my_title)):
                       if (len(my_body) > 0):
                           my_title = my_body
                if (nb_string == 7):
                   my_id = value
                   my_id = my_id.replace("-", "")
                   my_id = my_id[0:31]
        elif elem.tag == 'entry':
            my_dict[key] = value
            key = value = None
        elif elem.tag == 'data':
            nb_data += 1
            value = elem.text
            value_clean = re.sub(r" ", "", value)
            value_clean = re.sub(r"\t", "", value_clean)
            value_clean = re.sub(r"\n", "", value_clean)
            nb_picture += 1
            my_picture_name = str(nb_picture)+".jpg"
            liste_picture.append(my_picture_name)
            jpg_recovered = base64.decodestring(value_clean.encode())
            g = open(my_picture_name, "wb")
            g.write(jpg_recovered)
            g.close()
        elem.clear()

    #print("Data:",my_timestamp,",",my_title,",",my_body)
    if (len(my_title) > 150):
       print("Error",my_file);
    print("Filename:",my_file,"Data:",my_timestamp,",",my_title,",",my_id)
    nb_import += 1
    payload_note = {
                "parent_id":Awesome_UID_real,
                "title":my_title,
                "source":my_file,
                "order":nb_import,
                "user_created_time":my_timestamp,
                "user_updated_time":my_timestamp,
                "author":"Awesome Note",
                "body":my_body
}
    if (len(my_address) > 0):
        payload_note_put = {
                "source":my_file,
                "longitude":float(my_long),
                "latitude":float(my_lat),
                "order":nb_import,
                "user_created_time":my_timestamp,
                "user_updated_time":my_timestamp,
                "author":"Awesome Note"
}
    else :
        payload_note_put = {
                "source":my_file,
                "order":nb_import,
                "user_created_time":my_timestamp,
                "user_updated_time":my_timestamp,
                "author":"Awesome Note"
}

    myuid = my_id

    try:
        resp = requests.post(url_notes, json=payload_note)
        resp.raise_for_status()
        resp_dict = resp.json()
        print(resp_dict)
        myuid= resp_dict['id']
        my_id = myuid
    except requests.exceptions.HTTPError as e:
        print("Bad HTTP status code:", e)
        print("payload_note:", payload_note)
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
        print("payload_note:", payload_note_put)
    except requests.exceptions.RequestException as e:
        print("Network error:", e)

    for my_picture_name in liste_picture:
               cmd = "curl -F 'data=@"+my_picture_name+"' -F 'props={\"title\":\""+my_picture_name+"\"}' http://"+ip+":"+port+"/resources?token="+token
               print("Command"+cmd)
               resp = os.popen(cmd).read()
               try:
                  respj = json.loads(resp)
                  print(respj['id'])
                  myuid_picture= respj['id']
               except:
                  print('bad json: ', resp)

               my_body = my_body + "\n  ![" + my_picture_name + "](:/" + myuid_picture + ")   \n";

               payload_note_put = {
                "body":my_body
                }

               try:
                  resp = requests.put(url_notes_put, json=payload_note_put)
                  resp.raise_for_status()
                  resp_dict = resp.json()
                  print(resp_dict)
               except requests.exceptions.HTTPError as e:
                  print("Bad HTTP status code:", e)
                  print("payload_note:", payload_note_put)
               except requests.exceptions.RequestException as e:
                  print("Network error:", e)



