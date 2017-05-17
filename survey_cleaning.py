import pandas as pd
import numpy as np
import re
import pickle
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
"""
education.value_counts().plot(kind='barh', rot=0)
plt.tight_layout()
plt.savefig("output/hist_education.png")
"""
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
"""
plt.close()
fig, ax = plt.subplots(figsize=(10,10))
plt.pcolor(education_grid)
plt.yticks(np.arange(0.5, len(education_grid.index), 1), education_grid.index)
plt.xticks(np.arange(0.5, len(education_grid.columns), 1), education_grid.columns, rotation=45, ha='right')
fig.subplots_adjust(bottom=.5,left=0.5)
plt.colorbar()

"""
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
    for col in combined_years_columns:
        if col not in df.columns:
            df[col] = np.NaN
    survey_combined = survey_combined.append(df[combined_years_columns])

# TODO: Incomes are truncated, some years have higher ranges
# use some kind of hazard model to estimate?
# TODO: fix Other (please specify) category in 2016

income_dict = {'$80,000 - $100,000': 90000,
 '$20,000 - $40,000': 30000,
 '$60,000 - $80,000': 70000,
 '$40,000 - $60,000': 50000,
 '>$140,000': 160000,
 '$100,000 - $120,000': 110000,
 '<$20,000': 30000,
 '$120,000 - $140,000': 130000,
 'Less than $20,000': 10000,
 '$140,000 - $160,000': 150000,
 'More than $160,000': 180000,
 '$40,000 - $50,000': 45000,
 'Less than $10,000': 5000,
 'More than $200,000': 220000,
 '$10,000 - $20,000': 15000,
 '$90,000 - $100,000': 95000,
 '$30,000 - $40,000': 35000,
 '$20,000 - $30,000': 25000,
 '$70,000 - $80,000': 75000,
 '$80,000 - $90,000': 85000,
 '$50,000 - $60,000': 55000,
 '$60,000 - $70,000': 65000,
 '$140,000 - $150,000': 145000,
 '$130,000 - $140,000': 135000,
 '$100,000 - $110,000': 105000,
 '$110,000 - $120,000': 115000,
 '$160,000 - $170,000': 165000,
 '$180,000 - $190,000': 185000,
 '$120,000 - $130,000': 110000,
 '$150,000 - $160,000': 155000,
 '$190,000 - $200,000': 195000,
 '$170,000 - $180,000': 175000}

survey_combined['salary_midpoint'] = survey_combined.income.map(income_dict)

exper = \
    {'<2',
     '41310', '41435', '11', '41070', '40944',
       '6/10/2013', '2/5/2013', '6/10/2014', '2/5/2014', '2 - 5 years',
       '1 - 2 years', '6 - 10 years', '11+ years', 'Less than 1 year'}


pickle.dump(total_tech.str.lower(), open("Survey Data/languages.pkl",'wb'))
language_size = total_tech.reset_index().groupby('index')[0].size().rename("num_lang")
survey_combined = pd.concat([survey_combined, language_size], axis=1)
survey_combined.rename(columns={0:"num languages"})


for df in [survey2011, survey2012, survey2013, survey2014, survey2015, survey2016]:
    print("Australasia" in df.country.unique(), "Australia" in df.country.unique())

world_bank = pd.read_csv("Data_Extract_From_World_Development_Indicators/GDP Data.csv")

set(survey2016.country) - set(world_bank['Country Name'])
set(world_bank['Country Name']) - set(survey2016.country)

so_to_wb = {'Antigua & Deps': 'Antigua and Barbuda',
 'Bahamas': 'Bahamas, The',
 'Bosnia Herzegovina': 'Bosnia and Herzegovina',
 'Burkina': 'Burkina Faso',
 'Central African Rep': 'Central African Republic',
 'Egypt': 'Egypt, Arab Rep.',
 'Hong Kong': 'Hong Kong SAR, China',
 'Iran': 'Iran, Islamic Rep.',
 'Ireland {Republic}': 'Ireland',
 'Ivory Coast': "Cote d'Ivoire",
 'Korea North': 'Korea, Dem. People’s Rep.',
 'Korea South': 'Korea, Rep.',
 'Kyrgyzstan': 'Kyrgyz Republic',
 'Laos': 'Lao PDR',
 'Macedonia': 'Macedonia, FYR',
 'Micronesia': 'Micronesia, Fed. Sts.',
 'Myanmar, {Burma}':'Myanmar',
 'Palestine': 'West Bank and Gaza',
 'Sao Tome & Principe': 'Sao Tome and Principe',
 'Slovakia': 'Slovak Republic',
 'St Kitts & Nevis': 'St. Kitts and Nevis',
 'Syria': 'Syrian Arab Republic',
 'Trinidad & Tobago': 'Trinidad and Tobago',
 'Venezuela': 'Venezuela, RB',
 'Yemen': 'Yemen, Rep.'}

wb_to_so = {i[1]:i[0] for i in so_to_wb.items()}

world_bank['country'] = world_bank['Country Name']
world_bank.replace({'country': wb_to_so}, inplace=True)
set(survey2016.country) - set(world_bank.country)

merge_data = world_bank.loc[world_bank['Series Name'] == 'GDP per capita (current US$)', ['country', '2015 [YR2015]']]
merge_data.rename(columns = {"2015 [YR2015]": "GDP per capita 2015"}, inplace=True)
survey2016 = pd.merge(survey2016,merge_data, on='country')

survey2016['GDP per capita 2015'] = pd.to_numeric(survey2016['GDP per capita 2015'], errors='coerce')

pd.set_option('display.float_format', '{:,.0f}'.format)
country_salary = survey2016.groupby('country').apply(lambda x: pd.Series([
        x.salary_midpoint.mean(),
        x['GDP per capita 2015'] .mean(),
        x.salary_midpoint.mean() - x['GDP per capita 2015'] .mean(),
        len(x.salary_midpoint)])).rename(columns={0:'avg. developer salary',
                                                  1:'gdp per cap',
                                                  2:'salary diff',
                                                  3:'sample size'})

country_salary.to_csv("output/salary_gdp2016.csv")


merge_wb = world_bank[['1990 [YR1990]', '2000 [YR2000]', '2007 [YR2007]',
       '2008 [YR2008]', '2009 [YR2009]', '2010 [YR2010]', '2011 [YR2011]', '2012 [YR2012]', '2013 [YR2013]',
       '2014 [YR2014]', '2015 [YR2015]', '2016 [YR2016]', 'country']]

merge_wb = pd.melt(merge_wb, id_vars='country')
merge_wb['variable'] = merge_wb['variable'].str[:4].astype(int)
merge_wb.rename(columns={'variable':'year', 'value': 'country_gdp'}, inplace=True)

survey_combined = pd.merge(survey_combined, merge_wb, how='left', on=['country','year'])

survey_combined.to_csv("Survey Data/survey_combined.csv")


dependent = "salary_midpoint"

explanatory = ["age", "industry", "num_lang"]

regdata = survey_combined[explanatory + [dependent]]


from sklearn import linear_model
lm = linear_model.LinearRegression()
ix = total_tech[total_tech == 'C++'].index.get_level_values(0)
regdata['lang'] = 0
regdata.ix[ix, 'lang'] = 1
regdata.dropna(inplace=True)
X = pd.get_dummies(regdata[explanatory + ['lang']])
X.head()
y = regdata[dependent]
lm.fit(X,y)
