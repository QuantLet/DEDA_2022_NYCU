# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 15:26:03 2022

@author: Tracy Zhou
"""

# install package 
# pip install pysentiment2
# pip install yfinance

# Loading package
# Load moduls 
import requests
from bs4 import BeautifulSoup as soup
from datetime import datetime, date # needed to retrieve the date of publication 
import re
import os
import pysentiment2 as ps
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from urllib import parse
import warnings
warnings.filterwarnings('ignore')

# check directory
os.getcwd()
#direct = os.getcwd()

# WEB SCRAPE TWO SOURCES: 1. NEWSROOM 2.ANNOUCEMENTS
# 1. NEWSRROM
url1 = 'https://www.pfizer.com/newsroom/press-releases?items_per_page=12'
page = '&page='
url = list()
url.append(url1)
for i in range(1, 55):
    url2 = url1 + page + str(i)
    url.append(url2)
#print(url)

page_info = list() # create empty list 
for i in range(0,55):
    scmp_url = url[i]
    print(scmp_url)
    url_request = requests.get(scmp_url)
    url_content = url_request.content # … in bytes
    url_text = url_request.text # … in unicode
    parsed_content = soup(url_content)
    parsed_text = soup(url_text, 'html.parser') # ‘html.parser’ also possible, 'lxml'
    filtered_parts = parsed_text.find_all('li', class_ = "grid-x") 
    for section in filtered_parts: 
        unit_info = dict() # create empty dictionary where we gradually attach items to
        
        filtered_part1 = section.find_all('helix-core-content', slot = 'date') # for date 'sc-iqHYGH hkvqJt'
        #print(filtered_part1[0])
        news_date = datetime.strptime(filtered_part1[0].text.strip(),'%m.%d.%Y') # '%m.%d.%Y'
        news_date = news_date.date() # cuts off the time
        print(news_date)
        unit_info['news_date'] = news_date # add news_date to the dictionary
        
        filtered_part1 = section.find_all('a', href=re.compile("^/news/press-release/press-release-detail"))
        #print(filtered_part1[0])
        if filtered_part1 == []: # Error handling 
            continue
        news_title = filtered_part1[0].text.strip() # find title item 
        print(news_title)
        news_link = filtered_part1[0].get('href').strip() # find title item
        news_link = f"https://www.pfizer.com/{news_link}" # adjust link
        print(news_link)
        unit_info['news_title'] = news_title # add news_title to the dictionary
        unit_info['news_link'] = news_link # add news_link to the dictionary
        
        filtered_part3 = section.find_all('corporate-tag') # for tag , class_ = "tag tag--primary field_tags hydrated"
        #print(len(filtered_part3))
        if filtered_part3 == []: # Error handling 
            continue
        news_tag = filtered_part3[0].text.strip()
        print(news_tag)
        unit_info['news_tag'] = news_tag
        
        page_info.append(unit_info) # attach dictionary to list

df = pd.DataFrame(page_info, columns=['news_date', 'news_title', 'news_link', 'news_tag'])
#print(df)

direct = os.getcwd()
df.to_csv(direct + '/Pfizer_Press.csv')


df.insert(1,'Positive',0)
df.insert(2,'Negative',0)
df.insert(3,'Polarity',0.00)
df.insert(4,'Subjectivity',0.00)
df.insert(5,'news_time', None)

lenth = len(df)
#print(lenth)
for i in range(0, lenth):
    url = df.at[i,'news_link']
    print(url)
    url_request = requests.get(url)
    url_content = url_request.content # … in bytes
    url_text = url_request.text # … in unicode
    parsed_content = soup(url_content)
    parsed_text = soup(url_text, 'html.parser') # ‘html.parser’ also possible 'lxml'
    
    filtered_parts = parsed_text.find_all('div', class_ = "article-content") 
    if filtered_parts == []: # Error handling 
        print('NO VALUE')
        df.at[i,'Positive'] = None
        df.at[i,'Negative'] = None
        df.at[i,'Polarity'] = None
        df.at[i,'Subjectivity'] = None
        continue 
    else: 
        news_text = filtered_parts[0].text.strip() # find title item
        #print(news_text)
        # Sentiment Analysis
        hiv4 = ps.HIV4()
        tokens = hiv4.tokenize(news_text)
        score = hiv4.get_score(tokens)
        print(score)
        df.at[i,'Positive'] = score.get('Positive')
        df.at[i,'Negative'] = score.get('Negative')
        df.at[i,'Polarity'] = score.get('Polarity')
        df.at[i,'Subjectivity'] = score.get('Subjectivity')
    
    filtered_parts2 = parsed_text.find_all('div', class_ = "article-date copy-clipboard") 
    if filtered_parts2 == []: # Error handling 
        print('NA')
        continue 
    #print(filtered_parts2[0])
    news_time = filtered_parts2[0].text.strip() # find title item
    df.at[i,'news_time'] = news_time

print(df)

direct = os.getcwd()
df.to_csv(direct + '/Pfizer_Press_sentiment.csv')


# 2.ANNOUCEMENTS
url1 = 'https://www.pfizer.com/stories/announcements?items_per_page=12'
page = '&page='
url = list()
url.append(url1)
for i in range(1, 13):
    url2 = url1 + page + str(i)
    url.append(url2)
#print(url)

page_info = list() # create empty list 
for i in range(0,13):
    scmp_url = url[i]
    print(scmp_url)
    url_request = requests.get(scmp_url)
    url_content = url_request.content # … in bytes
    url_text = url_request.text # … in unicode
    parsed_content = soup(url_content)
    parsed_text = soup(url_text, 'html.parser') # ‘html.parser’ also possible, 'lxml'
    filtered_parts = parsed_text.find_all('li', class_ = "grid-x") 
    for section in filtered_parts: 
        unit_info = dict() # create empty dictionary where we gradually attach items to
        
        filtered_part1 = section.find_all('helix-core-content', slot = 'date') # for date 'sc-iqHYGH hkvqJt'
        #print(filtered_part1[0])
        news_date = datetime.strptime(filtered_part1[0].text.strip(),'%m.%d.%Y') # '%m.%d.%Y'
        news_date = news_date.date() # cuts off the time
        print(news_date)
        unit_info['news_date'] = news_date # add news_date to the dictionary
        
        filtered_part1 = section.find_all('a', href=re.compile("^/news/announcements"))
        if filtered_part1 == []: # Error handling 
            continue
        news_title = filtered_part1[0].text.strip() # find title item 
        print(news_title)
        news_link = filtered_part1[0].get('href').strip() # find title item
        news_link = f"https://www.pfizer.com/{news_link}" # adjust link
        print(news_link)
        unit_info['news_title'] = news_title # add news_title to the dictionary
        unit_info['news_link'] = news_link # add news_link to the dictionary
        
        filtered_part3 = section.find_all('corporate-tag') # for tag , class_ = "tag tag--primary field_tags hydrated"
        if filtered_part3 == []: # Error handling 
            continue
        news_tag = filtered_part3[0].text.strip()
        print(news_tag)
        unit_info['news_tag'] = news_tag
        
        page_info.append(unit_info) # attach dictionary to list

df = pd.DataFrame(page_info, columns=['news_date', 'news_title', 'news_link', 'news_tag'])
print(df)

direct = os.getcwd()
df.to_csv(direct + '/Pfizer_Story.csv')


df.insert(1,'Positive',0)
df.insert(2,'Negative',0)
df.insert(3,'Polarity',0.00)
df.insert(4,'Subjectivity',0.00)
df.insert(5,'news_time', None)

lenth = len(df)
#print(lenth)
for i in range(0, lenth):
    url = df.at[i,'news_link']
    print(url)
    url_request = requests.get(url)
    url_content = url_request.content # … in bytes
    url_text = url_request.text # … in unicode
    parsed_content = soup(url_content)
    parsed_text = soup(url_text, 'html.parser') # ‘html.parser’ also possible 'lxml'
    
    filtered_parts = parsed_text.find_all('div', class_ = "layout__region layout__region--content") 
    if filtered_parts == []: # Error handling 
        print('NO VALUE')
        df.at[i,'Positive'] = None
        df.at[i,'Negative'] = None
        df.at[i,'Polarity'] = None
        df.at[i,'Subjectivity'] = None
        continue 
    else: 
        news_text = filtered_parts[0].text.strip() # find title item
        #print(news_text)
        # Sentiment Analysis
        hiv4 = ps.HIV4()
        tokens = hiv4.tokenize(news_text)
        score = hiv4.get_score(tokens)
        print(score)
        df.at[i,'Positive'] = score.get('Positive')
        df.at[i,'Negative'] = score.get('Negative')
        df.at[i,'Polarity'] = score.get('Polarity')
        df.at[i,'Subjectivity'] = score.get('Subjectivity')
    
    filtered_parts2 = parsed_text.find_all('div', class_ = "article-date section-spacing") 
    if filtered_parts2 == []: # Error handling 
        print('NA')
        continue 
    #print(filtered_parts2[0])
    news_time = filtered_parts2[0].text.strip() # find title item
    df.at[i,'news_time'] = news_time

print(df)

direct = os.getcwd()
df.to_csv(direct + '/Pfizer_Story_sentiment.csv')


import yfinance as yf
stock = yf.download("PFE", start="2018-01-01", end="2022-12-30")
stock = stock.reset_index()
print(stock)
direct = os.getcwd()
stock.to_csv(direct + '/Pfizer_StockPrice.csv')


# pip install pytrends
from pytrends.request import TrendReq
from pprint import pprint
df = pd.DataFrame(columns = ['date','Pfizer'])
for y in range(2018,2023):
    yn = str(y+1)
    y = str(y)
    pytrend = TrendReq(hl='en-US', tz=360)
    keywords = ['Pfizer', 'COVID-19', 'Vaccines','Tesla']
    timeframe = '{0}-01-01 {0}-06-30'.format(y)
    pytrend.build_payload(keywords, timeframe = timeframe)
    df = df.append(pytrend.interest_over_time()).drop(columns = 'isPartial')
    timeframe = '{0}-06-30 {1}-01-01'.format(y,yn)
    pytrend.build_payload(keywords, timeframe = timeframe)
    df = df.append(pytrend.interest_over_time()).drop(columns = 'isPartial')
    
print(df)
direct = os.getcwd()
df.to_csv(direct + '/Pfizer_trends.csv')


from pytrends.request import TrendReq
from pprint import pprint
df = pd.DataFrame(columns = ['date','Pfizer'])
for y in range(2018,2023):
    yn = str(y+1)
    y = str(y)
    pytrend = TrendReq(hl='en-US', tz=360)
    keywords = ['Pfizer', 'COVID-19', 'Vaccines','Tesla']
    timeframe = '{0}-01-01 {0}-12-31'.format(y)
    pytrend.build_payload(keywords, timeframe = timeframe)
    df = df.append(pytrend.interest_over_time()).drop(columns = 'isPartial')
    
print(df)
direct = os.getcwd()
df.to_csv(direct + '/Pfizer_trends_week.csv')

