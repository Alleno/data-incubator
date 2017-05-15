import xml.etree.ElementTree as ET
import pandas as pd

# For cross validated

users = ET.parse("stats.stackexchange.com/Users.xml")
posts = ET.parse("stats.stackexchange.com/Posts.xml")
badges = ET.parse("stats.stackexchange.com/Badges.xml")

usr_root = users.getroot()
posts_root = posts.getroot()
badges_root = badges.getroot()

dusers = pd.DataFrame.from_dict([x.attrib for x in usr_root])
dposts = pd.DataFrame.from_dict([x.attrib for x in posts_root])
dbadges = pd.DataFrame.from_dict([x.attrib for x in badges_root])

dusers.to_csv("stats.stackexchange.com/Users.csv")
dposts.to_csv("stats.stackexchange.com/Posts.csv")

# For stack overflow

users = ET.parse("stackoverflow/Users.xml")
users = users.getroot()
# TODO: find a better way to turn this into a dataframe
# this is probably not the most efficient way to parse data, since we are creating an intermediate
# list?

users = pd.DataFrame((x.attrib for x in users))
users.to_csv("stackoverflow/users.csv")

