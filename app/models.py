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
                        InvoiceNumber VARCHAR NOT NULL,
                        InvoiceDate VARCHAR NOT NULL,
                        DueDate VARCHAR NOT NULL,
                        Description VARCHAR NOT NULL,
                        Quantity VARCHAR NOT NULL,
                        UnitAmount VARCHAR NOT NULL
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
        """initialize with name."""
        self.ContactName = ContactName
        self.InvoiceNumber = InvoiceNumber
        self.InvoiceDate = InvoiceDate
        self.DueDate = DueDate
        self.Description = Description
        self.Quantity = Quantity
        self.UnitAmount = UnitAmount