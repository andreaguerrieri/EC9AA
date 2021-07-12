import np as np
from newspaper import Article
from queries import load_all_articles, connect_to_db, save_sentiment, load_specific_article
from utils import BASE_LINK
import nltk
from tqdm import tqdm
from nltk.sentiment import SentimentIntensityAnalyzer

#modify options in manyarts to get specific articles, or to give links only

database_art = connect_to_db()
manyarts = load_all_articles(database_art)

def get_sentiment(article):
    arturl = BASE_LINK+article[0]
    pd_article = Article(arturl, language='en')
    pd_article.download()
    pd_article.html
    pd_article.parse()
    arttext = pd_article.text
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(arttext)["compound"]

for article in tqdm(manyarts):
    if article[4] == None:
        save_sentiment(database_art, article[0], get_sentiment(article))
    #print(load_specific_article(database_art,article[0]))

