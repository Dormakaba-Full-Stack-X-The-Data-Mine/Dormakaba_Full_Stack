from flask import Flask, render_template, redirect, url_for, request, jsonify, send_file
from db import create_table, add_entry
import sqlite3
import pandas as pd
import io
from graphs import heatmap as hm
from graphs import pie 

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
        print("Database insertion error:", e)
        return jsonify({'message': 'Error inserting entry into the database.', 'success': False}), 500

@app.route('/export-csv')
def export_csv():
    with sqlite3.connect('database.db') as conn:
        df = pd.read_sql_query("SELECT * FROM hotels", conn)
    output = io.BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return send_file(output, mimetype='text/csv', as_attachment=True, download_name='hotel_data.csv')

    
@app.route('/heatmap')
def heatmap():
    img = hm.create_heatmap()
    return send_file(img, mimetype='image/png')

@app.route('/piechart')
def piechart():
    img = pie.create_pie_chart()
    return send_file(img, mimetype='image/png')
if __name__ == '__main__':
    app.run(debug=True)
