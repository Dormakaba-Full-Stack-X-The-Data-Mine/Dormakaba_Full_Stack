from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
import pandas as pd
import io
import csv
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__, template_folder='.')

def init_db():
    try:
        with sqlite3.connect('data.db') as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS hotels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_account TEXT NOT NULL,
                    sap_s8 TEXT NOT NULL,
                    hotel_inn_code TEXT,
                    marsha_code TEXT,
                    starlink_code TEXT,
                    vacation_rental BOOLEAN DEFAULT FALSE,
                    trade_name TEXT,
                    hotel_chain TEXT NOT NULL,
                    affiliation TEXT,
                    country TEXT NOT NULL,
                    street_number TEXT,
                    street_name TEXT,
                    zip_code TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")
        raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.json
        required_fields = ['customer_account', 'sap_s8', 'hotel_chain', 'country']
        
        # Validate required fields
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({
                "success": False,
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400
        
        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO hotels (
                    customer_account, sap_s8, hotel_inn_code, marsha_code,
                    starlink_code, vacation_rental, trade_name, hotel_chain,
                    affiliation, country, street_number, street_name, zip_code
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('customer_account'),
                data.get('sap_s8'),
                data.get('hotel_inn_code'),
                data.get('marsha_code'),
                data.get('starlink_code'),
                data.get('vacation_rental') == 'yes',
                data.get('trade_name'),
                data.get('hotel_chain'),
                data.get('affiliation'),
                data.get('country'),
                data.get('street_number'),
                data.get('street_name'),
                data.get('zip_code')
            ))
            
        return jsonify({
            "success": True,
            "message": "Data submitted successfully"
        })
        
    except sqlite3.Error as e:
        return jsonify({
            "success": False,
            "message": f"Database error: {str(e)}"
        }), 500
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error submitting data: {str(e)}"
        }), 500

@app.route('/export-csv')
def export_csv():
    try:
        with sqlite3.connect('data.db') as conn:
            df = pd.read_sql_query("SELECT * FROM hotels", conn)
        
        output = io.StringIO()
        df.to_csv(output, index=False)
        
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'hotel_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
        
    except sqlite3.Error as e:
        return jsonify({
            "success": False,
            "message": f"Database error: {str(e)}"
        }), 500
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error exporting data: {str(e)}"
        }), 500

@app.route('/upload-bulk', methods=['POST'])
def upload_bulk():
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "message": "No file selected"}), 400
    
    try:
        # Read the file based on its extension
        filename = secure_filename(file.filename)
        if filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        else:
            return jsonify({
                "success": False,
                "message": "Unsupported file format. Please upload CSV or Excel files only."
            }), 400
        
        # Validate required columns
        required_columns = ['customer_account', 'sap_s8', 'hotel_chain', 'country']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return jsonify({
                "success": False,
                "message": f"Missing required columns: {', '.join(missing_columns)}"
            }), 400
        
        success_count = 0
        error_count = 0
        errors = []
        
        with sqlite3.connect('data.db') as conn:
            for index, row in df.iterrows():
                try:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO hotels (
                            customer_account, sap_s8, hotel_inn_code, marsha_code,
                            starlink_code, vacation_rental, trade_name, hotel_chain,
                            affiliation, country, street_number, street_name, zip_code
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        row.get('customer_account'),
                        row.get('sap_s8'),
                        row.get('hotel_inn_code'),
                        row.get('marsha_code'),
                        row.get('starlink_code'),
                        row.get('vacation_rental', False),
                        row.get('trade_name'),
                        row.get('hotel_chain'),
                        row.get('affiliation'),
                        row.get('country'),
                        row.get('street_number'),
                        row.get('street_name'),
                        row.get('zip_code')
                    ))
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    errors.append(f"Row {index + 2}: {str(e)}")
        
        message = f"Successfully processed {success_count} rows."
        if error_count > 0:
            message += f" Failed to process {error_count} rows."
        
        return jsonify({
            "success": True,
            "message": message,
            "errors": errors if errors else None
        })
                
    except pd.errors.EmptyDataError:
        return jsonify({
            "success": False,
            "message": "The uploaded file is empty"
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error processing file: {str(e)}"
        }), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)