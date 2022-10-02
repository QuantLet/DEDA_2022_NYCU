#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import pprint
import pandas as pd
import numpy
import matplotlib.pyplot as plt
import requests

response = requests.get("	https://datacenter.taichung.gov.tw/swagger/OpenData/9af00e84-473a-4f3d-99be-b875d8e86256")
content = response.content
json_tree = json.loads(content)
pprint.pprint(json_tree)


# In[2]:


for bike_rent_records in json_tree['retVal']:
    leftRatio = float(bike_rent_records["sbi"]) / float(bike_rent_records["tot"]) * 100
    print("ID:{0}  Left:{2:0.1f}%  Name:{1}".format(bike_rent_records["sno"], bike_rent_records["aren"], leftRatio))


# In[3]:


dataframe = pd.DataFrame(json_tree['retVal'])
dataframe['lat']=dataframe['lat'].astype(float)
dataframe['lng']=dataframe['lng'].astype(float)
dataframe['sbi']=dataframe['sbi'].astype(float)
w = dataframe['lat']
v = dataframe['lng']
k = dataframe['sbi']
dataframe


# In[4]:


plt.scatter(w, v, k)
plt.title('Scatter plot of Taichung U-bike')
plt.xlabel('lat')
plt.ylabel('long')
plt.show()
plt.savefig('DEDA_410707007_HW2_Scraping with Taichung YouBike dataset')


# In[5]:


import folium
from folium.plugins import MarkerCluster
import numpy as np
import matplotlib.pyplot as plt

u_bike = folium.Map(location= [24.136807, 120.684875], zoom_start=13 )


for i in range(0,1202):
    pop_text=str(dataframe['sarea'][i]) + '</br>'             '場站名稱: ' +str(dataframe['sna'][i]) + '</br>'             '地址: ' +str(dataframe['ar'][i]) + '</br>'             '總停車格: ' +str(dataframe['tot'][i]) + '</br>'             '目前車輛數量: ' +str(dataframe['sbi'][i]) + '</br>'             '可還車位數: ' +str(dataframe['bemp'][i]) 

    folium.Marker([dataframe['lat'][i], dataframe['lng'][i]], icon = folium.Icon(icon='heart', color = 'beige'), popup = folium.Popup(pop_text, max_width=1000)).add_to(u_bike)
u_bike.save("DEDA_410707007_HW2_Scraping with Taichung YouBike dataset.html")
u_bike


# In[ ]:




