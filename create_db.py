from os import path

from queries import connect_to_db, DB_FILE

CREATE_TABLE = "CREATE TABLE articles ( link text, day integer, month integer, year integer, extra text, UNIQUE(link))"
def create_table():
    if path.exists(DB_FILE):
        print('database already exist please delete '+ DB_FILE)
        return
    conn = connect_to_db()
    c = conn.cursor()
    c.execute(CREATE_TABLE)
    conn.commit()
    print('articles table created')
    conn.close()


if __name__ == '__main__':
    create_table()
