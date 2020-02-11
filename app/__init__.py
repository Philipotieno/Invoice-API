import os
import csv
import datetime
from operator import itemgetter
import datetime


from flask import Flask, abort, jsonify, request
from werkzeug.utils import secure_filename

from app.models import Database, Invoice
from flask_cors import CORS
from instance.config import app_config

db = Database()
cur = db.cur

ALLOWED_EXTENSIONS = set(['csv'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_app(config_name):
    """
    Flask object  Returns it after it is loaded
    with configurations settings
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    CORS(app)

    @app.route('/invoices', methods=['POST'])
    def upload_file_data():
        '''
            - This route locates files from the sytem and only upload file with the allowed extention
        '''
        if 'file' not in request.files:  # check if the post request has the file part
            msg = jsonify({
                'error': 'No file part'
            }), 409

        file = request.files['file']
        if file.filename == '':
            msg = jsonify({
                'error': 'No file selected for uploading'
            }), 409
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            try:
                new_filename = 'temp.csv'
                new_filename2 = 'temp2.csv'
                with open(filename, 'r') as source:
                    with open(new_filename, 'w') as result:
                        writer = csv.writer(result, lineterminator='\n')
                        reader = csv.reader(source)
                        source.readline()
                        for row in reader:
                            ts = row[12]
                            tx = row[13]
                            ts = datetime.datetime.strptime(ts, "%d/%m/%Y").strftime("%Y-%m-%d")
                            tx = datetime.datetime.strptime(tx, "%d/%m/%Y").strftime("%Y-%m-%d")
                            if ts != "" and tx != "":
                                row[12] = ts
                                row[13] = tx
                                writer.writerow(row)
                with open(new_filename, 'r') as f:
                    # creating a csv reader object
                    reader = csv.reader(f)
                    with open(new_filename2, 'w') as output_file:
                        writer = csv.writer(output_file, delimiter=',')

                        # Get specific columns and write them on the new csv file
                        writer.writerows(
                            map(itemgetter(0, 10, 12, 13, 16, 17, 18), reader))

                # Open new file and copy the items to the invoices table
                contactnames = Invoice.check_data()
                if len(contactnames) == 0:
                    with open(new_filename2, 'r') as r:
                        reader = csv.reader(r)
                        cmd = "COPY invoices FROM STDIN WITH (FORMAT CSV, HEADER TRUE)"
                        cur.copy_expert(cmd, r)
                        db.conn.commit()

                        # Covert the csv file into a dictionary
                        dictreader = csv.reader(open(new_filename2))
                        result = {}
                        for row in dictreader:
                            result[row[0]] = row[1:]
                        os.remove(new_filename)
                        os.remove(new_filename2)

                        msg = jsonify({
                            'success': 'File successfully uploaded',
                            'invoice': result
                        }), 201
                else:
                    msg = jsonify({
                        'message' : 'clear the database to add new data'
                        })
            except Exception as e:
                msg = jsonify({"Error": str(e)}), 422
        else:
            msg = jsonify({
                'error': 'Allowed file types is csv only'
            }), 422

        return msg

    @app.route('/invoices/topcustomers', methods=['GET'])
    def get_top_invoices():
        '''
            - This route gets top five cutomers according the amount due
        '''
        invoices = Invoice.get_top_customers()
        if invoices:
            return jsonify({
                'invoices': invoices,
                'total': len(invoices)
            }), 200
        return jsonify({'message': 'No invoices are available!'}), 404

    @app.route('/invoices/transactions', methods=['POST'])
    def get_transactions():
        '''
            - This route returns the last 30 transactions from any given date
        '''
        data = request.get_json()['date']

        if datetime.datetime.strptime(data, '%Y-%m-%d'):
            invoices = Invoice.transactions_query(data)
            if invoices:
                return jsonify({
                    'invoices': invoices,
                    'message': 'found {} transactions'.format(len(invoices))
                }), 200
            return jsonify({'message': 'No transctions before that date'}), 404
        return jsonify({
            "message": "wrong date format"
        })

    @app.route('/invoices/summary', methods=['GET'])
    def get_summary():
        '''
            - This route returns a summary of total amount incurred for each month in every year
        '''
        invoices = Invoice.get_summary()
        if invoices:
            return jsonify({
                'Invoice': invoices,
                'total': len(invoices)
            }), 200
        return jsonify({'message': 'No invoices are available!'}), 404

    return app