# -*- coding: utf-8 -*-
"""

@author: saarah.rasheed
"""

import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
st.set_page_config(layout="wide")


st.title('Data Exploration App')
#file_path1=r'C:\Users\Hp\Documents\Emmad\Data Analyst_CDA\Python for DS\Final Assignment\athlete_events.csv'
#file_path2=r'C:\Users\Hp\Documents\Emmad\Data Analyst_CDA\Python for DS\Final Assignment\noc_regions.csv'
athelete_data=pd.read_csv('athlete_events.csv')
noc_data=pd.read_csv('noc_regions.csv')
#Data Cleaning
#filling na 
#updated_data.isna().sum()
updated_data=athelete_data.drop_duplicates()
Avg_Height=updated_data['Height'].mean()
Avg_Weight=updated_data['Weight'].mean()
Avg_Age=updated_data['Age'].mean()

updated_data['Height']=updated_data['Height'].fillna(Avg_Height)
updated_data['Weight']=updated_data['Weight'].fillna(Avg_Weight)
updated_data['Age']=updated_data['Age'].fillna(Avg_Age)
updated_data['Medal']=updated_data['Medal'].fillna('Not Known')

#Adjusting Data Type 
updated_data['Year']=pd.to_datetime(updated_data['Year'])

#merged data
#merfing data using left join on NOC column to better creating summary
merged_df = updated_data.merge(noc_data, on="NOC", how='left')

#adding coulumn to existing Dataframe
merged_df= pd.concat([merged_df,pd.get_dummies(merged_df['Medal'])], axis=1)
#Groupby year
each_medal_df=merged_df.groupby('Year')[['Gold','Silver','Bronze']].sum()
#medal count


# use year to filter data
country_select = st.selectbox('Select country', merged_df['region'].unique())
subset=merged_df[merged_df['region']==country_select]

all_medal=subset[subset['Medal']!='Not Known']

gold_m=subset[subset['Medal']=='Gold']
silver_m=subset[subset['Medal']=='Silver']
bronze_m=subset[subset['Medal']=='Bronze']  

gold_medal=gold_m['Medal'].count()
silver_medal=silver_m['Medal'].count()
bronze_medal=bronze_m['Medal'].count()

#sorted(data[].unique())

# the metric component takes the value you want to show and the change from a prev.
# value (it shows it as up/down arrow based on the change value)
curr_count = 100
inc_count = 10

curr_medals = 50
inc_medals = -4

country_count = 14
inc_count = 5


# combining metrics and columns to create 
#st.header('Olympics - {}'.format(year))
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric('Number of Olympians', subset['ID'].nunique(), inc_count)
col2.metric('Participating Countries', country_count, inc_count)
col3.metric('Gold Medals', gold_medal, inc_medals)
col4.metric('Silver Medals', silver_medal, inc_medals)
col5.metric('Bronze Medals', bronze_medal, inc_medals)


with st.container():
    left, right = st.columns(2)
    # for dataframe styling, e.g. highlighting max values in a df, refer to the following 
    #link: https://docs.streamlit.io/library/api-reference/data/st.dataframe
    df = pd.DataFrame(np.random.randn(10, 10), columns=('col %d' % i for i in range(10)))
    left.header('Tabular View')
    left.dataframe(df.style.highlight_max(axis=0))
    
    
    
    #creating visuals
    chart_data = plt.plot(each_medal_df.Year, each_medal_df.Gold, 'b-o'),
    #columns=['a', 'b', 'c'])
    right.header('Line Chart Visual')
    right.line_chart(chart_data)
    
    #left.header('Bar Chart Visual')
    #left.bar_chart(chart_data)
    
    arr = np.random.normal(1, 1, size=100)
    fig, ax = plt.subplots()
    ax.hist(arr, bins=20)
    
    right.header('Histogram Visual')
    right.pyplot(fig)
    
    #left.header('Area Chart Visual')
    #left.area_chart(chart_data)




