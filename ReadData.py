#!/usr/bin/python
import psycopg2
from config import config

def getData():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	    # execute a statement
        print('Get PostgreSQL data ...')
        sql_query = 'SELECT id, sku, name, brand_id, cpu, gpu, os, ram, display, display_resolution, display_screen, weight, rating_avg, discount_price FROM public.products ORDER BY id ASC'
        cur.execute(sql_query)

        # display the PostgreSQL database
        records = cur.fetchall()
        print("Total rows are:  ", len(records))
        
        #for row in records:
            #print("Id: " + str(row[0]) + " sku: " + str(row[1]) + " name: " +  row[2] + " - price: " + str(row[13]))
       
	    # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    getData()