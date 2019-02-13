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
import gmplot
from staticmap import StaticMap, CircleMarker

m = StaticMap(1600, 800, url_template='http://a.tile.osm.org/{z}/{x}/{y}.png')

marker = CircleMarker((10, 47), '#0036FF', 3)
m.add_marker(marker)

#Token
ip = "127.0.0.1"
port = "41184"

token = "Put your token here"
nb_request = 0
nb_plot = 0
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
        url_notes2 = (
    "http://"+ip+":"+port+"/notes/"+my_note.get('id')+"?fields=longitude,latitude&"
    "token="+token
)
        try:
           resp2 = requests.get(url_notes2, headers=headers)
           nb_request += 1
           resp2.raise_for_status()
           resp_dict2 = resp2.json()
           #print(resp_dict2)
           long = resp_dict2.get('longitude')
           lat = resp_dict2.get('latitude')
           if (long != '0.00000000'):
              nb_plot += 1
              marker = CircleMarker((float(long), float(lat)), '#0036FF', 12)
              m.add_marker(marker)
        except requests.exceptions.HTTPError as e:
             print("Bad HTTP status code:", e)
        except requests.exceptions.RequestException as e:
             print("Network error:", e)
except requests.exceptions.HTTPError as e:
    print("Bad HTTP status code:", e)
except requests.exceptions.RequestException as e:
    print("Network error:", e)

image = m.render(zoom=1)
image.save('mymap_zoom1.png')
image = m.render(zoom=2)
image.save('mymap_zoom2.png')
image = m.render(zoom=3)
image.save('mymap_zoom3.png')
image = m.render(zoom=4)
image.save('mymap_zoom4.png')
image = m.render(zoom=5)
image.save('mymap_zoom5.png')
image = m.render(zoom=6)
image.save('mymap_zoom6.png')

print ("Number total of request",nb_request)
print ("Number total of pin",nb_plot)
