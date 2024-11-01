from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
import pandas as pd
import io

app = Flask(__name__, template_folder='../../frontend')

def init_db():
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hotels (
                customer_account INTEGER PRIMARY KEY,
                sap_s8 INTEGER NOT NULL,
                hotel_inn_code TEXT,
                marsha_code TEXT,
                starlink_code TEXT,
                vacation_rental BOOLEAN,
                trade_name TEXT,
                hotel_chain TEXT NOT NULL,
                affiliation TEXT,
                country TEXT NOT NULL,
                street_number TEXT,
                street_name TEXT,
                zip_code TEXT
            )
        ''')
        conn.commit()

def insert_hotel_data(data):
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO hotels (
                customer_account, sap_s8, hotel_inn_code, marsha_code,
                starlink_code, vacation_rental, trade_name, hotel_chain,
                affiliation, country, street_number, street_name, zip_code
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['customer_account'], data['sap_s8'], data['hotel_inn_code'],
            data['marsha_code'], data['starlink_code'], data['vacation_rental'],
            data['trade_name'], data['hotel_chain'], data['affiliation'],
            data['country'], data['street_number'], data['street_name'],
            data['zip_code']
        ))
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/insert', methods=['POST'])
def insert():
    try:
        data = request.get_json()
        insert_hotel_data(data)
        return jsonify({"success": True, "message": "Data inserted successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/export-csv')
def export_csv():
    with sqlite3.connect('data.db') as conn:
        df = pd.read_sql_query("SELECT * FROM hotels", conn)
    
    output = io.StringIO()
    df.to_csv(output, index=False)
    
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='hotel_data.csv'
    )

if __name__ == '__main__':
    init_db()
    app.run(debug=True)