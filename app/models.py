import os
import psycopg2
from psycopg2.extras import RealDictCursor
# from dotenv import load_dotenv
# load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor(cursor_factory=RealDictCursor)


class Database:
    '''constructor initialize environment'''

    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL)
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)

    def create_tables(self):
        """ Method to create tables """
        invoices = '''CREATE TABLE IF NOT EXISTS invoices(
                        ContactName VARCHAR NOT NULL,
                        InvoiceNumber INT NOT NULL,
                        InvoiceDate DATE NOT NULL,
                        DueDate DATE NOT NULL,
                        Description VARCHAR NOT NULL,
                        Quantity INT NOT NULL,
                        UnitAmount INT NOT NULL
                    );'''

        queries = [invoices]
        for q in queries:
            self.cur.execute(q)
            self.conn.commit()
        print("All tables created successfully!")

    def drop_tables(self):
        '''Method to drop tables'''
        query = "DROP TABLE invoices;"
        self.cur.execute(query)
        self.conn.commit()
        print("All tables dropped successfully!")
        self.cur.close()


class Invoice:
    def __init__(self, ContactName, InvoiceNumber, InvoiceDate, DueDate, Description, Quantity, UnitAmount):
        """invoice constructor"""
        self.ContactName = ContactName
        self.InvoiceNumber = InvoiceNumber
        self.InvoiceDate = InvoiceDate
        self.DueDate = DueDate
        self.Description = Description
        self.Quantity = Quantity
        self.UnitAmount = UnitAmount

    @staticmethod
    def get_top_customers():
        """ Fetch top customers using unitamount"""
        query = "SELECT contactname,\
                (quantity*unitamount) as totalamountdue from invoices\
                ORDER BY unitamount DESC LIMIT 5;"
        cur.execute(query)
        invoices = cur.fetchall()

        return invoices
    
    @staticmethod
    def get_summary():
        """ Fetch invoice summary"""
        query = "SELECT date_part('year', duedate) AS year, date_part('month', duedate) AS month,\
                SUM(quantity*unitamount) as totalamountdue from invoices\
                GROUP BY year, month ORDER BY year, month;"

        cur.execute(query)
        invoices = cur.fetchall()

        return invoices


    @staticmethod
    def transactions_query(data):
        """ get lastt 30 transactions """
        query = "SELECT duedate,\
            (quantity*unitamount) as totalamountdue from invoices\
            WHERE duedate < '{}' ORDER BY duedate DESC LIMIT 30;".format(data)
        cur.execute(query)
        invoices = cur.fetchall()

        return invoices