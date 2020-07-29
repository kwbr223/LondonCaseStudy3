 
import  pandas as pd 
import numpy as np

 
import matplotlib.pyplot as plt




url_LondonHousePrices = "https://data.london.gov.uk/download/uk-house-price-index/70ac0766-8902-4eb5-aab5-01951aaed773/UK%20House%20price%20index.xls"


properties = pd.read_excel(url_LondonHousePrices, sheet_name='Average price', index_col= None)




properties.head()




properties_T = properties.T




properties_T.index





properties_T = properties_T.reset_index() 




properties_T.columns 




properties_T.iloc[[0]]




properties_T.columns = properties_T.iloc[0]





properties_T = properties_T.drop(properties_T.index[0])





properties_T = properties_T.rename(columns={'Unnamed: 0':'London_Borough', pd.NaT: 'ID'})





properties_T = properties_T.rename(columns={'Unnamed: 0':'London_Borough', pd.NaT: 'ID'})





properties_T.columns





clean_properties = pd.melt(properties_T, id_vars= ['London_Borough', 'ID'])





clean_properties = clean_properties.rename(columns = {0: 'Month', 'value': 'Average_price'})




clean_properties['Average_Price'] = pd.to_numeric(clean_properties['Average_price'])




clean_properties[clean_properties['ID'].isna()]



NaNFreeDF1 = clean_properties[clean_properties['Average_price'].notna()]
NaNFreeDF1.head(48)




NaNFreeDF2 = clean_properties.dropna()
NaNFreeDF2.head(48)





nonBoroughs = ['Inner London', 'Outer London', 
               'NORTH EAST', 'NORTH WEST', 'YORKS & THE HUMBER', 
               'EAST MIDLANDS', 'WEST MIDLANDS',
              'EAST OF ENGLAND', 'LONDON', 'SOUTH EAST', 
              'SOUTH WEST', 'England']





NaNFreeDF2[NaNFreeDF2.London_Borough.isin(nonBoroughs)]




NaNFreeDF2[~NaNFreeDF2.London_Borough.isin(nonBoroughs)]




NaNFreeDF2 = NaNFreeDF2[~NaNFreeDF2.London_Borough.isin(nonBoroughs)]




df = NaNFreeDF2





camden_prices = df[df['London_Borough'] == 'Camden']
ax = camden_prices.plot(kind ='line', x = 'Month', y='Average_Price')
ax.set_ylabel('Price')




df['Year'] = df['Month'].apply(lambda t: t.year)
df.tail()





dfg = df.groupby(by=['London_Borough', 'Year']).mean()
dfg.sample(10)





dfg = dfg.reset_index()
dfg.head()





def create_price_ratio(d):
    y1998 = float(d['Average_Price'][d['Year']==1998])
    y2018 = float(d['Average_Price'][d['Year']==2018])
    ratio = [y1998/y2018]
    return ratio



create_price_ratio(dfg[dfg['London_Borough']=='Barking & Dagenham'])





final = {}





for b in dfg['London_Borough'].unique():
    borough = dfg[dfg['London_Borough'] == b]
    final[b] = create_price_ratio(borough)
print(final) 





df_ratios = pd.DataFrame(final)





df_ratios_T = df_ratios.T
df_ratios = df_ratios_T.reset_index()
df_ratios.head()





df_ratios.rename(columns={'index':'Borough', 0:'2018'}, inplace=True)
df_ratios.head()





top15 = df_ratios.sort_values(by='2018',ascending=False).head(15)
print(top15)





ax = top15[['Borough','2018']].plot(kind='bar')

ax.set_xticklabels(top15.Borough)






