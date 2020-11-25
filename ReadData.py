#!/usr/bin/python
import psycopg2
from config import config
from pandas import DataFrame
import codecs


HOST_IP = "localhost"
DB_NAME = "eshop"
USER_NAME = "postgres"
PASS = "password123"

def getData():
    """ Connect to the PostgreSQL database server """
    conn = None
    df = None

    try:
        # read connection parameters
        #params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        #conn = psycopg2.connect(**params)
        conn = psycopg2.connect(host=HOST_IP,
                database=DB_NAME,
                user=USER_NAME,
                password=PASS)
		
        # create a cursor
        cur = conn.cursor()
        
	    # execute a statement
        print('Get PostgreSQL data ...')
        sql_query = 'SELECT id, sku, name, brand_id, cpu, gpu, os, ram, display, display_resolution, display_screen, weight, rating_avg, discount_price FROM public.products ORDER BY id ASC'
        cur.execute(sql_query)

        # display the PostgreSQL database
        records = cur.fetchall()
        df = DataFrame(records)
        df.columns = [desc[0] for desc in cur.description]
        #print (df)

        print("Total rows are:  ", len(records))
        #records = [("id", "sku", "name", "brand_id", "cpu", "gpu", "os", "ram", "display", "display_resolution", "display_screen", "weight", "rating_avg", "discount_price")] + records;
        #print("Total rows are:  ", len(records))
        
        file = codecs.open("data.txt", "w", "utf-8")
        
        
        for row in records:
            #print (row)
            file.write('\n' + str(row))
            #print("Id: " + str(row[0]) + " os: " + str(row[6]) + " name: " +  row[2] + " - price: " + str(row[13]))
            #print("Id: " + str(row[0]))
	    # close the communication with the PostgreSQL
        cur.close()
        file.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    return df

if __name__ == '__main__':
    getData()