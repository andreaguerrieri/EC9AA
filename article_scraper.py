import sqlite3
import traceback

import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from itertools import count
from queries import save_article, connect_to_db
from utils import make_logger, BASE_LINK, INDEX_LINK, MIN_YEAR, month_string_to_number, read_config, Scraper_data

logger = make_logger()
total_num_of_articles = count()
conn = connect_to_db()



def scrape_articles(articles, day, month, year):
    """pipoday"""
    for article_ob in tqdm(articles):
        try:
            article_href = article_ob.a.get('href')
        except AttributeError:
            continue
        next(total_num_of_articles)
        save_article(conn,article_href,day,month,year)

def scrape_days(days, month, year):
    """pipo"""
    for day_ob in days:
        day = int(day_ob.text.replace(' ', '')[:2])
        if day < Scraper_data.last_day:
            continue# solo i giorni sono in ordine crescente
        day_href = day_ob.get('href')
        html_source = requests.get(BASE_LINK + day_href).text
        soup_object_day = BeautifulSoup(html_source, 'html.parser')
        articles = soup_object_day.body.find('div', id='content').findChildren('ul', recursive=True)[1]
        logger.info(f'saving approximately {int(len(articles)/2)} articles from day: {day}')
        scrape_articles(articles,day,month,year)
        del soup_object_day, html_source
        Scraper_data.last_day = day



def scrape_months(months, year):
    """popo"""
    for month_ob in months:
        month = month_ob.a.text
        month_href = month_ob.a.get('href')
        logger.info(f'scraping {month}')
        month_number = month_string_to_number(month)
        if month_number > Scraper_data.last_month:
            continue
        html_source = requests.get(BASE_LINK + month_href).text
        soup_object_month = BeautifulSoup(html_source, 'html.parser')
        def days_filter(day):
            MONTH_KEYWORD = '/home/sitemaparchive/day_'
            if 'href' in day.attrs.keys() and MONTH_KEYWORD in day.get('href'):
                return True
            else:
                return False
        filtered_days = filter(days_filter, soup_object_month.body.find('div', id = 'content').findChildren('a', recursive=True))
        scrape_days(filtered_days,month_number,year)
        del soup_object_month, html_source
        Scraper_data.last_month = month_number
        Scraper_data.last_day = 0

def scrape_years():
    html_source = requests.get(BASE_LINK+INDEX_LINK).text
    soup_object = BeautifulSoup(html_source, 'html.parser')
    all_years = soup_object.find('div', id='content').find('ul').findChildren('li', recursive=False)
    for year_ob in all_years:
        year = int(year_ob.h2.getText())
        if year < MIN_YEAR or year > Scraper_data.last_year:
            continue
        logger.info(f'Scraping {year}')
        months = year_ob.ul.findChildren('li', recursive=False)
        scrape_months(months, year)
        del months
        Scraper_data.last_year = year
        Scraper_data.last_month = 13
        Scraper_data.last_day = 0

def scrape():
    try:
        scrape_years()
    except Exception:
        logger.exception(traceback.print_exc())
    finally:
        conn.close()
        tot = next(total_num_of_articles)
        Scraper_data.total_articles_scraped = tot
        Scraper_data.save()
        logger.info(f'Total articles scraped: {tot}')

if __name__ == '__main__':
    scrape()
