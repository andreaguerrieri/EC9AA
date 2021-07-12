import sqlite3

DB_FILE = 'articles.db'

def connect_to_db():
    return sqlite3.connect(DB_FILE)

def save_article(conn, link, day, month, year, extra = None):
    query = """INSERT OR REPLACE INTO articles(link, day, month, year, extra) VALUES (?,?,?,?,?);"""
    c = conn.cursor()
    c.execute(query,(link, day, month, year, extra))
    conn.commit()

def load_all_articles(conn, day=None, month=None, year=None, load_link_only = False):
    var_names = {'0': 'day', '1': 'month', '2': 'year'}
    var_values = {'0': day, '1': month, '2': year}
    c = conn.cursor()
    if load_link_only:
        link = 'link'
    else:
        link = '*'
    query = f"SELECT {link} FROM articles"
    sel_counter = 0
    for index, selector in enumerate([day, month, year]):
        if selector != None:
            if sel_counter == 0:
                query += " WHERE "
            elif sel_counter >= 1:
                query += " AND "
            query += f"{var_names[str(index)]} = {var_values[str(index)]}"
            sel_counter += 1
    query+= ';'
    c.execute(query)
    return c.fetchall()

def load_specific_article(conn, link_value, load_link_only = False):
    if load_link_only:
        link = 'link'
    else:
        link = '*'
    query = f'SELECT {link} FROM articles WHERE link = "{link_value}"'
    c = conn.cursor()
    c.execute(query)
    return c.fetchall()

def save_sentiment(conn, link, sentiment):
    query =  f'''UPDATE articles SET extra = {str(sentiment)} WHERE link = "{link}"'''
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    c.close()

if __name__ == '__main__':
   # print(load_all_articles(connect_to_db(),year= 2021, month= 6, day=1 ))
    conn = connect_to_db()
    print(load_specific_article(conn,"/tvshowbiz/article-9642401/Former-WAG-Phoebe-Burgess-32-does-school-run-fashion-week.html"))
    save_sentiment(conn,"/tvshowbiz/article-9642401/Former-WAG-Phoebe-Burgess-32-does-school-run-fashion-week.html", '1.0')

    print(load_specific_article(conn,"/tvshowbiz/article-9642401/Former-WAG-Phoebe-Burgess-32-does-school-run-fashion-week.html"))