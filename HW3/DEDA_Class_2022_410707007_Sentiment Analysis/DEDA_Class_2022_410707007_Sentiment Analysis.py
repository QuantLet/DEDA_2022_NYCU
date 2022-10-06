
#import nltk
#nltk.download()

from selenium import webdriver
import matplotlib.pyplot as plt
import re
from nltk.corpus import stopwords
import os
from selenium.webdriver.common.by import By
import pandas as pd
#import pysentiment as ps
#from wordcloud import WordCloud


#path_direct = os.getcwd()
#os.chdir(path_direct + '/pyning')
#p = r""
#os.chdir(p)


# Start Selenium
browser = webdriver.Chrome(r"D:\DEDA_Class_2022_410707007_Sentiment Analysis\chromedriver.exe")
url = "https://edition.cnn.com/2020/08/21/politics/joe-biden-democratic-presidential-nomination-speech/index.html"



# Extract text
browser.get(url)

#content = browser.find_element_by_class_name("t-single__content-Body-content")
content = browser.find_element(By.CLASS_NAME, "article__content-container") #
text = content.text
browser.close()
browser.stop_client()




# Some expressions still left
# Differ between quotes!
expression = "[()]|(\“)|(\”)|(\“)|(\”)|(\,|\.|-|\;|\<|\>)|(\\n)|(\\t)|(\=)|(\|)|(\-)|(\')|(\’)"
cleantextCAP = re.sub(expression, '', text)
cleantext = cleantextCAP.lower()       

# Count and create dictionary
dat = list(cleantext.split())
dict1 = {}
for i in range(len(dat)):
    print(i)
    word = dat[i]
    dict1[word] = dat.count(word)
    continue


# Filter Stopwords
keys = list(dict1)
filtered_words = [word for word in keys if word not in stopwords.words('english')]
dict2 = dict((k, dict1[k]) for k in filtered_words if k in filtered_words)

#keys in stopwords.words("english")

# Resort in list
# Reconvert to dictionary

def valueSelection(dictionary, length, startindex = 0): # length is length of highest consecutive value vector
    
    # Test input
    lengthDict = len(dictionary)
    if length > lengthDict:
        return print("length is longer than dictionary length");
    else:
        d = dictionary
        items = [(v, k) for k, v in d.items()]
        items.sort()
        items.reverse()   
        itemsOut = [(k, v) for v, k in items]
    
        highest = itemsOut[startindex:startindex + length]
        dd = dict(highest)
        wanted_keys = dd.keys()
        dictshow = dict((k, d[k]) for k in wanted_keys if k in d)

        return dictshow;
    
dictshow = valueSelection(dictionary = dict2, length = 7, startindex = 0)


# Plot
n = range(len(dictshow))
plt.bar(n, dictshow.values(), align='center')
plt.xticks(n, dictshow.keys())
plt.title("Most frequent Words")
plt.savefig("DEDA_Class_2022_410707007_Sentiment Analysis_a.png")
plt.show()


# Overview
overview =  valueSelection(dictionary = dict2, length =500, startindex = 0)
nOverview = range(len(overview.keys()))
plt.bar(nOverview, overview.values(), color = "g", tick_label = "")
plt.title("Word Frequency Overview")
plt.xticks([])
plt.savefig("DEDA_Class_2022_410707007_Sentiment Analysis_b.png")


import pysentiment as ps
# Sentiment Analysis
hiv4 = ps.HIV4()
tokens = hiv4.tokenize(cleantext)
score = hiv4.get_score(tokens)
print(score)
print('Positive:'+str(score['Positive']))
print('Negative:'+str(score['Negative']))
print('Polarity:'+str(score['Polarity']))
print('Subjectivity:'+str(score['Subjectivity']))

text_file = open("Joe Biden speech.txt", "w",encoding='UTF-8')

text_file.write('Joe Biden takes on Trump-era traumas in career-defining speech'+'\n')
text_file.write('Positive:'+str(score['Positive'])+'\n')
text_file.write('Negative:'+str(score['Negative'])+'\n')
text_file.write('Polarity:'+str(score['Polarity'])+'\n')
text_file.write('Subjectivity:'+str(score['Subjectivity'])+'\n')
text_file.close()


pd_tab = pd.DataFrame.from_dict(score, orient='index')
pd_tab.columns=['Joe Biden takes on Trump-era traumas in career-defining speech']
plt.figure('Joe Biden takes on Trump-era traumas in career-defining speech')             
ax = plt.axes(frame_on=False) 
ax.xaxis.set_visible(False)   
ax.yaxis.set_visible(False)
   
pd.plotting.table(ax, pd_tab.round(2), loc='center') 
plt.tight_layout()
plt.savefig('DEDA_Class_2022_410707007_Sentiment Analysis.png')  
#table_pd = pd.DataFrame(score)


# Polarity
# Formula: (Positive - Negative)/(Positive + Negative)

# Subjectivity
# Formula: (Positive + Negative)/N


