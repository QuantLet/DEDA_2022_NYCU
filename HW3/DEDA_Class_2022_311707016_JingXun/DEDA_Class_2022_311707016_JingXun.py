from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import pandas as pd
import matplotlib.pyplot as plt
import pysent3 as ps
import requests
import re

# get the website data from the url
url = 'https://www.federalreserve.gov/newsevents/speech/powell20220826a.htm'
res = requests.get(url).text

# parsing the html and find the part to be analyzed
parsed_html = BeautifulSoup(res, 'lxml')
text = parsed_html.find_all('div', class_='col-xs-12 col-sm-8 col-md-8')

# data cleaning
text_list = []
for i in text:
    text_list.append(i.get_text())

cleantext_prep = str(text_list[0])

expression = '[^a-zA-Z0-9 ]' # keep only letters, numbers and whitespace
cleantextCAP = re.sub(expression, '', cleantext_prep) # replace empty string
cleantext = cleantextCAP.lower()

# split the text into list
splited = list(cleantext.split())

# add the words into a dictionary and get the frequency (key: word, value: freq)
dict1 = {}
for i in range(len(splited)):
    word = splited[i]
    dict1[word] = splited.count(word)

# discard the words that in stopwords
keys = list(dict1)
filtered_words = [word for word in keys if word not in stopwords.words('english')]
dict2 = dict((k, dict1[k]) for k in filtered_words)

# use the defining function to get the most frequent words according to the length (number of words)
def sequenceSelection(dictionary, length, startindex = 0):

    # check input
    if length > len(dictionary):
        print('Input length is too long.')
        return 1
    else:
        # keys in dict become value, frequency in dict become key
        # to perform the sort() function by the first item in tuple
        items = [(v, k) for k, v in dictionary.items()] 
        items.sort()
        items.reverse()
        items_out = [(k, v) for v, k in items]

        # get the highest words
        highest = items_out[startindex : startindex + length]
        dd = dict(highest)
        selected_keys = dd.keys()
        dict_show = dict((k, dictionary[k]) for k in selected_keys if k in dictionary)
        
        return dict_show

freq_words = sequenceSelection(dictionary=dict2, length=10)

# visualization and save the figure
plt.figure(figsize=(8, 5), dpi=100)
plt.xticks(rotation=45, fontsize=10)
plt.ylabel('frequency', fontsize=13)
plt.title('The Most Frequent Words in Fed Speech on Aug 26, 2022', fontsize=14)
fig = plt.bar(freq_words.keys(), freq_words.values(), color='orange')

for bar in fig:
    height = bar.get_height()
    plt.text(bar.get_x()+0.25, height, str(height), ha='left')

plt.savefig('speech_frequency.jpg', dpi=200, bbox_inches='tight')

plt.show()


# sentiment analysis
hiv4 = ps.HIV4() # Use Harvard IV
tokens = hiv4.tokenize(cleantext) # split string into constituents
score = hiv4.get_score(tokens) 
print(score)
sentiment_output = open('sentiment_output.txt', 'w')
sentiment_output.write(str(score))
sentiment_output.close()