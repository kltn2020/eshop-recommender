#!/usr/bin/python
import psycopg2
from config import config

HOST_IP = "35.213.174.112"
DB_NAME = "eshop"
USER_NAME = "phathdt379"
PASS = "password123"

def getData():
    """ Connect to the PostgreSQL database server """
    conn = None
    records = None
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
        records = [("id", "sku", "name", "brand_id", "cpu", "gpu", "os", "ram", "display", "display_resolution", "display_screen", "weight", "rating_avg", "discount_price")] + records;
        print("Total rows are:  ", len(records))
        
        for row in records:
            print (row)
            #print("Id: " + str(row[0]) + " os: " + str(row[6]) + " name: " +  row[2] + " - price: " + str(row[13]))
            #print("Id: " + str(row[0]))
	    # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    return records

if __name__ == '__main__':
    getData()