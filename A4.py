
# coding: utf-8

# In[1]:


import pandas as pd
import math
import numpy as np


# In[2]:


"""
Stanford Geospatial Center
Mass Shooting in America Dataset
Cleans up the following columns:
* Fate of Shooter
* Shooter Race
* Average Shooter Age
* Place Type
* Shooter's Cause of Death
* Relationship to Incident Location
"""


# In[3]:


origdata = pd.read_csv("https://raw.githubusercontent.com/StanfordGeospatialCenter/MSA/master/Data/Stanford_MSA_Database.csv")


# In[4]:


# Clean up 'Fate of Shooter' column
for index, row in origdata.iterrows():
    if row['Fate of Shooter']== 'FALSE':
        origdata.loc[index, 'Fate of Shooter'] = ""
    if row['Fate of Shooter'] == "Custody/Escaped":
        origdata.loc[index, 'Fate of Shooter'] = "Custody"
    # merge 3 records into custody
    if row['Fate of Shooter'] == "Custody / Escaped":
        origdata.loc[index, 'Fate of Shooter'] = "Custody"
    if type(row['Fate of Shooter']) == float:
        origdata.loc[index, 'Fate of Shooter'] = ""


# In[5]:


# Clean up 'Shooter Race' column
for index, row in origdata.iterrows():
    if row['Shooter Race']== "White American or European American/Some other Race":
        origdata.loc[index, 'Shooter Race'] = "White American or European American"
        
    if row['Shooter Race']== "Black American or African American/Unknown":
        origdata.loc[index, 'Shooter Race'] = "Black American or African American"
    
    if row['Shooter Race']== "Asian American/Some other race":
        origdata.loc[index, 'Shooter Race'] = "Asian American"
    
    if row['Shooter Race']== "Some other race":
        origdata.loc[index, 'Shooter Race'] = "Some Other Race"


# In[6]:


# Clean up 'Average Shooter Age' colummn
for index, row in origdata.iterrows():
    if row['Average Shooter Age'] == "32\n+ Unknown":
        origdata.loc[index, 'Average Shooter Age'] = '32'
    elif row['Average Shooter Age'] == 'Unknown':
        origdata.loc[index, 'Average Shooter Age'] = float('nan')
    else:
        origdata.loc[index, 'Average Shooter Age'] = float(row['Average Shooter Age'])


# In[7]:


# Checks that these columns are numbers
number_columns = ['Number of Civilian Fatalities','Number of Civilian Injured',
                  'Number of Enforcement Fatalities','Number of Enforcement Injured','Total Number of Victims']
for col in number_columns:
    for index, row in origdata.iterrows():
        try:
            float(row[col])
        except ValueError:
            print(index)


# In[8]:


# Clean up 'Place Type' Column
col = 'Place Type'
for index, row in origdata.iterrows():
    if row[col] in ['Secondary School','Secondary school' ]:
        origdata.loc[index, col] = 'Secondary school'
    if row[col] in ['Restaurant/Cafe', 'Restaurant/Cafe?', 'Restaurant/Cafeé','Restaurant/cafe' ]:
        origdata.loc[index, col] = 'Restaurant/Cafe'
    if row[col] in ['Residential Home/Neighborhood','Residential home', 'Residential home/Neighborhood', 
                    'Residential home/Neighborhood,\nRetail/ Wholesale/Services facility',
                    'Residential home/Neighborhood \nand Street/Highway' ]:
        origdata.loc[index, col] = 'Residential Home/Neighborhood'
    if row[col] in ['Entertainment Venue','Entertainment venue' ]:
        origdata.loc[index, col] = 'Entertainment venue'
    if row[col] in ['Park/Wilderness','Park/Wildness' ]:
        origdata.loc[index, col] = 'Park/Wilderness'
    if row[col] in ['Public Transportation','Public transportation' ]:
        origdata.loc[index, col] = 'Public transportation'
    if row[col] in ['Retail/ Wholesale/Services facility','Retail/ Wholesale/Services facility\nand Primary school',
                   'Retail/Wholesale/Services facility', 'Retail/Wholesale/Services facility\n/Residential home/Neighborhood']:
        origdata.loc[index, col] = 'Retail/Wholesale/Services facility'


# In[9]:


# clean up 'School Related' column
col = 'School Related'
for index, row in origdata.iterrows():
    if row['Place Type'] in ['College/University/Adult education','Primary school', 'Secondary school' ]:
        origdata.loc[index, col] = 'Yes'
    if origdata.loc[index, col] == 'no':
        origdata.loc[index, col] = 'No'
    if origdata.loc[index, col] == 'Killed':
        origdata.loc[index, col] = 'No'


# In[10]:


# clean up "Shooter's Cause of Death"
col = 'Shooter\'s Cause of Death'
for index, row in origdata.iterrows():
    if row[col] in ['Not Apllicable','Not Applicable', 'Not applicable' ]:
        origdata.loc[index, col] = 'Not applicable'


# In[11]:


# clean up 'Relationship to Incident Location'
col = 'Relationship to Incident Location'
for index, row in origdata.iterrows():
    if type(row[col]) == float:
        origdata.loc[index, col] = 'Unknown'
    if row[col] in ['None','Unknown']:
        origdata.loc[index, col] = 'Unknown'
    if row[col] in ['Place of Residency', 'Residential home/Neighborhood']:
        origdata.loc[index, col] = 'Place of residency'
    if row[col] in ['Place of business/employment\nPlace of residency', 
                    'Place of Business/employment', 'Place of business/employment']:
        origdata.loc[index, col] = 'Place of business/employment'


# In[12]:


# print out unique values and frequency
col = 'Relationship to Incident Location'
uniqueValues, occurCount = np.unique(origdata[col], return_counts=True)
 
# Zip both the arrays
listOfUniqueValues = zip(uniqueValues, occurCount)
# Iterate over the zip object
for elem in listOfUniqueValues:
    print(elem[0] , ' Occurs : ' , elem[1], ' times')


# In[13]:


origdata.to_csv("msa.csv")

