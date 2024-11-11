from flask import Flask, render_template, redirect, url_for, request, jsonify, send_file
from db import create_table, add_entry
import sqlite3
import pandas as pd
import io

app = Flask(__name__)
create_table()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        customer_account = request.form['customer_account']
        sap_s8 = request.form['sap_s8']
        hotel_inn_code = request.form.get('hotel_inn_code')
        marsha_code = request.form.get('marsha_code')
        starlink_code = request.form.get('starlink_code')
        vacation_rental = bool(request.form.get('vacation_rental'))
        trade_name = request.form.get('trade_name')
        hotel_chain = request.form['hotel_chain']
        affiliation = request.form.get('affiliation')
        country = request.form['country']
        street_number = request.form.get('street_number')
        street_name = request.form.get('street_name')
        zip_code = request.form.get('zip_code')
        
        add_entry(customer_account, sap_s8, hotel_inn_code, marsha_code, starlink_code, 
                  vacation_rental, trade_name, hotel_chain, affiliation, 
                  country, street_number, street_name, zip_code)
        return redirect(url_for('index'))
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/export-csv')
def export_csv():
    with sqlite3.connect('database.db') as conn:
        df = pd.read_sql_query("SELECT * FROM hotels", conn)
    output = io.BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return send_file(output, mimetype='text/csv', as_attachment=True, download_name='hotel_data.csv')

if __name__ == '__main__':
    app.run(debug=True)