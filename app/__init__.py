from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import csv
from instance.config import app_config

from app.models import Database, Invoice

db = Database()
cur = db.cur

def create_app(config_name):
    """
    Flask object  Returns it after it is loaded
    with configurations settings
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
 
    @app.route('/upload', methods=['POST'])
    def upload_data():
        file = request.files['file']
        csv_file_path = 'SalesInvoiceTemplate.csv'
        with open(csv_file_path, 'r') as f:
            cmd = 'COPY invoices FROM STDIN CSV HEADER'
            print(type(cmd))
            cur.copy_expert(cmd, f)
            db.conn.commit()
            
        return "Success"

    return app
