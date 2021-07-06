import np as np
from newspaper import Article
from queries import load_all_articles, connect_to_db
from utils import BASE_LINK
import nltk
from tqdm import tqdm
from nltk.sentiment import SentimentIntensityAnalyzer

#modify options in manyarts to get specific articles, or to give links only

database_art = connect_to_db()
manyarts = load_all_articles(database_art, month=2, year=2020, day=1)

# test sentiment analysis on a single url, then we move to loops

# firstart = BASE_LINK+manyarts[4][0]
#
# pd_article = Article(firstart, language='en')
# pd_article.download()
# pd_article.html
# pd_article.parse()
# arttext = pd_article.text
# #arttext2 = (nltk.word_tokenize(arttext))
#
# #load stopwords
# stopwords = nltk.corpus.stopwords.words("english")
#
# #remove stopwords from corpus-seems like it's not needed tho
# words = [w for w in arttext if w.lower() not in stopwords if w.isalpha()]
#
# #makes frequency distribution of words
# #fd = nltk.FreqDist(words)
#
# # sentiment intensity from nltk-stopwords will still be there
# sia = SentimentIntensityAnalyzer()
# print(sia.polarity_scores(arttext))


# now we try looping
# score=0
#
# for article in manyarts:
#     arturl = BASE_LINK+article[0]
#     pd_article = Article(arturl, language='en')
#     pd_article.download()
#     pd_article.html
#     pd_article.parse()
#     arttext = pd_article.text
#     sia = SentimentIntensityAnalyzer()
#     score += sia.polarity_scores(arttext)["compound"]
#     print(score)
# scoreavg = score/len(manyarts)

scoreday = []
scoremonth = []
scoreyear = []


for k in range(27):
    for j in range(12):
        for i in tqdm(range(24)):
            manyarts = load_all_articles(database_art, day=i, month=j, year=k)
            for article in manyarts:
                arturl = BASE_LINK+article[0]
                pd_article = Article(arturl, language='en')
                pd_article.download()
                pd_article.html
                pd_article.parse()
                arttext = pd_article.text
                sia = SentimentIntensityAnalyzer()
                scoreday += sia.polarity_scores(arttext)["compound"]
        scoremonth = scoreday
        print(scoremonth)
    scoreyear = scoremonth
