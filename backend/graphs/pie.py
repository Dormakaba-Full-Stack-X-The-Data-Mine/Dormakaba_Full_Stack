import sqlite3
import matplotlib.pyplot as plt
import io

def create_pie_chart():
    conn = sqlite3.connect('database.db')
    
    query = '''
        SELECT affiliation
        FROM hotels
    '''
    
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    
    conn.close()
    
    affiliation_counts = {}
    for row in data:
        affiliation = row[0]
        if affiliation in affiliation_counts:
            affiliation_counts[affiliation] += 1
        else:
            affiliation_counts[affiliation] = 1
    
    sorted_affiliations = sorted(affiliation_counts.items(), key=lambda x: x[1], reverse=True)
    
    top_affiliations = sorted_affiliations[:6]
    other_count = sum(count for _, count in sorted_affiliations[6:])
    if other_count > 0:
        top_affiliations.append(("Other", other_count))
    
    labels, sizes = zip(*top_affiliations)
    
    plt.figure(figsize=(10, 7))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    
    return img
