import sqlite3
import time

import nltk
import psutil as psutil
from newspaper import Article
from queries import load_all_articles, connect_to_db, save_sentiment, load_specific_article, DB_FILE, load_not_null, \
    load_null
from utils import BASE_LINK, make_logger
from tqdm import tqdm
from nltk.sentiment import SentimentIntensityAnalyzer
import concurrent.futures
#modify options in manyarts to get specific articles, or to give links only

logger = make_logger()
database_art = sqlite3.connect(DB_FILE, check_same_thread=False)
manyarts = load_all_articles(database_art)
ranges = []
num_of_threads = 30
#nltk.download('vader_lexicon')
def get_sentiment(article):
    arturl = BASE_LINK+article[0]
    pd_article = Article(arturl, language='en')
    pd_article.download()
    pd_article.html
    pd_article.parse()
    arttext = pd_article.text
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(arttext)["compound"]

def loop_over_range(l_range : tuple):
    diff = l_range[1]-l_range[0]
    art_counter = 0
    for i in range(l_range[0], l_range[1]):
        article = manyarts[i]
        if article[4] == None:
            logger.info(f"Computing sentiment of article {art_counter} out of {diff}")
            try:
                sentiment = get_sentiment(article)
                logger.info(f"Saving {sentiment} to article {art_counter} out of {diff}")
                save_sentiment(database_art, article[0], sentiment)
            except Exception as ex:
                logger.exception(ex)
            art_counter+=1

def compute_threads_ranges():
    articles_per_thread = int(len(manyarts) / num_of_threads)
    logger.info(f"num_of_threads:{num_of_threads}, num_of_articles:{len(manyarts)}, articles_per_thread:{articles_per_thread}")
    start = 0
    for i in range(num_of_threads - 1):
        ranges.append((start, start + articles_per_thread))
        start = start + articles_per_thread + 1
    ranges.append((start, len(manyarts)))

def execute_sentiment_analysis():
    compute_threads_ranges()
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_of_threads+1) as executor:
        results = [executor.submit(loop_over_range, l_range) for l_range in ranges]

if __name__ == '__main__':
    execute_sentiment_analysis()
    total_articles = len(manyarts)
    database_art.close()
    del manyarts
    #print(load_all_articles(connect_to_db()))
    conn = connect_to_db()
    not_null =  load_not_null(conn)
    dim_n_n = len(not_null)
    del not_null
    diff = total_articles - dim_n_n
    if diff > 0:
        logger.info(f"Not NULL article: {dim_n_n}, still NULL articles  {diff}")
        null_arts = load_null(conn)
        for article in tqdm(null_arts):
            save_sentiment(conn, article[0], get_sentiment(article))
        conn.close()





