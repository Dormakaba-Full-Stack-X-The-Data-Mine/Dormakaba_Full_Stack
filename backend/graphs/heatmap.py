import sqlite3
import seaborn as sns
import matplotlib.pyplot as plt
import io

def create_heatmap():
    conn = sqlite3.connect('database.db')
    
    query = '''
        SELECT 
            customer_account,
            sap_s8,
            hotel_inn_code,
            marsha_code,
            starlink_code,
            vacation_rental,
            trade_name,
            hotel_chain,
            affiliation,
            country,
            street_number,
            street_name,
            zip_code
        FROM hotels
    '''
    
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    
    columns = [description[0] for description in cursor.description]
    
    conn.close()
    
    na_map = []
    for row in data:
        na_map.append([1 if value is None else 0 for value in row])
    
    na_map = list(map(list, zip(*na_map)))
    
    plt.figure(figsize=(25, 10))
    sns.heatmap(na_map, cbar=False, cmap='Paired', yticklabels=columns)
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    
    return img
