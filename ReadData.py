# import module/lib using
import psycopg2
from config import config
from pandas import DataFrame
import codecs
import os

# define default env
DB_HOST_IP = 'localhost'
DB_NAME = 'eshop'
DB_USER_NAME = 'postgres'
DB_USER_PASS = 'password123'

HOST_IP = os.getenv('DB_HOST_IP', DB_HOST_IP)
DB_NAME = os.getenv('DB_NAME', DB_NAME)
USER_NAME = os.getenv('DB_USER_NAME', DB_USER_NAME)
PASS = os.getenv('DB_USER_PASS', DB_USER_PASS)

# write file function


def writeFile(list, fileName):
    file = codecs.open(fileName, "w", "utf-8")
    for row in list:
        file.write('\n' + str(row))

    file.close()

# items info


def getDataProducts():
    conn = None
    df = None

    try:
        # read connection parameters
        # params = config()
        # connect to the PostgreSQL server
        # print('Connecting to the PostgreSQL database...')
        # conn = psycopg2.connect(**params)
        conn = psycopg2.connect(host=HOST_IP,
                                database=DB_NAME,
                                user=USER_NAME,
                                password=PASS)

        cur = conn.cursor()
        sql_query = 'SELECT * FROM public.products ORDER BY id ASC'
        cur.execute(sql_query)

        records = cur.fetchall()
        df = DataFrame(records)
        df.columns = [desc[0] for desc in cur.description]

        #print("Total rows are:  ", len(records))
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            #print('Database connection closed.')

    return df

# user review info


def getDataReviews():
    conn = None
    df = None

    try:
        # read connection parameters
        # params = config()
        # connect to the PostgreSQL server
        # print('Connecting to the PostgreSQL database...')
        # conn = psycopg2.connect(**params)
        conn = psycopg2.connect(host=HOST_IP,
                                database=DB_NAME,
                                user=USER_NAME,
                                password=PASS)

        cur = conn.cursor()
        sql_query = 'SELECT * FROM public.reviews'
        cur.execute(sql_query)

        records = cur.fetchall()
        df = DataFrame(records)
        df.columns = [desc[0] for desc in cur.description]

        #print("Total rows are:  ", len(records))
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            #print('Database connection closed.')

    return df
