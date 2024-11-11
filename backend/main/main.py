from flask import Flask, render_template, request,send_file
import sqlite3
from graphs import heatmap as hm

app = Flask(__name__, template_folder='../../frontend')

def init_db():
    with sqlite3.connect('data.db') as conn:  
        cursor = conn.cursor() #Creating table this is only done the first time the data base is made
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS my_table (
                customer_account INTEGER PRIMARY KEY,
                SAP_S8 INTEGER NOT NULL,
                HOTEL_CHAIN TEXT NOT NULL
            )
        ''')
        conn.commit()

def insert_data(name, value):
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO my_table (name, value) VALUES (?, ?)', (name, value))#adds the rows of the file to the db
        conn.commit()

@app.route('/') # Displaying HTML CODE
def index():
    return render_template('index.html')

@app.route('/insert', methods=['POST'])#post is giving data to someother place, so here is 
def insert():
    name = request.form.get('name')
    value = request.form.get('value')
    if name and value:
        insert_data(name, value)
        return f"Inserted {name} with value {value} into the database!"
    return "Failed to insert data."


@app.route('/heatmap')
def heatmap():
    img = hm.create_heatmap()
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    init_db()  
    app.run(debug=True)
