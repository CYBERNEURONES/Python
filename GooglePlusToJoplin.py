#
# Version 3 
# for Python 3
# 
#   ARIAS Frederic
#   Sorry ... It's difficult for me the python :)
#

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

nb_metadata = 0
nb_metadata_import = 0
def month_string_to_number(string):
    m = {
        'janv.': 1,
        'feb.': 2,
        'févr.': 2,
        'mar.': 3,
        'mars': 3,
        'apr.':4,
        'avr.':4,
         'may.':5,
         'mai':5,
         'juin':6,
         'juil.':7,
         'aug.':8,
         'août':8,
         'sept.':9,
         'oct.':10,
         'nov.':11,
         'déc.':12
        }
    s = string.strip()[:5].lower()

    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')

locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
#today = datetime.date.today()
#print(today.strftime('The date :%d %b. %Y à %H:%M:%S UTC'))
from time import strftime,localtime
print(localtime())
print(strftime("%H:%M:%S, %d %b. %Y",localtime()))
date = datetime.strptime('2017-05-04',"%Y-%m-%d")

#Token
ip = "127.0.0.1"
port = "41184"

token = "Put the token here"
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
GooglePlus_UID = "12345678901234567801234567890123"
UID = {}

payload = {
    "id":GooglePlus_UID,
    "title":"GooglePlus Import"
}

try:
    resp = requests.post(url_folders, data=json.dumps(payload, separators=(',',':')), headers=headers)
    resp.raise_for_status()
    resp_dict = resp.json()
    print(resp_dict)
    print("My ID")
    print(resp_dict['id'])
    GooglePlus_UID_real = resp_dict['id']
    save = str(resp_dict['id'])
    UID[GooglePlus_UID]= save
except requests.exceptions.HTTPError as e:
    print("Bad HTTP status code:", e)
except requests.exceptions.RequestException as e:
    print("Network error:", e)

for csvfilename in glob.iglob('Takeout*/**/*.metadata.csv', recursive=True):
  nb_metadata += 1
  print(nb_metadata," ",csvfilename)
  #print("Picture:"+os.path.basename(csvfilename))
  mybasename = os.path.basename(csvfilename)
  mylist = mybasename.split(".")
  myfilename = mylist[0] + "." + mylist[1]
  filename = os.path.dirname(csvfilename)+"/"+myfilename
  my_file = Path(filename)

  myfilename2 = mylist[0] + "." + mylist[1] + ".jpg"
  filename2 = os.path.dirname(csvfilename)+"/"+myfilename2
  my_file2 = Path(filename2)

  myfilename3 = mylist[0] + ".jpg"
  filename3 = os.path.dirname(csvfilename)+"/"+myfilename3
  my_file3 = Path(filename3)

  with open(csvfilename) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if (len(row['description']) > 0):
            print(row['title'], row['description'], row['creation_time.formatted'], row['geo_data.latitude'], row['geo_data.longitude'])
            #date = datetime.strptime(row['creation_time.formatted'], "%d %b %Y à %H:%M:%S %Z").timetuple()
            #print(date)
            mylist2 = row['creation_time.formatted'].split(" ");
            mylist3 = mylist2[4].split(":");
            date = date.replace(hour=int(mylist3[0]), year=int(mylist2[2]), month=month_string_to_number(mylist2[1]), day=int(mylist2[0]))
            timestamp = time.mktime(date.timetuple())*1000
            print(timestamp)
            nb_metadata_import += 1
            mybody = row['description']
            if (len(row['geo_data.latitude']) > 2):
              payload_note = {
                "parent_id":GooglePlus_UID_real,
                "title":row['creation_time.formatted'],
                "source":myfilename,
                "source_url":row['url'],
                "order":nb_metadata_import,
                "body":mybody
                }
              payload_note_put = {
                "latitude":float(row['geo_data.latitude']),
                "longitude":float(row['geo_data.longitude']),
                "source":myfilename,
                "source_url":row['url'],
                "order":nb_metadata_import,
                "user_created_time":timestamp,
                "user_updated_time":timestamp,
                "author":"Google+"
                }
            else:
               payload_note = {
                "parent_id":GooglePlus_UID_real,
                "title":row['creation_time.formatted'],
                "source":myfilename,
                "source_url":row['url'],
                "order":nb_metadata_import,
                "user_created_time":timestamp,
                "user_updated_time":timestamp,
                "author":"Google+",
                "body":mybody
                }
               payload_note_put = {
                "source":myfilename,
                "order":nb_metadata_import,
                "source_url":row['url'],
                "user_created_time":timestamp,
                "user_updated_time":timestamp,
                "author":"Google+"
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
            
            if my_file.is_file():
               cmd = "curl -F 'data=@"+filename+"' -F 'props={\"title\":\""+myfilename+"\"}' http://"+ip+":"+port+"/resources?token="+token
               print("Command"+cmd)
               resp = os.popen(cmd).read()
               try:
                  respj = json.loads(resp)
                  print(respj['id'])
                  myuid_picture= respj['id']
               except:
                  print('bad json: ', resp)

               mybody = row['description'] + "\n  ![" + myfilename + "](:/" + myuid_picture + ")   \n";

               payload_note_put = {
                "body":mybody
                }

               try:
                  resp = requests.put(url_notes_put, json=payload_note_put)
                  resp.raise_for_status()
                  resp_dict = resp.json()
                  print(resp_dict)
               except requests.exceptions.HTTPError as e:
                  print("Bad HTTP status code:", e)
               except requests.exceptions.RequestException as e:
                  print("Network error:", e)

            if my_file2.is_file():
               cmd = "curl -F 'data=@"+filename2+"' -F 'props={\"title\":\""+myfilename2+"\"}' http://"+ip+":"+port+"/resources?token="+token
               print("Command"+cmd)
               resp = os.popen(cmd).read()
               try:
                  respj = json.loads(resp)
                  print(respj['id'])
                  myuid_picture= respj['id']
               except:
                  print('bad json: ', resp)

               mybody = row['description'] + "\n  ![" + myfilename2 + "](:/" + myuid_picture + ")   \n";

               payload_note_put = {
                "body":mybody
                }

               try:
                  resp = requests.put(url_notes_put, json=payload_note_put)
                  resp.raise_for_status()
                  resp_dict = resp.json()
                  print(resp_dict)
               except requests.exceptions.HTTPError as e:
                  print("Bad HTTP status code:", e)
               except requests.exceptions.RequestException as e:
                  print("Network error:", e)

            if my_file3.is_file():
               cmd = "curl -F 'data=@"+filename3+"' -F 'props={\"title\":\""+myfilename3+"\"}' http://"+ip+":"+port+"/resources?token="+token
               print("Command"+cmd)
               resp = os.popen(cmd).read()
               try:
                  respj = json.loads(resp)
                  print(respj['id'])
                  myuid_picture= respj['id']
               except:
                  print('bad json: ', resp)

               mybody = row['description'] + "\n  ![" + myfilename3 + "](:/" + myuid_picture + ")   \n";

               payload_note_put = {
                "body":mybody
                }

               try:
                  resp = requests.put(url_notes_put, json=payload_note_put)
                  resp.raise_for_status()
                  resp_dict = resp.json()
                  print(resp_dict)
               except requests.exceptions.HTTPError as e:
                  print("Bad HTTP status code:", e)
               except requests.exceptions.RequestException as e:
                  print("Network error:", e)

print(nb_metadata)
print(nb_metadata_import)

