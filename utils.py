import logging
from configparser import ConfigParser
LOGGER_NAME = 'root'
BASE_LINK = 'https://www.dailymail.co.uk'
INDEX_LINK = '/home/sitemaparchive/index.html'
MIN_YEAR = 1994

def read_config():
    parser = ConfigParser()
    parser.read('config.ini')
    return parser

class Scraper_data :
    last_day = read_config().getint('scraper_data','last_day', fallback=0)
    last_month = read_config().getint('scraper_data','last_month', fallback=13)
    last_year = read_config().getint('scraper_data','last_year', fallback=500000)
    total_articles_scraped = 0
    @staticmethod
    def save():
        parser = read_config()
        parser.set('scraper_data', 'last_day', str(Scraper_data.last_day))
        parser.set('scraper_data', 'last_month', str(Scraper_data.last_month))
        parser.set('scraper_data', 'last_year', str(Scraper_data.last_year))
        parser.set('scraper_data', 'total_articles_scraped', str(Scraper_data.total_articles_scraped))
        with open('config.ini', 'w') as configfile:
            parser.write(configfile)

def make_logger():
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s - %(threadName)s'))
    file_handler = logging.FileHandler('errors.log', mode='w')
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(logging.Formatter(
        '%(levelname)s-%(asctime)s\nmessagge: %(message)s\nmodule: %(module)s\nfunction: %(funcName)s\nline: %(lineno)d\n'))
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


def month_string_to_number(string):
    m = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr':4,
         'may':5,
         'jun':6,
         'jul':7,
         'aug':8,
         'sep':9,
         'oct':10,
         'nov':11,
         'dec':12
        }
    s = string.strip()[:3].lower()

    try:
        out = m[s]
        return out
    except:
        raise ValueError(f'{s} is not a month')