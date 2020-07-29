 
import  pandas as pd 
import numpy as np

 
import matplotlib.pyplot as plt


# #### 1.2.  Loading the data
# Your data comes from the [London Datastore](https://data.london.gov.uk/): a free, open-source data-sharing portal for London-oriented datasets. 

# In[8]:


# First, make a variable called url_LondonHousePrices, and assign it the following link, enclosed in quotation-marks as a string:
# https://data.london.gov.uk/download/uk-house-price-index/70ac0766-8902-4eb5-aab5-01951aaed773/UK%20House%20price%20index.xls

url_LondonHousePrices = "https://data.london.gov.uk/download/uk-house-price-index/70ac0766-8902-4eb5-aab5-01951aaed773/UK%20House%20price%20index.xls"

# The dataset we're interested in contains the Average prices of the houses, and is actually on a particular sheet of the Excel file. 
# As a result, we need to specify the sheet name in the read_excel() method.
# Put this data into a variable called properties.  
properties = pd.read_excel(url_LondonHousePrices, sheet_name='Average price', index_col= None)


# ### 2. Cleaning, transforming, and visualizing
# This second stage is arguably the most important part of any Data Science project. The first thing to do is take a proper look at the data. Cleaning forms the majority of this stage, and can be done both before or after Transformation.
# 
# The end goal of data cleaning is to have tidy data. When data is tidy: 
# 
# 1. Each variable has a column.
# 2. Each observation forms a row.
# 
# Keep the end goal in mind as you move through this process, every step will take you closer. 
# 
# 
# 
# ***Hint:*** This part of the data science pipeline should test those skills you acquired in: 
# - Intermediate Python for data science, all modules.
# - pandas Foundations, all modules. 
# - Manipulating DataFrames with pandas, all modules.
# - Data Types for Data Science, Module Four.
# - Python Data Science Toolbox - Part One, all modules

# **2.1. Exploring your data** 
# 
# Think about your pandas functions for checking out a dataframe. 

# In[9]:


properties.head()


# **2.2. Cleaning the data**
# 
# You might find you need to transpose your dataframe, check out what its row indexes are, and reset the index. You  also might find you need to assign the values of the first row to your column headings  . (Hint: recall the .columns feature of DataFrames, as well as the iloc[] method).
# 
# Don't be afraid to use StackOverflow for help  with this.

# In[10]:


properties_T = properties.T


# In[11]:


properties_T.index


# In[12]:


properties_T = properties_T.reset_index() 


# In[13]:


properties_T.columns 


# In[14]:


properties_T.iloc[[0]]


# In[15]:


properties_T.columns = properties_T.iloc[0]


# In[16]:


properties_T = properties_T.drop(properties_T.index[0])


# **2.3. Cleaning the data (part 2)**
# 
# You might we have to **rename** a couple columns. How do you do this? The clue's pretty bold...

# In[17]:


properties_T = properties_T.rename(columns={'Unnamed: 0':'London_Borough', pd.NaT: 'ID'})


# In[18]:


properties_T = properties_T.rename(columns={'Unnamed: 0':'London_Borough', pd.NaT: 'ID'})


# In[19]:


properties_T.columns


# **2.4.Transforming the data**
# 
# Remember what Wes McKinney said about tidy data? 
# 
# You might need to **melt** your DataFrame here. 

# In[20]:


clean_properties = pd.melt(properties_T, id_vars= ['London_Borough', 'ID'])


# In[21]:


clean_properties = clean_properties.rename(columns = {0: 'Month', 'value': 'Average_price'})


# In[22]:


clean_properties['Average_Price'] = pd.to_numeric(clean_properties['Average_price'])


# **2.5. Cleaning the data (part 3)**
# 
# Do we have an equal number of observations in the ID, Average Price, Month, and London Borough columns? Remember that there are only 32 London Boroughs. How many entries do you have in that column? 
# 
# Check out the contents of the London Borough column, and if you find null values, get rid of them however you see fit. 

# In[23]:


clean_properties[clean_properties['ID'].isna()]


# In[24]:


NaNFreeDF1 = clean_properties[clean_properties['Average_price'].notna()]
NaNFreeDF1.head(48)


# In[25]:


NaNFreeDF2 = clean_properties.dropna()
NaNFreeDF2.head(48)


# Remember to make sure your column data types are all correct. Average prices, for example, should be floating point numbers... 

# In[26]:


nonBoroughs = ['Inner London', 'Outer London', 
               'NORTH EAST', 'NORTH WEST', 'YORKS & THE HUMBER', 
               'EAST MIDLANDS', 'WEST MIDLANDS',
              'EAST OF ENGLAND', 'LONDON', 'SOUTH EAST', 
              'SOUTH WEST', 'England']


# In[27]:


NaNFreeDF2[NaNFreeDF2.London_Borough.isin(nonBoroughs)]


# In[28]:


NaNFreeDF2[~NaNFreeDF2.London_Borough.isin(nonBoroughs)]


# In[29]:


NaNFreeDF2 = NaNFreeDF2[~NaNFreeDF2.London_Borough.isin(nonBoroughs)]


# In[30]:


df = NaNFreeDF2


# **2.6. Visualizing the data**
# 
# To visualize the data, why not subset on a particular London Borough? Maybe do a line plot of Month against Average Price?

# In[31]:


camden_prices = df[df['London_Borough'] == 'Camden']
ax = camden_prices.plot(kind ='line', x = 'Month', y='Average_Price')
ax.set_ylabel('Price')


# To limit the number of data points you have, you might want to extract the year from every month value your *Month* column. 
# 
# To this end, you *could* apply a ***lambda function***. Your logic could work as follows:
# 1. look through the `Month` column
# 2. extract the year from each individual value in that column 
# 3. store that corresponding year as separate column. 
# 
# Whether you go ahead with this is up to you. Just so long as you answer our initial brief: which boroughs of London have seen the greatest house price increase, on average, over the past two decades? 

# In[32]:


df['Year'] = df['Month'].apply(lambda t: t.year)
df.tail()


# In[33]:


dfg = df.groupby(by=['London_Borough', 'Year']).mean()
dfg.sample(10)


# In[34]:


dfg = dfg.reset_index()
dfg.head()


# **3. Modeling**
# 
# Consider creating a function that will calculate a ratio of house prices, comparing the price of a house in 2018 to the price in 1998.
# 
# Consider calling this function create_price_ratio.
# 
# You'd want this function to:
# 1. Take a filter of dfg, specifically where this filter constrains the London_Borough, as an argument. For example, one admissible argument should be: dfg[dfg['London_Borough']=='Camden'].
# 2. Get the Average Price for that Borough, for the years 1998 and 2018.
# 4. Calculate the ratio of the Average Price for 1998 divided by the Average Price for 2018.
# 5. Return that ratio.
# 
# Once you've written this function, you ultimately want to use it to iterate through all the unique London_Boroughs and work out the ratio capturing the difference of house prices between 1998 and 2018.
# 
# Bear in mind: you don't have to write a function like this if you don't want to. If you can solve the brief otherwise, then great! 
# 
# ***Hint***: This section should test the skills you acquired in:
# - Python Data Science Toolbox - Part One, all modules

# In[37]:


def create_price_ratio(d):
    y1998 = float(d['Average_Price'][d['Year']==1998])
    y2018 = float(d['Average_Price'][d['Year']==2018])
    ratio = [y1998/y2018]
    return ratio


# In[38]:


create_price_ratio(dfg[dfg['London_Borough']=='Barking & Dagenham'])


# In[39]:


final = {}


# In[42]:


for b in dfg['London_Borough'].unique():
    borough = dfg[dfg['London_Borough'] == b]
    final[b] = create_price_ratio(borough)
print(final) 


# In[43]:


df_ratios = pd.DataFrame(final)


# In[44]:


df_ratios_T = df_ratios.T
df_ratios = df_ratios_T.reset_index()
df_ratios.head()


# In[45]:


df_ratios.rename(columns={'index':'Borough', 0:'2018'}, inplace=True)
df_ratios.head()


# In[46]:


top15 = df_ratios.sort_values(by='2018',ascending=False).head(15)
print(top15)


# In[52]:


ax = top15[['Borough','2018']].plot(kind='bar')

ax.set_xticklabels(top15.Borough)


# ### 4. Conclusion
# What can you conclude? Type out your conclusion below. 
# 
# Look back at your notebook. Think about how you might summarize what you have done, and prepare a quick presentation on it to your mentor at your next meeting. 
# 
# We hope you enjoyed this practical project. It should have consolidated your data hygiene and pandas skills by looking at a real-world problem involving just the kind of dataset you might encounter as a budding data scientist. Congratulations, and looking forward to seeing you at the next step in the course! 

# In[ ]:



