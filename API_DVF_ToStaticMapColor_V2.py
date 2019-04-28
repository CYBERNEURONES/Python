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
m2 = StaticMap(1100, 1100, url_template='http://a.tile.osm.org/{z}/{x}/{y}.png')

codeinsee = "06018"
date_inondation = datetime.strptime("2015-10-03",'%Y-%m-%d')
nb_request = 0
nb_plot = 0
nb_Vente = 0
nb_Echange = 0
nb_Adjudication = 0
nb_Futur = 0
nb_Expropriation = 0
nb_Autre = 0
after_inondation = 0
before_inondation = 0
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
url_notes = (
    "http://api.cquest.org/dvf?"
    "code_commune="+codeinsee
)
try:
    resp = requests.get(url_notes, headers=headers)
    nb_request += 1
    resp.raise_for_status()
    resp_dict = resp.json()
    for my_resource in resp_dict['resultats']:
        long = my_resource.get('lon')
        lat = my_resource.get('lat')
        my_nature = my_resource.get('nature_mutation')
        my_date = datetime.strptime(my_resource.get('date_mutation'),'%Y-%m-%d')
        if (long) and (lat):
           nb_plot += 1
           print("Long:",float(long),"Lat:",float(lat),"Date:",my_date,"Nature",my_nature);
           if my_nature == "Adjudication" : 
              nb_Adjudication += 1
              marker = CircleMarker((float(long), float(lat)), '#FFFFFF', 6)
              marker2 = CircleMarker((float(long), float(lat)), '#FF0000', 7)
              m2.add_marker(marker2)
           elif my_nature == "Echange" : 
              nb_Echange += 1
              marker = CircleMarker((float(long), float(lat)), '#0036FF', 6)
           elif my_nature == "Vente en l'état futur d'achèvement" :
              nb_Futur += 1
              marker = CircleMarker((float(long), float(lat)), '#FF00FF', 6)
           elif my_nature == "Expropriation" : 
              nb_Expropriation += 1
              marker = CircleMarker((float(long), float(lat)), '#FF0000', 6)
              marker2 = CircleMarker((float(long), float(lat)), '#FF0033', 7)
              m2.add_marker(marker2)
           elif my_nature == "Vente" : 
              nb_Vente += 1
              marker = CircleMarker((float(long), float(lat)), '#00FFFF', 6)
           else :         
              nb_Autre += 1
              marker = CircleMarker((float(long), float(lat)), '#888888', 6)
           m.add_marker(marker)
except requests.exceptions.HTTPError as e:
    print("Bad HTTP status code:", e)
except requests.exceptions.RequestException as e:
    print("Network error:", e)

image = m.render(zoom=13)
image.save('mymap_Biot_zoom13_col.png')
image = m.render(zoom=14)
image.save('mymap_Biot_zoom14_col.png')
image = m.render(zoom=15)
image.save('mymap_Biot_zoom15_col.png')

image = m2.render(zoom=13)
image.save('mymap_Biot_Adjudication_Expro_zoom13_col.png')
image = m2.render(zoom=14)
image.save('mymap_Biot_Adjudication_Expro_zoom14_col.png')
image = m2.render(zoom=15)
image.save('mymap_Biot_Adjudication_Expro_zoom15_col.png')

print ("Number total of request",nb_request)
print ("Number total of pin",nb_plot," Adjudication ",nb_Adjudication," Echange ", nb_Echange, " Vente en l'état futur d'achèvement (Fushia)", nb_Futur, " Expropriation (Rouge)", nb_Expropriation, " Vente (Bleu) ", nb_Vente, " Autre ", nb_Autre)
