import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import os
plt.style.use('ggplot')

## Create a timeseries graph of users and posts over time on Cross Validated
dusers = pd.read_csv("stats.stackexchange.com/Users.csv")
dposts = pd.read_csv("stats.stackexchange.com/Posts.csv")

dposts['CreationDate'] = pd.to_datetime(dposts['CreationDate'], format='%Y-%m-%dT%H:%M:%S.%f')
dposts['Date'] = dposts.CreationDate.dt.date

dusers.CreationDate = pd.to_datetime(dusers['CreationDate'], format='%Y-%m-%dT%H:%M:%S.%f')
dusers['Date'] = dusers.CreationDate.dt.date
usercounts = dusers.groupby('Date').size()
postcounts = dposts.groupby('Date').size()
posts_users = pd.DataFrame(data={"users": usercounts.cumsum(),
                                 "posts": postcounts},
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

# Create a scatterplot of number of posts under a tag and avg salary of the tag
# by merging stackoverflow metadata with stackoverflow developer survey

survey2016 = pd.read_csv("Survey Data/2016 Stack Overflow Survey Responses.csv")
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
# over time compared to number of survey respondents


country_counts = survey2016.country.value_counts()
country_counts[country_counts>100].plot(kind='bar')

survey2012 = pd.read_csv("Survey Data/2012 Stack Overflow Survey Responses.csv")