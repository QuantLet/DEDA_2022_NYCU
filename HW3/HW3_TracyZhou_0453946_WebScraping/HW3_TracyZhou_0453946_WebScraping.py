# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 17:37:14 2022

@author: Tracy Zhou
"""



from selenium import webdriver
import matplotlib.pyplot as plt
import re
import os
import pysentiment as ps


#path_direct = os.getcwd()
#os.chdir(path_direct + '/pyning')
p = "F:/Python/MyScript"
os.chdir(p)


# Start Selenium
browser = webdriver.Chrome()
#url = "http://teachingamericanhistory.org/library/document/what-to-the-slave-is-the-fourth-of-july/"
url = "https://www.federalreserve.gov/newsevents/speech/powell20220826a.htm"

# Extract text
browser.get(url)
text = browser.find_element('id', 'content').text
#print(text)
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
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords 
keys = list(dict1)
filtered_words = [word for word in keys if word not in stopwords.words('english')]
dict2 = dict((k, dict1[k]) for k in filtered_words if k in filtered_words)
# len(dict2) :520

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

# Save dictionaries for wordcloud
text_file = open("Output_Speech_by_JeromePowell.txt", "w")
text_file.write(str(cleantext))
text_file.close()


# Plot
n = range(len(dictshow))
plt.bar(n, dictshow.values(), align='center')
plt.xticks(n, dictshow.keys())
plt.title("Most frequent Words")
plt.savefig("plot_MostFrequentWords.png", transparent=True)

# Overview
# len(dict2) :520; set length < 520
overview =  valueSelection(dictionary = dict2, length = 500, startindex = 0)
nOverview = range(len(overview.keys()))
plt.bar(nOverview, overview.values(), color = "g", tick_label = "")
plt.title("Word Frequency Overview")
plt.xticks([])
plt.savefig("plot_WordFrequencyOverview.png", transparent=True)


# Sentiment Analysis
hiv4 = ps.HIV4()
tokens = hiv4.tokenize(cleantext)
score = hiv4.get_score(tokens)
print(score)

text_file = open("Output_score.txt", "w")
text_file.write(str(score))
text_file.close()

# Polarity
# Formula: (Positive - Negative)/(Positive + Negative)

# Subjectivity
# Formula: (Positive + Negative)/N



#####--------------- Part 2 : Custom Word Cloud --------------- #####
# Wordcloud

from wordcloud import WordCloud


# Read the whole text.
#text = browser.find_element('id', 'content').text
text = open(path.join(p, 'Output_Speech_by_JeromePowell.txt')).read()


# Generate a word cloud image
wordcloud = WordCloud().generate(text)

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
#plt.savefig("plot_Wordcloud.png", bbox_inches='tight',dpi=200,pad_inches=0.0)

# lower max_font_size
wordcloud = WordCloud(max_font_size=40).generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
#plt.show()
plt.savefig("plot_Wordcloud.png", bbox_inches='tight',dpi=200,pad_inches=0.1)


# The pil way (if you don't have matplotlib)
# image = wordcloud.to_image()
# image.show()

#####--------------- Part 3 : Latent Dirichlet Allocation (LDA) --------------- #####

import os
import re
from os import path

# d = os.environ['USERPROFILE'] + '\pyning'
# d = "F:/Users/user/pyning"
p = "F:/Users/user/scraping"


# text = browser.find_element('id', 'content').text
text = open(path.join(p, 'Output_Speech_by_JeromePowell.txt')).read()
doc_l = str.split(text)
doc_l.pop()[0]

doc_complete = doc_l

"""
# d = os.environ['USERPROFILE'] + '\pyning'
d = "C:/Users/Julian/pyning"

# Read the whole text.
cleantextprep = open(path.join(d, 'speeches.txt'), encoding = "utf8").read()
doc_l = str.split(text, sep = 'SPEECH')
doc_l.pop()[0]

doc_complete = doc_l
"""

doc_out = []
for l in doc_complete:
    
    cleantextprep = str(l)
    
    # Regex cleaning
    expression = "[^a-zA-Z ]" # keep only letters, numbers and whitespace
    cleantextCAP = re.sub(expression, '', cleantextprep) # apply regex
    cleantext = cleantextCAP.lower() # lower case 
    bound = ''.join(cleantext)
    doc_out.append(bound)


doc_complete = doc_out


import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
stop = set(stopwords.words('english'))
stop.add('going')
stop.add('know')
exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized


doc_clean = [clean(doc).split() for doc in doc_complete]    


# Importing Gensim
import gensim
from gensim import corpora

# Creating the term dictionary of our courpus, where every unique term is assigned an index.
dictionary = corpora.Dictionary(doc_clean)

# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]



# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

# Running and Trainign LDA model on the document term matrix.
ldamodel = Lda(doc_term_matrix, num_topics=3, id2word = dictionary, passes=20)


print(ldamodel.print_topics(num_topics=3, num_words=10))

text_file = open("Output_LDAmodel.txt", "w")
text_file.write(str(ldamodel.print_topics(num_topics=3, num_words=10)))
text_file.close()