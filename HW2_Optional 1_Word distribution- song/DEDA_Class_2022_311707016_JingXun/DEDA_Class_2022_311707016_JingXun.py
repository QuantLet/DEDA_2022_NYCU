from PIL import Image
from wordcloud import WordCloud, STOPWORDS

text = open('lyrics.txt', encoding='utf-8').read()

stopwords = set(STOPWORDS)
stopwords.add('Oh')

wc = WordCloud(
    max_words = 1000,
    stopwords = stopwords,
    mode = 'RGBA',
    background_color = 'White',
    width=800,
    height=600
)

wc.generate(text)
wc.to_file('wordcloud.png')