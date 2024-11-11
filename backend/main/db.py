import sqlite3

def create_connection():
    conn = sqlite3.connect('database.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
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
        zip_code TEXT
    )
    ''')
    conn.commit()
    conn.close()

def add_entry(customer_account, sap_s8, hotel_inn_code, marsha_code, 
              starlink_code, vacation_rental, trade_name, hotel_chain, 
              affiliation, country, street_number, street_name, zip_code):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO hotels (customer_account, sap_s8, hotel_inn_code, marsha_code, 
                            starlink_code, vacation_rental, trade_name, hotel_chain, 
                            affiliation, country, street_number, street_name, zip_code) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (customer_account, sap_s8, hotel_inn_code, marsha_code, starlink_code, 
          vacation_rental, trade_name, hotel_chain, affiliation, country, 
          street_number, street_name, zip_code))
    conn.commit()
    conn.close()