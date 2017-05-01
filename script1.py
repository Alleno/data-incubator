import xml.etree.ElementTree as ET
import pandas as pd
import geocoder
import requests
import pickle
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
plt.style.use('ggplot')

users = ET.parse("stats.stackexchange.com/Users.xml")
posts = ET.parse("stats.stackexchange.com/Posts.xml")

usr_root = users.getroot()
posts_root = posts.getroot()

dusers = pd.DataFrame.from_dict([x.attrib for x in usr_root])
dposts = pd.DataFrame.from_dict([x.attrib for x in posts_root])

dposts['CreationDate'] = pd.to_datetime(dposts['CreationDate'], format='%Y-%m-%dT%H:%M:%S.%f')

dposts['Date'] = dposts.CreationDate.dt.date

dusers.CreationDate = pd.to_datetime(dusers['CreationDate'], format='%Y-%m-%dT%H:%M:%S.%f')
dusers['Date'] = dusers.CreationDate.dt.date
usercounts = dusers.groupby('Date').size()
postcounts = dposts.groupby('Date').size()
posts_users = pd.DataFrame(data={"users": usercounts.cumsum(),
                                 "posts": postcounts,},
                           index=postcounts.index)

posts_users['users30dayMA'] = posts_users['users'].rolling(window=30).mean()
posts_users['posts30dayMA'] = posts_users['posts'].rolling(window=30).mean()

#graph = pd.rolling_mean(dposts.groupby('Date').size(), window=30).plot(kind='line')
#graph.set(xlabel='Date', ylabel='30 Day Average New Posts', title="Cross Validated Posts Over Time")
#graph.set_xlim(pd.Timestamp('2011-02-15'), pd.Timestamp('2015-07-01'))

fig, ax1 = plt.subplots()
ax1.plot(posts_users.index, posts_users['users30dayMA'], color='b', label="Number of Users")
ax1.set_xlabel('Date')

# Make the y-axis label, ticks and tick labels match the line color.
ax1.set_ylabel('Number of Users', color='b')
ax1.tick_params('y', colors='b')

ax2 = ax1.twinx()
ax2.plot(posts_users.index, posts_users['posts30dayMA'], color='r', label="Posts per Day (30 day MA)")
ax2.set_ylabel('Posts per day', color='r')
ax2.tick_params('y', colors='r')

ax1.set(title="Growth of Cross Validated Over Time")
def update_ylabels(ax):
    ylabels = [format(label, ',.0f') for label in ax.get_yticks()]
    ax.set_yticklabels(ylabels)
update_ylabels(ax1)
fig.tight_layout()
plt.savefig("Growth of Cross Validated over time.png")


for child in usr_root[:2]:
    print(child.tag,child.attrib)


dusers = dusers.apply(pd.to_numeric, errors='ignore')
dposts = dposts.apply(pd.to_numeric, errors='ignore')

# google api has 2500 per day limit
# bing api has ... per limit
unique_addresses = dusers.Location.unique()
google_addresses = unique_addresses[:2500]
bing_addresses = unique_addresses[2500:5000]
leftovers = unique_addresses[5000:]

#Geocode locations
if not os.path.exists("locations_dict.pkl"):
    locations_dict = {}
    with requests.Session() as session:
        for address in google_addresses:
            locations_dict[address] = geocoder.google(address, session=session)

    with requests.Session() as session:
        for address in bing_addresses:
            locations_dict[address] = geocoder.bing(address, session=session)

    with requests.Session() as session:
        for address in leftovers:
            locations_dict[address] = geocoder.osm(address, session=session)

    pickle.dump(locations_dict, "locations_dict.pkl")

else:
    pickle.load("locations_dict.pkl")


with requests.Session() as session:
    for address in bing_addresses:
        locations_dict[address] = geocoder.osm(address, session=session)


with requests.Session() as session:
    for address in leftovers:
        locations_dict[address] = geocoder.osm(address, session=session)




