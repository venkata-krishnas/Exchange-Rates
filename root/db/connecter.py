import json
import sys
import mariadb
import datetime

class exchange():
    def __init__(self):
        with open("./root/db/config.json",'r') as configfile:
            self.credentials = json.load(configfile)

    def __createconnection(self):
        try:
            self.conn = mariadb.connect(
            user=self.credentials['user'],
            password=self.credentials['password'],
            host=self.credentials['host'],
            port=self.credentials['port'],
            database=self.credentials['database']
        )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
# Get Cursor
        self.cur = self.conn.cursor()
        return self.cur

    def getcredentials(self):
        return self.credentials
    
    def rundbquery(self,query):
        cur = self.__createconnection()
        cur.execute(query)
        self.conn.commit()
        # for row in cur:
        #     print(row)
        return cur
        # for i in cur:
        #     print(i)
    

exchangeobj = exchange()

def update(date, rates):
    # print("UPDATE store VALUES('{}','{}') WHERE date='{}'".format(date, rates,date))
    try:
        exchangeobj.rundbquery("UPDATE store SET price='{}' WHERE date = '{}'".format(rates,date))
    except Exception as e:
        print(e)


def insert(date, rates):
    try:
        exchangeobj.rundbquery("INSERT INTO store VALUES('{}','{}')".format(date, rates))
    except Exception as e:
        print(e)

def get(date):
    try:
        print(date)
        print( "SELECT price FROM store WHERE date = '{}';".format(date) )
        cur = exchangeobj.rundbquery("SELECT price FROM store WHERE date = '{}';".format(date))
        return cur
    except Exception as e:
        print(e)
# data = storeobj.rundbquery("SELECT customer_name,count(customer_id) FROM g_store2 WHERE discount>0.5 group by(customer_id)")
# from datetime import date
# day = str(datetime.date(2023,1,23))
# print(day)
# insert(day, '{"id": 1, "name": "Monty"}')