from flask import Flask, request, jsonify, render_template, send_file
import sqlite3
import csv
import os

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_account TEXT,
            sap_s8 TEXT,
            hotel_inn_code TEXT,
            marsha_code TEXT,
            starlink_code TEXT,
            trade_name TEXT,
            hotel_chain TEXT,
            affiliation TEXT,
            street_number TEXT,
            street_name TEXT,
            zip_code TEXT,
            country TEXT
        )''')
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-entry', methods=['POST'])
def submit_entry():
    data = request.json
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO entries (customer_account, sap_s8, hotel_inn_code, marsha_code, starlink_code,
                          trade_name, hotel_chain, affiliation, street_number, street_name, zip_code, country)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (data['customer_account'], data['sap_s8'], data['hotel_inn_code'], data['marsha_code'],
                        data['starlink_code'], data['trade_name'], data['hotel_chain'], data['affiliation'],
                        data['street_number'], data['street_name'], data['zip_code'], data['country']))
        conn.commit()
    return jsonify({'message': 'Entry submitted successfully!', 'success': True})

@app.route('/export-csv')
def export_csv():
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM entries")
        entries = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]

    with open('entries.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(entries)
    return send_file('entries.csv', as_attachment=True)

@app.route('/generate-graphs')
def generate_graphs():
    # Call your Python scripts for generating graphs
    os.system('python3 generate_graphs.py')  # Replace with actual script path
    return jsonify({'message': 'Graphs generated successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
