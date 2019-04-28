#
# for Python 3
# 
#   ARIAS Frederic
#   Sorry ... It's difficult for me the python :)
#

from time import gmtime, strftime
import time
import json
import requests
from datetime import *
from staticmap import StaticMap, CircleMarker

m = StaticMap(1100, 1100, url_template='http://a.tile.osm.org/{z}/{x}/{y}.png')

codepostal = "06410"
date_inondation = datetime.strptime("2015-10-03",'%Y-%m-%d')
nb_request = 0
nb_plot = 0
after_inondation = 0
before_inondation = 0
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
url_notes = (
    "http://api.cquest.org/dvf?"
    "code_postal="+codepostal
)
try:
    resp = requests.get(url_notes, headers=headers)
    nb_request += 1
    resp.raise_for_status()
    resp_dict = resp.json()
    #print(resp_dict);
    for my_resource in resp_dict['resultats']:
        #print(my_resource)
        long = my_resource.get('lon')
        lat = my_resource.get('lat')
        my_nature = my_resource.get('nature_mutation')
        my_date = datetime.strptime(my_resource.get('date_mutation'),'%Y-%m-%d')
        if (long) and (lat):
           nb_plot += 1
           print("Long:",float(long),"Lat:",float(lat),"Date:",my_date,"Nature",my_nature);
           if my_nature == "Adjudication" : 
            marker = CircleMarker((float(long), float(lat)), '#00FF36', 8)
           else :
            if my_date > date_inondation : 
              marker = CircleMarker((float(long), float(lat)), '#0036FF', 8)
              after_inondation += 1
            else :         
              marker = CircleMarker((float(long), float(lat)), '#FF3600', 8)
              before_inondation += 1
           m.add_marker(marker)
except requests.exceptions.HTTPError as e:
    print("Bad HTTP status code:", e)
except requests.exceptions.RequestException as e:
    print("Network error:", e)

image = m.render(zoom=13)
image.save('mymap_zoom13_col.png')
image = m.render(zoom=14)
image.save('mymap_zoom14_col.png')
image = m.render(zoom=15)
image.save('mymap_zoom15_col.png')

print ("Number total of request",nb_request)
print ("Number total of pin",nb_plot,"Before date",before_inondation,"After date",after_inondation)
