import requests
from bs4 import BeautifulSoup
import csv
import os
import time
from datetime import datetime

# Function to extract book information
def extract_book_info(book_url):
    response = requests.get(book_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the required information
    product_page_url = book_url
    upc = soup.find('th', text='UPC').find_next_sibling('td').text
    book_title = soup.find('h1').text
    price_including_tax = soup.find('th', text='Price (incl. tax)').find_next_sibling('td').text
    price_excluding_tax = soup.find('th', text='Price (excl. tax)').find_next_sibling('td').text
    quantity_available = soup.find('th', text='Availability').find_next_sibling('td').text.strip()
    product_description = soup.find('div', id='product_description').find_next('p').text
    category = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()
    review_rating = soup.find('p', class_='star-rating')['class'][1]
    image_url = soup.find('img')['src'].replace('../../', 'http://books.toscrape.com/')

    # Return the extracted information as a dictionary
    return {
        'product_page_url': product_page_url,
        'universal_product_code (upc)': upc,
        'book_title': book_title,
        'price_including_tax': price_including_tax,
        'price_excluding_tax': price_excluding_tax,
        'quantity_available': quantity_available,
        'product_description': product_description,
        'category': category,
        'review_rating': review_rating,
        'image_url': image_url
    }

# Function to get all book URLs in a category, handling pagination
def get_book_urls(category_url):
    book_urls = []
    while category_url:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all product page URLs on the current page
        book_links = soup.find_all('h3')
        for link in book_links:
            book_urls.append('http://books.toscrape.com/catalogue/' + link.find('a')['href'].replace('../../../', ''))

        # Check if there is a next page, if so, update category_url
        next_button = soup.find('li', class_='next')
        category_url = 'http://books.toscrape.com/catalogue/' + next_button.find('a')['href'] if next_button else None

    return book_urls

# Function to get all category URLs
def get_category_urls(home_url):
    response = requests.get(home_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all category links
    categories = soup.find('ul', class_='nav nav-list').find('ul').find_all('a')
    category_urls = ['http://books.toscrape.com/' + category['href'] for category in categories]
    
    return category_urls

# Function to check for price changes
def check_price_changes(old_data, new_data):
    changes = []
    for old, new in zip(old_data, new_data):
        if old['price_including_tax'] != new['price_including_tax'] or old['quantity_available'] != new['quantity_available']:
            changes.append({
                'book_title': new['book_title'],
                'old_price': old['price_including_tax'],
                'new_price': new['price_including_tax'],
                'old_quantity': old['quantity_available'],
                'new_quantity': new['quantity_available'],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
    return changes

# Function to load previous data
def load_previous_data(filepath):
    if not os.path.exists(filepath):
        return []
    
    with open(filepath, 'r', newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)

# Function to save data
def save_data(filepath, data):
    with open(filepath, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

# Main script to monitor all categories
def monitor_books():
    home_url = 'http://books.toscrape.com/index.html'
    category_urls = get_category_urls(home_url)

    # Create a directory to store the CSV files
    os.makedirs('book_data', exist_ok=True)
    os.makedirs('price_logs', exist_ok=True)

    for category_url in category_urls:
        # Get the category name for file naming
        category_name = category_url.split('/')[-2]
        
        print(f'Extracting data for category: {category_name}')

        # Get all book URLs in the current category
        book_urls = get_book_urls(category_url)

        # Extract data for each book in the category
        all_books_data = [extract_book_info(book_url) for book_url in book_urls]

        # Load previous data
        previous_data_file = f'book_data/{category_name}_books_info.csv'
        previous_data = load_previous_data(previous_data_file)

        # Check for price changes if there's previous data
        if previous_data:
            changes = check_price_changes(previous_data, all_books_data)
            if changes:
                log_file = f'price_logs/{category_name}_price_changes.csv'
                save_data(log_file, changes)
                print(f'Price changes detected and logged in {log_file}')

        # Save the current data
        save_data(previous_data_file, all_books_data)
        print(f'Data for category "{category_name}" has been updated.')

    print('Monitoring cycle complete.')

# Run the monitoring script
monitor_books()

