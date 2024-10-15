import requests
import json
import os
import mysql.connector  # Import for MySQL
from exam_names import exam_names

# Set up your Google Search API key and Custom Search Engine ID
API_KEY = 'AIzaSyB6UHAMTx9odZni0cwDhLmT6Mj81m83FaQ'
SEARCH_ENGINE_ID = '77c0d992b4fda4357'

db_config = {
    'host': 'localhost',
    'user': 'root',   # replace with your MySQL username
    'password': 'Anshika@123',  # replace with your MySQL password
    'database': 'exam_data'
}

def connect_to_db():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def load_existing_data(conn):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT exam_name FROM exams")
    rows = cursor.fetchall()
    return rows

def exam_exists(exam_name, existing_data):
    # Check if the exam already exists in the loaded data
    for exam in existing_data:
        if exam['exam_name'].lower() == exam_name.lower():
            return True
    return False

def insert_exam_data(conn, exam_name, title, link):
    cursor = conn.cursor()
    # Using ON DUPLICATE KEY UPDATE to handle duplicates
    sql = """
    INSERT IGNORE INTO exams (exam_name, title, link) 
    VALUES (%s, %s, %s)
    """
    cursor.execute(sql, (exam_name, title, link))
    conn.commit()

def search_exam_info(exam_name):
    query = f"{exam_name} official website"
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = []
        for item in data.get('items', []):
            exam_info = {
                'exam_name': exam_name,
                'title': item.get('title'),
                'link': item.get('link'),
            }
            results.append(exam_info)
        return results
    else:
        return []

if __name__ == '__main__':
    # Connect to the MySQL database
    conn = connect_to_db()
    if conn is None:
        exit()

    # Load existing data from MySQL
    existing_exam_data = load_existing_data(conn)

    new_exam_data = []

    # Loop through each exam name and search for its official website
    for exam in exam_names:
        if not exam_exists(exam, existing_exam_data):
            # Only add if the exam doesn't exist in the current data
            exam_data = search_exam_info(exam)
            if exam_data:
                for data in exam_data:
                    insert_exam_data(conn, data['exam_name'], data['title'], data['link'])
                    new_exam_data.append(data)

    conn.close()

    print(f"Scraped and saved data for {len(new_exam_data)} new exams.")
