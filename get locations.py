import os
import pandas as pd
import numpy as np
import re
import requests
import pickle
import geocoder

#Geocode locations
if not os.path.exists("locations_dict.pickle"):
    locations_dict = {}
    starting_loc = 0
    users = pd.read_csv("stackoverflow/users.csv")
    locations = users.Location.unique()
else:
    with open(r"locations_dict.pickle", "rb") as f:
        locations, locations_dict = pickle.load(f)

with requests.Session() as session:
    locations_dict = {key: value for key, value in locations_dict.items()
                      if str(value) != '<[OVER_QUERY_LIMIT] Google - Geocode>'}
    locations = [x for x in locations if x not in locations_dict]
    for address in locations[:2500]:
        locations_dict[address] = geocoder.google(address, session=session)

# , key = "AIzaSyCwusCGg3MmReI9TsBoFU0mbVriNJJQr2Q"
with open(r"locations_dict.pickle", "wb") as f:
    pickle.dump((locations, locations_dict), f)