#
# Version 5 
# for Python 3
# 
#   ARIAS Frederic
#   Sorry ... It's difficult for me the python :)
#

import xml.etree.ElementTree as etree
from time import gmtime, strftime
import time
import json
import requests
import os

strftime("%Y-%m-%d %H:%M:%S", gmtime())
start = time.time()

#Token
ip = "127.0.0.1"
port = "41184"
#token = "ABCD123ABCD123ABCD123ABCD123ABCD123"
token = "bcf7475af70806df3e0b88dd10fcf88971e7088e3116e754e08d8a526ceeaeeb3d95d424330aab10c283eeddb7fc9f24c95472af626c03980eedfbb8d514cdeb"
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
Diaro_UID = "12345678901234567801234567890123"
Lat = {}
Lng = {}
UID = {} 
TAGS = {}
Lat[""] = ""
Lng[""] = ""

payload = {
    "id":Diaro_UID,
    "title":"Diaro Import"
}

try:
    #resp = requests.post(url_folders, json=payload)
    resp = requests.post(url_folders, data=json.dumps(payload, separators=(',',':')), headers=headers)
    #time.sleep(1)
    resp.raise_for_status()
    resp_dict = resp.json()
    print(resp_dict)
    print("My ID")
    print(resp_dict['id'])
    Diaro_UID_real = resp_dict['id']
    save = str(resp_dict['id'])
    UID[Diaro_UID]= save
except requests.exceptions.HTTPError as e:
    print("Bad HTTP status code:", e)
except requests.exceptions.RequestException as e:
    print("Network error:", e)

print("Start : Parse Table")
tree = etree.parse("./DiaroBackup.xml")
for table in tree.iter('table'):
    name = table.attrib.get('name')
    print(name)
    myorder = 1
    for r in table.iter('r'):
         myuid = ""
         mytitle = ""
         mylat = ""
         mylng = ""
         mytags = ""
         mydate = ""
         mydate_ms = 0;
         mytext = ""
         myfilename = ""
         myfolder_uid = Diaro_UID
         mylocation_uid = ""
         myprimary_photo_uid = ""
         myentry_uid = ""
         myorder += 1
         nb_import += 1
         for subelem in r:
             print(subelem.tag)
             if (subelem.tag == 'uid'):
                 myuid = subelem.text
                 print ("myuid",myuid)
             if (subelem.tag == 'entry_uid'):
                 myentry_uid = subelem.text
                 print ("myentry_uid",myentry_uid)
             if (subelem.tag == 'primary_photo_uid'):
                 myprimary_photo_uid = subelem.text
                 print ("myprimary_photo_uid",myprimary_photo_uid)
             if (subelem.tag == 'folder_uid'):
                 myfolder_uid = subelem.text
                 print ("myfolder_uid",myfolder_uid)
             if (subelem.tag == 'location_uid'):
                 mylocation_uid = subelem.text
                 print ("mylocation_uid",mylocation_uid)
             if (subelem.tag == 'date'):
                 mydate = subelem.text
                 mydate_ms = int(mydate)
                 print ("mydate",mydate," in ms",mydate_ms)
             if (subelem.tag == 'title'):
                 mytitle = subelem.text
                 print ("mytitle",mytitle)
             if (subelem.tag == 'lat'):
                 mylat = subelem.text
                 print ("mylat",mylat)
             if (subelem.tag == 'lng'):
                 mylng = subelem.text
                 print ("mylng",mylng)
             if (subelem.tag == 'tags'):
                 mytags = subelem.text
                 if mytags:
                    mytags[1:]
                 print ("mytags",mytags)
             if (subelem.tag == 'text'):
                 mytext = subelem.text
                 print ("mytext",mytext)
                 #if type(mytext) == str:
                       #mytext = mytext.encode('utf8')
             if (subelem.tag == 'filename'):
                 myfilename = subelem.text
                 print ("myfilename",myfilename)
                 
         if (name == 'diaro_folders'):
            payload_folder = {
  "id":myuid,
  "title":mytitle,
  "parent_id":Diaro_UID_real
}
            print(payload_folder)
            try:
                #resp = requests.post(url_folders, json=payload_folder)
                resp = requests.post(url_folders, data=json.dumps(payload_folder,separators=(',',':')), headers=headers)
                resp.raise_for_status()
                resp_dict = resp.json()
                print(resp_dict)
                print(resp_dict['id'])
                save = str(resp_dict['id']) 
                UID[myuid]= save
            except requests.exceptions.HTTPError as e:
                print("Bad HTTP status code:", e)
            except requests.exceptions.RequestException as e:
                print("Network error:", e)

         if (name == 'diaro_tags'):
            payload_tags = {
                "id":myuid,
                "title":mytitle
            }
            try:
                #resp = requests.post(url_tags, json=payload_tags)
                resp = requests.post(url_tags, data=json.dumps(payload_tags,separators=(',',':')), headers=headers)
                #time.sleep(1)
                resp.raise_for_status()
                resp_dict = resp.json()
                print(resp_dict)
                print(resp_dict['id'])
                UID[myuid]= resp_dict['id']
                TAGS[myuid] = mytitle
            except requests.exceptions.HTTPError as e:
                print("Bad HTTP status code:", e)
            except requests.exceptions.RequestException as e:
                print("Network error:", e)

         if (name == 'diaro_attachments'):
            print("Push : "+myfilename)
            filename = "media/photo/" + myfilename
            print("----------0-----------")

            cmd = "curl -F 'data=@"+filename+"' -F 'props={\"title\":\""+myfilename+"\"}' http://"+ip+":"+port+"/resources?token="+token
            resp = os.popen(cmd).read()
            respj = json.loads(resp)
            print(respj['id'])
            UID[myuid]= respj['id']

            print("Link : ",myuid," => ",myentry_uid," // ",UID[myuid]+" => ",UID[myentry_uid])
            time.sleep(1)

            # Not possible : sniff !
            #cmd = "curl -X PUT http://"+ip+":"+port+"/ressources/"+UID[myuid]+"/notes/"+UID[myentry_uid]+"?token="+token
            #resp = os.popen(cmd).read()
            #print (resp)

            url_link = (
               "http://"+ip+":"+port+"/notes/"+UID[myentry_uid]+"?"
               "token="+token
               )
            try:
               resp = requests.get(url_link)
               resp.raise_for_status()
               resp_dict = resp.json()
               print(resp_dict)
               mybody= resp_dict['body']
            except requests.exceptions.HTTPError as e:
               print("Bad HTTP status code:", e)
            except requests.exceptions.RequestException as e:
               print("Network error:", e)

            mybody = mybody + "\n  ![" + myfilename + "](:/" + UID[myuid] + ")   \n";
            payload_note = {
                "body":mybody
            }
            try:
               resp = requests.put(url_link, json=payload_note)
               resp.raise_for_status()
               resp_dict = resp.json()
               print(resp_dict)
            except requests.exceptions.HTTPError as e:
               print("Bad HTTP status code:", e)
            except requests.exceptions.RequestException as e:
               print("Network error:", e)

         if (name == 'diaro_locations'):
              Lat[myuid] = mylat
              Lng[myuid] = mylng

         if (name == 'diaro_entries'):
            if not mytext:
                  mytext = ""
            if not myfolder_uid:
                  myfolder_uid = Diaro_UID
            if not mytags:
                  mytags = ""
            if not mylocation_uid:
                  mylocation_uid = ""
            mytext = mytext.replace("'", "")
            mytitle = mytitle.replace("'", "")
            mytext = mytext.strip("\'")
            mytitle = mytitle.strip("\'")
            mytext = mytext.strip('(')
            mytitle = mytitle.strip('(')
            listtags = mytags.split(",")
            new_tagslist = "";
            for uid_tags in listtags:
                 if (len(uid_tags) > 2):
                        if uid_tags in UID:
                             new_tagslist = new_tagslist + TAGS[uid_tags] + ",";
            print ("TAGS",mytags,"==>",new_tagslist);
            if (len(Lat[mylocation_uid]) > 2):
              payload_note = {
                "id":myuid,
                "tags":new_tagslist,
                "parent_id":UID[myfolder_uid],
                "title":mytitle,
                "source":myuid,
                "order":myorder,
                "body":mytext 
                }
              payload_note_put = {
                "latitude":float(Lat[mylocation_uid]),
                "longitude":float(Lng[mylocation_uid]),
                "source":myuid,
                "order":myorder,
                "user_created_time":mydate_ms,
                "user_updated_time":mydate_ms,
                "author":"Diaro"
                }
            else:
               payload_note = {
                "id":myuid,
                "tags":new_tagslist,
                "parent_id":UID[myfolder_uid],
                "title":mytitle,
                "source":myuid,
                "order":myorder,
                "user_created_time":mydate_ms,
                "user_updated_time":mydate_ms,
                "author":"Diaro",
                "body":mytext
                }
               payload_note_put = {
                "source":myuid,
                "order":myorder,
                "user_created_time":mydate_ms,
                "user_updated_time":mydate_ms,
                "author":"Diaro"
                }


            url_notes_put = (
    "http://"+ip+":"+port+"/notes/"+myuid+"?"
    "token="+token
)
            try:
                resp = requests.post(url_notes, json=payload_note)
                #resp = requests.post(url_notes, data=json.dumps(payload_note,separators=(',',':')), headers=headers)
                #time.sleep(1)
                resp.raise_for_status()
                resp_dict = resp.json()
                print(resp_dict)
                print(resp_dict['id'])
                UID[myuid]= resp_dict['id']
            except requests.exceptions.HTTPError as e:
                print("Bad HTTP status code:", e)
            except requests.exceptions.RequestException as e:
                print("Network error:", e)

            try:
                resp = requests.put(url_notes_put, json=payload_note_put)
                #time.sleep(1)
                resp.raise_for_status()
                resp_dict = resp.json()
                print(resp_dict)
                UID[myuid]= resp_dict['id']
            except requests.exceptions.HTTPError as e:
                print("Bad HTTP status code:", e)
            except requests.exceptions.RequestException as e:
                print("Network error:", e)
 
            print ("------------- Note -----------------")

print("End : Parse Diaro")

strftime("%Y-%m-%d %H:%M:%S", gmtime())
done = time.time()
elapsed = done - start
print(elapsed)
print(nb_import)

# END : Ouf ...
