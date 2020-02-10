import os
import csv
import datetime
from operator import itemgetter

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
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    CORS(app)


    @app.route('/', methods=['POST'])
    def upload_file():
        # check if the post request has the file part
        if 'file' not in request.files:
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            msg = jsonify({
                'success' : 'File successfully uploaded'
            })
        else:
            msg = jsonify({
                'error': 'Allowed file types is csv only'
            }), 422

        return msg

    @app.route('/invoices', methods=['POST'])
    def upload_data():
        file = request.files['filename']
        try:
            filename = 'SalesInvoiceTemplate.csv'
            new_filename = 'NewSalesInvoiceTemplate.csv'

            with open(filename, 'r') as f:

                # creating a csv reader object
                reader = csv.reader(f)
                with open(new_filename, 'w') as output_file:
                    writer = csv.writer(output_file, delimiter=',')

                    # Get specific columns and write them on the new csv file
                    writer.writerows(
                        map(itemgetter(0, 10, 12, 13, 16, 17, 18), reader))

                # Open new file and copy the items to the invoices table
                with open(new_filename, 'r') as r:
                    reader = csv.reader(r)
                    cmd = "COPY invoices FROM STDIN WITH (FORMAT CSV, HEADER TRUE)"
                    cur.copy_expert(cmd, r)
                    db.conn.commit()

                # Covert the csv file into a dictionary
                dictreader = csv.reader(open(new_filename))
                result = {}
                for row in dictreader:
                    result[row[0]] = row[1:]

                return jsonify({
                    'success': True,
                    'invoice': result
                }), 201
        except Exception as e:
            return jsonify({"Error": str(e)}), 422

    @app.route('/invoices', methods=['GET'])
    # gets top 5 invoices 
    def get_top_invoices():
        invoices = Invoice.get_top_customers()
        if invoices:
            return jsonify({
                'Invoice': invoices,
                'total': len(invoices)
            }), 200
        return jsonify({'message': 'No invoices are available!'}), 404

    @app.route('/invoices/transactions', methods=['POST'])
    def get_transactions():
        data = request.get_json()['date']

        if datetime.datetime.strptime(data, '%Y-%m-%d'):
            invoices = Invoice.transactions_query(data)
            if invoices:
                return jsonify({
                    'Invoice': invoices,
                    'total': len(invoices)
                }), 200
            return jsonify({'message': 'No invoices are available for the provided date'}), 404
        return jsonify({
            "message": "wrong date format"
        })

    @app.route('/invoices/summary', methods=['GET'])
    def get_summary():
        invoices = Invoice.get_summary()
        if invoices:
            return jsonify({
                'Invoice': invoices,
                'total': len(invoices)
            }), 200
        return jsonify({'message': 'No invoices are available!'}), 404

    return app
