import pandas as pd
import numpy as np
import re
def printf(x):
    pd.set_option('display.max_info_rows', len(x))
    print(x)
    pd.reset_option('display.max_info_rows')

#read in data
survey2011 = pd.read_csv('Survey Data/2011 Stack Overflow Survey Responses.csv', encoding='ISO-8859-1')
survey2012 = pd.read_csv('Survey Data/2012 Stack Overflow Survey Responses.csv', encoding='ISO-8859-1')
survey2013 = pd.read_csv('Survey Data/2013 Stack Overflow Survey Responses.csv', encoding='ISO-8859-1')
survey2014 = pd.read_csv('Survey Data/2014 Stack Overflow Survey Responses.csv')
survey2015 = pd.read_csv('Survey Data/2015 Stack Overflow  Survey Responses.csv', skiprows=1)
survey2016 = pd.read_csv('Survey Data/2016 Stack Overflow Survey Responses.csv')

# increase index of each data frame
total_records = 0
for yr, df in zip(range(2011,2017),
                  [survey2011, survey2012, survey2013, survey2014, survey2015, survey2016]):
    df['year'] = yr
    df['index'] = np.arange(total_records, total_records+len(df))
    df.set_index('index', inplace=True)
    total_records += len(df)

rename_columns = {
    'What Country or Region do you live in?': "country",
    'What Country do you live in?': "country",
    'Country': 'country',
    'Which US State or Territory do you live in?': "state",
    'How old are you?': 'age',
    'age_range': 'age',
    'Age': 'age',
    'What is your gender?': 'gender',
    'Gender': 'gender',
    'How many years of IT/Programming experience do you have?': "yrs_exp",
    'experience_range': 'yrs_exp',
    'Years IT / Programming Experience': 'yrs_exp',
    'How would you best describe the industry you work in?': "industry",
    'Industry': 'industry',
    'How would you best describe the industry you currently work in?': "industry",
    'Which best describes the size of your company?': "company_size",
    'company_size_range': 'company_size',
    'How many people work for your company?': 'company_size',
    'How many developers are employed at your company?': 'num_developers_company',
    'Which of the following best describes your occupation?': "occupation",
    'Occupation': 'occupation',
    'How likely is it that a recommendation you make will be acted upon?': "influence",
    'What type of project are you developing?': "type_of_project",
    'Including yourself, how many developers are employed at your company?': 'num_developers_company',
    "How large is the team that you work on?": 'team_size',
    'team_size_range': 'team_size',
    'Including bonus, what is your annual compensation in USD?': 'income',
    'Compensation': 'income',
    'salary_range': 'income',
    'Employment Status': 'employment_status',
    'Compensation: midpoint': 'income_midpoint',
    'What is your current Stack Overflow reputation?': 'so_reputation',
}

#2011
survey2011.rename(columns=rename_columns, inplace=True)


tech = ['Which languages are you proficient in?',
'Unnamed: 31',
'Unnamed: 32',
'Unnamed: 33',
'Unnamed: 34',
'Unnamed: 35',
'Unnamed: 36',
'Unnamed: 37',
'Unnamed: 38',
'Unnamed: 39',
'Unnamed: 40',
'Unnamed: 41',
'Unnamed: 42',]

survey2011['UserID'] = np.arange(len(survey2011))

reformat_tech_2011 = survey2011[tech]
reformat_tech_2011 = pd.concat([reformat_tech_2011,
                                reformat_tech_2011['Unnamed: 42'].str.split(', ?', expand=True)],
                               axis = 1)

del(reformat_tech_2011['Unnamed: 42'])

reformat_tech_2011 = reformat_tech_2011.stack()


total_length = len(survey2011)
#2012
survey2012.rename(columns=rename_columns,inplace=True)
survey2012.set_index(np.arange(total_length,total_length+len(survey2012)), inplace=True)
tech = ['Which languages are you proficient in?', 'Unnamed: 23', 'Unnamed: 24',
       'Unnamed: 25', 'Unnamed: 26', 'Unnamed: 27', 'Unnamed: 28',
       'Unnamed: 29', 'Unnamed: 30', 'Unnamed: 31', 'Unnamed: 32',
       'Unnamed: 33', 'Unnamed: 34', 'Unnamed: 35', 'Unnamed: 36']

reformat_tech_2012 = survey2012[tech]
reformat_tech_2012 = pd.concat([reformat_tech_2012,
                                reformat_tech_2012['Unnamed: 36'].str.split(', ?', expand=True)],
                               axis = 1)
del(reformat_tech_2012['Unnamed: 36'])

#remove first row
reformat_tech_2012 = reformat_tech_2012.loc[total_length+1:,:].stack()

total_tech = reformat_tech_2011.append(reformat_tech_2012)

survey2012.drop(tech, axis=1, inplace=True)

#2013
survey2013.rename(columns=rename_columns, inplace=True)
tech = ['Which of the following languages or technologies have you used significantly in the past year?',
       'Unnamed: 57', 'Unnamed: 58', 'Unnamed: 59', 'Unnamed: 60',
       'Unnamed: 61', 'Unnamed: 62', 'Unnamed: 63', 'Unnamed: 64',
       'Unnamed: 65', 'Unnamed: 66', 'Unnamed: 67', 'Unnamed: 68',
       'Unnamed: 69']

other_tech = ['Which technologies are you excited about?',
       'Unnamed: 71', 'Unnamed: 72', 'Unnamed: 73', 'Unnamed: 74',
       'Unnamed: 75', 'Unnamed: 76', 'Unnamed: 77', 'Unnamed: 78',
       'Unnamed: 79', 'Unnamed: 80']

reformat_tech_2013 = survey2013[tech]
reformat_tech_2013 = pd.concat([reformat_tech_2013,
                                reformat_tech_2013['Unnamed: 69'].str.split('(, ?| / )', expand=True)],
                               axis = 1)

del(reformat_tech_2013['Unnamed: 69'])

reformat_tech_2013 = reformat_tech_2013.stack()
total_tech = total_tech.append(reformat_tech_2013)

#2014
survey2014.rename(columns=rename_columns,inplace=True)

tech = ['Which of the following languages or technologies have you used significantly in the past year?',
       'Unnamed: 43', 'Unnamed: 44', 'Unnamed: 45', 'Unnamed: 46',
       'Unnamed: 47', 'Unnamed: 48', 'Unnamed: 49', 'Unnamed: 50',
       'Unnamed: 51', 'Unnamed: 52', 'Unnamed: 53']

reformat_tech_2014 = survey2014[tech]
reformat_tech_2014 = pd.concat([reformat_tech_2014,
                                reformat_tech_2014['Unnamed: 53'].str.split('(, ?| / )', expand=True)],
                               axis = 1)

del(reformat_tech_2014['Unnamed: 53'])

reformat_tech_2014 = reformat_tech_2014.stack()

total_tech = total_tech.append(reformat_tech_2014)

#2015
survey2015.rename(columns=rename_columns,inplace=True)
tech = survey2015.columns[survey2015.columns.str.match('Current Lang & Tech:')]

reformat_tech_2015 = survey2015[tech]
reformat_tech_2015 = pd.concat([reformat_tech_2015,
                                reformat_tech_2015['Current Lang & Tech: Write-In'].str.split('(, ?| / )', expand=True)],
                               axis = 1)

del(reformat_tech_2015['Current Lang & Tech: Write-In'])
reformat_tech_2015 = reformat_tech_2015.stack()


total_tech = total_tech.append(reformat_tech_2015)
#2016
survey2016.rename(columns = rename_columns, inplace=True)

reformat_tech_2016 = survey2016['tech_do']
reformat_tech_2016 = reformat_tech_2016.str.split('; ', expand=True)
reformat_tech_2016 = reformat_tech_2016.stack()
total_tech = total_tech.append(reformat_tech_2016)

pd.DataFrame(total_tech.str.lower().value_counts()).to_csv("languages.csv")

languages_dict = pd.read_csv('languages_dict.csv')


variable_availability = pd.DataFrame(columns=range(2011,2017))

for yr, df in zip(range(2011,2017),
                  [survey2011, survey2012, survey2013, survey2014, survey2015, survey2016]):
    for column in df.columns:
        if not re.match("Unnamed", column):
            variable_availability.loc[column, yr] = '|'.join(df[column][1:5].astype(str))

variable_availability.to_csv("variable_availability.csv")

education = survey2016.education.str.split('; ',expand=True).stack()

import matplotlib.pyplot as plt

education.value_counts().plot(kind='barh', rot=0)
plt.tight_layout()
plt.savefig("output/hist_education.png")

# Cant use a table here because of multiple overlaps:
# If we use a count table on
# wide format, we will have a len(education.unique()) dimensional table




# salary of those without formal eeducation
degrees = ["I'm self-taught",
           'On-the-job training',
           'Online class (e.g. Coursera, Codecademy, Khan Academy, etc.)',
           'Full-time, intensive program (e.g. "boot-camp")',
           'Part-time program (e.g. night school)',
           'Some college coursework in Computer Science (or related field)',
           'B.A. in Computer Science (or related field)',
           'B.S. in Computer Science (or related field)',
           'Masters Degree in Computer Science (or related field)',
           'PhD in Computer Science (or related field)']

education_grid = pd.DataFrame(index=degrees, columns=degrees)

index_slice = pd.IndexSlice
for ed1 in education.unique():
    ix = education[education == ed1].index.get_level_values(0)
    number_with_education = len(ix)
    subset = education.loc[index_slice[ix,:]]
    for ed2 in subset.unique():
        # rows of the dataframe all have the same denominator: number of people with the ed.
        education_grid.loc[ed1,ed2] = np.sum(subset == ed2)/number_with_education

education_grid = education_grid.astype(float)
plt.close()
fig, ax = plt.subplots(figsize=(10,10))
plt.pcolor(education_grid)
plt.yticks(np.arange(0.5, len(education_grid.index), 1), education_grid.index)
plt.xticks(np.arange(0.5, len(education_grid.columns), 1), education_grid.columns, rotation=45, ha='right')
fig.subplots_adjust(bottom=.5,left=0.5)
plt.colorbar()


survey2016['highest_degree'] = "None"

#attempt this with different orderings of degrees
for deg in degrees:
    survey2016.loc[survey2016.education.str.match(re.escape(deg)).fillna(False), 'highest_degree'] = deg

survey2016.groupby('highest_degree')['salary_midpoint'].mean()[degrees].plot(kind='bar')



combined_years_columns = ['income', 'year', 'age', 'country', 'yrs_exp','industry','company_size','occupation']

survey_combined = pd.DataFrame()
for yr, df in zip(range(2011,2017),
                  [survey2011, survey2012, survey2013, survey2014, survey2015, survey2016]):
    df.to_csv("Survey Data/survey%s_cleaned.csv" % yr)
    survey_combined = survey_combined.append(df)

