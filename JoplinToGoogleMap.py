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

strftime("%Y-%m-%d %H:%M:%S", gmtime())
start = time.time()

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
x=[] #longitudes
y=[] #latitudes
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
              #print(long,lat)
              nb_plot += 1
              if (nb_plot == 1):
                 gmap1 = gmplot.GoogleMapPlotter(float(lat), float(long), 13 )
              x.append(float(long))
              y.append(float(lat))
        except requests.exceptions.HTTPError as e:
             print("Bad HTTP status code:", e)
        except requests.exceptions.RequestException as e:
             print("Network error:", e)
except requests.exceptions.HTTPError as e:
    print("Bad HTTP status code:", e)
except requests.exceptions.RequestException as e:
    print("Network error:", e)

gmap1.scatter( y, x, '#FF0000', size = 10, marker = False )
gmap1.draw("mymap.html")

print ("Number total of request",nb_request)
print ("Number total of pin",nb_plot)
