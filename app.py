import requests
import json
import os
from urllib.parse import urlparse
from exam_names import exam_names
# Set up your Google Search API key and Custom Search Engine ID
API_KEY = 'AIzaSyB6UHAMTx9odZni0cwDhLmT6Mj81m83FaQ'
SEARCH_ENGINE_ID = '77c0d992b4fda4357'


def load_existing_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []

def exam_exists(exam_name, existing_data):
    # Check if the exam already exists in the loaded data
    for exam in existing_data:
        if exam['exam_name'].lower() == exam_name.lower():
            return True
    return False

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

query = "List of competitive exams in India 2024 for get engineering college"

def search_competitive_exams(query):
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        exam_names = []
        for item in data.get('items', []):
            title = item.get('title', '').strip()
            # Extracting possible exam names from titles
            exam_names.append(title)
        return exam_names
    else:
        print(f"Error: Unable to fetch data from Google Search API (Status Code: {response.status_code})")
        return []
    
if __name__ == '__main__':
    # Load existing data from exam_data.json if it exists

    
    filename = 'exam_data.json'
    existing_exam_data = load_existing_data(filename)

    new_exam_data = []

    # Loop through each exam name and search for its official website
    for exam in exam_names:
        if not exam_exists(exam, existing_exam_data):
            # Only add if the exam doesn't exist in the current data
            exam_data = search_exam_info(exam)
            if exam_data:
                new_exam_data.extend(exam_data)

    # Combine existing data with new data
    all_exam_data = existing_exam_data + new_exam_data

    # Save all exam data to JSON file for frontend usage
    with open(filename, 'w') as f:
        json.dump(all_exam_data, f, indent=4)

    print(f"Scraped and saved data for {len(new_exam_data)} new exams.")
