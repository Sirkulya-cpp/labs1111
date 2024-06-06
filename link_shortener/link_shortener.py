import base64
import hashlib

#import sqlite3
import psycopg2

db_params = {
    'host': 'link_postgres_db',  # Вказуйте іменоване ім'я сервісу PostgreSQL
    'port': '5432',
    'user': 'user',  # Ваш користувач PostgreSQL
    'password': 'password',  # Ваш пароль PostgreSQL
    'database': 'microservices'  # Ваша база даних PostgreSQL
}


def check_link_exists(link):
    
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    
    cursor.execute("SELECT EXISTS(SELECT 1 FROM links WHERE long_url = %s)", (link,))
    
    result = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    
    print(result)
    return result


def check_shorten_link_exists(link):
    
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    cursor.execute("SELECT EXISTS(SELECT 1 FROM links WHERE short_url = %s)", (link,))
    
    result = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    
    return result


def link_shorten_request(link_text):

    link_exist = check_link_exists(link_text)
    
    if link_exist:

        print("Getting old link from database")
        
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        cursor.execute("SELECT short_url FROM links WHERE long_url = %s", (link_text,))
        shorten_link = cursor.fetchone()[0]
        
        cursor.close()
        connection.close()
        
        return shorten_link
    
    else:

        print("Adding new ling to database")
        
        shorten_link = generate_short_link(link_text)
        
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        
        cursor.execute("INSERT INTO links (long_url, short_url) VALUES (%s, %s)", (link_text, shorten_link))
        
        cursor.close()
        connection.commit()
        connection.close()
        
        return shorten_link


def link_lengthen_request(link_text):

    if check_shorten_link_exists(link_text):
        
        print("Getting long link from database")
        
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        
        cursor.execute("SELECT long_url FROM links WHERE short_url = %s", (link_text,))
        shorten_link = cursor.fetchone()[0]
        
        cursor.close()
        connection.close()
        
        print(shorten_link)
        
        return shorten_link
    
    else:
        
        raise Exception("Wrong link")


'''
def link_shorten_request(link_text):
    link_exist = check_link_exists(link_text)
    if link_exist:
        print("Getting old link from database")
        conn = sqlite3.connect('links.db')
        cursor = conn.cursor()
        cursor.execute("SELECT short_url FROM links WHERE long_url = ?",
                       (link_text,))
        shorten_link = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return shorten_link
    else:
        print("Adding new ling to database")
        shorten_link = generate_short_link(link_text)
        conn = sqlite3.connect('links.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO links (long_url, short_url) VALUES (?, ?)",
                       (link_text, shorten_link))
        cursor.close()
        conn.commit()
        conn.close()
        return shorten_link

def link_lengthen_request(link_text):
    if check_shorten_link_exists(link_text):
        print("Getting long link from database")
        conn = sqlite3.connect('links.db')
        cursor = conn.cursor()
        cursor.execute("SELECT long_url FROM links WHERE short_url = ?",
                       (link_text,))
        shorten_link = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        print(shorten_link)
        return shorten_link
    else:
        raise Exception("Wrong link")

def check_link_exists(link):
    conn = sqlite3.connect('links.db')
    cursor = conn.cursor()
    cursor.execute("SELECT EXISTS(SELECT 1 FROM links WHERE long_url = ?)",
                   (link,))
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    print(result)
    return result

def check_shorten_link_exists(link):
    conn = sqlite3.connect('links.db')
    cursor = conn.cursor()
    cursor.execute("SELECT EXISTS(SELECT 1 FROM links WHERE short_url = ?)",
                   (link,))
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return result
'''


def generate_short_link(long_url):
    # encoded_bytes = base64.b64encode(text.encode('utf-8'))
    # encoded_text = encoded_bytes.decode('utf-8')
    md5_hash = hashlib.md5(long_url.encode()).hexdigest()
    short_url = md5_hash[:8]
    return short_url

def decode_short_link(encoded_text):
    decoded_bytes = base64.b64decode(encoded_text.encode('utf-8'))
    decoded_text = decoded_bytes.decode('utf-8')
    return decoded_text

def adder(a: int, p: str) -> int:
    b = a + p
    return b
