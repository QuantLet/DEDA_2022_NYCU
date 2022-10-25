
#import nltk
#nltk.download()

from selenium import webdriver
import matplotlib.pyplot as plt
import re
from nltk.corpus import stopwords
import os
from selenium.webdriver.common.by import By
#import pysentiment as ps
#from wordcloud import WordCloud


#path_direct = os.getcwd()
#os.chdir(path_direct + '/pyning')
#p = r""
#os.chdir(p)


# Start Selenium
browser = webdriver.Chrome(r"D:\DEDA_Class_2022_410707007_Oration in Memory of Abraham Lincoln\chromedriver.exe")
url = "https://teachingamericanhistory.org/document/oration-in-memory-of-abraham-lincoln/"



# Extract text
browser.get(url)

#content = browser.find_element_by_class_name("t-single__content-Body-content")
content = browser.find_element(By.CLASS_NAME, "t-single__content-Body-content") #
text = content.text
browser.close()
browser.stop_client()

# find and delete <...> combinations
# find and delete /...> combinations
# Takes only lists as input
# Returns list as output

"""

def SearchAndReplaceSeq(html, opensign, closesign):
    
        openbool = False
        nText = range(len(text))
        
        for i in nText:
            
            print("i = ", i)
            print("outer loop")
            
            if text[i] in opensign:
                loc = opensign.index('<')
                openbool = True
                print("deleting ", text[i])  
                text[i] = "" # delete
                
                while openbool:         
                            print("inner loop")
                            
                            if text[i] != closesign[loc]:
                                print(i, "deleting ", text[i])  
                                text[i] = ""
                                i += 1
                            
                            else:
                                print(i, "deleting ", text[i])  
                                text[i] = ""
                                openbool = False
                                i += 1
                                                        
                

                #continue # switch to next mark, first one is always open

            else:
                print("keeping", text[i])
                print("outer loop down")
                continue #i += 1     
                
        return(text); 

                     
textout = SearchAndReplaceSeq(html = text, opensign = ['<', '/', '{'], closesign = ['>', '>', '}'])

s = "".join(textout)   

"""

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

# Save dictionaries for wordcloud
text_file = open("Output.txt", "w")
text_file.write(str(cleantext))
text_file.close()


# Plot
n = range(len(dictshow))
plt.bar(n, dictshow.values(), align='center')
plt.xticks(n, dictshow.keys())
plt.title("Most frequent Words")
plt.savefig("DEDA_Class_2022_410707007_Oration in Memory of Abraham Lincoln_a.png")
plt.show()


# Overview
overview =  valueSelection(dictionary = dict2, length = 1000, startindex = 0)
nOverview = range(len(overview.keys()))
plt.bar(nOverview, overview.values(), color = "g", tick_label = "")
plt.title("Word Frequency Overview")
plt.xticks([])
plt.savefig("DEDA_Class_2022_410707007_Oration in Memory of Abraham Lincoln_b.png")


import pysentiment as ps
# Sentiment Analysis
hiv4 = ps.HIV4()
tokens = hiv4.tokenize(cleantext)
score = hiv4.get_score(tokens)
print(score)




# Polarity
# Formula: (Positive - Negative)/(Positive + Negative)

# Subjectivity
# Formula: (Positive + Negative)/N



"""
# Wordcloud
inputWordcloud = str(dict2.keys())
# Generate a word cloud image
wordcloud = WordCloud(path.join("symbola.ttf")).generate(inputWordcloud)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

wordcloud2 = WordCloud(max_font_size=40).generate(inputWordcloud)
plt.figure()
plt.imshow(wordcloud2, interpolation="bilinear")
plt.axis("off")
plt.show()

dict2.index("would")
dict2.get("would")
dict2.keys()
"""

