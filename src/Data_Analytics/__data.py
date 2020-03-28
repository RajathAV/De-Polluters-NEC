#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib as plt
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
from matplotlib.offsetbox import AnchoredText


meta_data = pd.read_csv("DataSet/IndiaAffectedWaterQualityAreas.csv",encoding='latin1')

# In[29]:


states = meta_data['State Name'].unique()

meta_data['Quality Parameter'].value_counts()


# In[7]:


meta_data['Quality Parameter'].groupby(meta_data['State Name']).describe()


# In[8]:


import dateutil
meta_data['date'] = meta_data['Year'].apply(dateutil.parser.parse, dayfirst=True)
import datetime as dt
meta_data['date'] = pd.to_datetime(meta_data['date'])
meta_data['year'] = meta_data['date'].dt.year
meta_data['month'] = meta_data['date'].dt.month


# In[9]:


State_Data = meta_data[['State Name', 'Quality Parameter', 'year','month']]
del State_Data ['year']
del State_Data ['month']


# In[10]:


import sklearn
from sklearn.preprocessing import LabelEncoder
numbers = LabelEncoder()


# In[11]:


State_Data['Quality'] = numbers.fit_transform(State_Data['Quality Parameter'].astype('str'))


# In[13]:


Group1 = State_Data.groupby(['State Name','Quality Parameter','Quality']).count()
Group1


# In[14]:


State_Quality_Count = pd.DataFrame({'count' : State_Data.groupby( [ "State Name", "Quality","Quality Parameter"] ).size()}).reset_index()



# In[39]:


state_data = {}
for k in states:
    state_data[k]="No Data Avaliable"

def state_wise_data(state):
    state = state.upper()
    if state in state_data:
        state_data[state] = State_Quality_Count[State_Quality_Count["State Name"] == state]
    


# In[110]:


for s in states:
    state_wise_data(s)

    

l = state_data['KARNATAKA'].values.tolist()

# In[113]:

import json

out_file = open('data_out.txt','w+')

state_dict = {}
def list_gen(state):
    temp_chem =[]
    temp_count =[]
    temp = state_data[state].values.tolist()
    for k in temp:
        temp_chem.append(k[2])
        temp_count.append(k[3])
    state_dict[state]=[temp_chem,temp_count]

for k in states:
    list_gen(k)

json.dump(state_dict,out_file)
# In[81]:


def plot_data(state):
    #plt.figure(figsize=(6,4))
    ax = sns.barplot(x="count", y ="Quality Parameter", data = state_data.get(state))
    #ax.set(xlabel='Count')
    sns.despine(left=True, bottom=True)
    plot_name = "Water Quality Parameter In "+ state
    plt.title(plot_name)
    filename = "plots/"+state+".png"
    plt.savefig(filename, dpi=400)
    plt.close()
    
for k in states:
    plot_data(k)


# In[82]:


'''plt.figure(figsize=(6,4))
ax = sns.barplot(x="count", y ="Quality Parameter", data = TAMIL_NADU)
ax.set(xlabel='Count')
sns.despine(left=True, bottom=True)
plt.title("Water Quality Parameter In Tamil Nadu")'''


# In[18]:


'''plt.figure(figsize=(6,4))
ax = sns.barplot(x="count", y ="Quality Parameter", data = KARNATAKA)
ax.set(xlabel='Count')
sns.despine(left=True, bottom=True)
plt.title("Water Quality Parameter In KARNATAKA")
fig = ax.get_figure()
fig.savefig("Karnataka.png")'''


# In[19]:


x = State_Quality_Count.groupby('State Name')
plt.rcParams['figure.figsize'] = (9.5, 6.0)
genre_count = sns.barplot(y='Quality Parameter', x='count', data=State_Quality_Count, palette="Blues", ci=None)
#plt.show()

plt.close()




# In[ ]:




