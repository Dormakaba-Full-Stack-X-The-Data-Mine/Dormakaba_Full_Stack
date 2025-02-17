import pandas as pd
import sqlite3
def clean_customer_data(database):
    conn = sqlite3.connect(database)
    df = pd.read_sql_query("SELECT * FROM customer_data", conn)
    df = handle_missing_values(df)
    df = remove_duplicates(df)
    df = normalize_data(df)
    df = remove_unwanted_trade_names(df)
    conn.close()

    return df


def handle_missing_values(df):
    df = df.fillna('')

    return df

def remove_duplicates(df):
   
    # Drop duplicate rows based on a combination of columns
    df = df.drop_duplicates(subset=['Customer_account', 'SAP_S8_Customer', 'Hotel_Inn_Code', 
                                   'MARSHA_Code', 'Starlink_Code', 'Trade_Name', 'Hotel_Chain',
                                   'Affiliation', 'Street_Name', 'City', 'State', 'Country', 'Zip_Code'])
    return df

def normalize_data(df):
    df.columns = [col.replace(' ', '_') for col in df.columns]

    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].str.strip().str.capitalize()

    return df

def remove_unwanted_trade_names(df):

    df = df[~(df['Trade_Name'].isin(['nan', 'testing','test']) | 
              df['Trade_Name'].str.startswith('**') | 
              df['Trade_Name'].str.match(r'^[\d\W]+$'))]

    return df

