import pandas as pd
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import re
import requests
import matplotlib.pyplot as plt
plt.style.use('ggplot')

# Create a scatterplot of number of posts under a tag and avg salary of the tag
# by merging stackoverflow metadata with stackoverflow developer survey

survey2016 = pd.read_csv("2016 Stack Overflow Survey Results/2016 Stack Overflow Survey Results/2016 Stack Overflow Survey Responses.csv")
tags = ET.parse("stackoverflow/Tags.xml")
tags = tags.getroot()

tags = pd.DataFrame.from_dict([x.attrib for x in tags])
tags = tags.apply(pd.to_numeric, errors='ignore')
unique_tags = tags.TagName.unique()

survey2016['tags'] = survey2016.tech_do.str.lower() #.str.split("; *")

plotting_tags = tags.loc[tags.Count > 10000, :]
plotting_tags.loc[:, 'avg_salary'] = np.NaN
plotting_tags = plotting_tags.reset_index()

# TODO: don't use a loop here
# TODO: make sure to do a better job cleaning the tags before passing in
for i in range(len(plotting_tags)):
    tag = plotting_tags.loc[i, 'TagName']
    regex = re.escape(tag)
    print(tag)
    plotting_tags.loc[i, 'avg_salary'] = survey2016.loc[survey2016.tags.str.contains(regex).fillna(False), 'salary_midpoint'].mean()

plt_tags = plotting_tags.loc[~plotting_tags.avg_salary.isnull()]
fig, ax = plt.subplots()

plt_tags.plot('Count', 'avg_salary', kind='scatter', ax=ax)

for k, v in plt_tags.iterrows():
    ax.annotate(plt_tags.loc[k, 'TagName'], plt_tags.loc[k, ['Count', 'avg_salary']])

plt.show()

# I'm not an expert at matplotlib so the graphics might be somewhat lacking
fig, ax = plt.subplots()
ax.scatter(plt_tags.Count, plt_tags.avg_salary)
ax.set(xlabel='Number of Posts', ylabel='Average Salary in 2016', title="Stack Overflow Posts And Salary")
for k, v in plt_tags.iterrows():
    ax.annotate(plt_tags.loc[k, 'TagName'], plt_tags.loc[k, ['Count', 'avg_salary']])

plt.savefig("salary_vs_posts.png")

# Create a simple time series graph showing the growth of stackoverflow
# over time

users = ET.parse("stackoverflow/Users.xml")
users = users.getroot()
# TODO: find a better way to turn this into a dataframe
# this is probably not the most efficient way to parse data, since we are creating an intermediate
# list?
users = pd.DataFrame.from_dict([x.attrib for x in users])
