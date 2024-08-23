import requests
from bs4 import BeautifulSoup
import csv
import time
import logging

logging.basicConfig(filename='scraper.log', level=logging.INFO)

# Base URL of the website
base_url = 'http://books.toscrape.com'

def get_category_urls(home_url):
    response = requests.get(home_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    category_links = soup.find('div', class_='side_categories').find_all('a')
    category_urls = [base_url + '/' + link['href'] for link in category_links if link['href'] != '../']
    
    return category_urls

def get_book_urls(category_url):
    book_urls = []
    while category_url:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        books = soup.find_all('h3')
        for book in books:
            book_page = book.find('a')['href']
            book_urls.append(base_url + '/catalogue/' + book_page)
        
        # Pagination
        next_button = soup.find('li', class_='next')
        if next_button:
            next_page_url = next_button.find('a')['href']
            category_url = base_url + '/catalogue/category/books/' + next_page_url
        else:
            break
    
    return book_urls

def extract_book_info(book_url):
    logging.info(f"Fetching {book_url}")
    try:
        response = requests.get(book_url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {book_url}: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the required information
    product_page_url = book_url
    upc = soup.find('th', string='UPC').find_next_sibling('td').text
    book_title = soup.find('h1').text
    price_including_tax = soup.find('th', string='Price (incl. tax)').find_next_sibling('td').text
    price_excluding_tax = soup.find('th', string='Price (excl. tax)').find_next_sibling('td').text
    quantity_available = soup.find('th', string='Availability').find_next_sibling('td').text.strip()

    product_description_tag = soup.find('div', id='product_description')
    if product_description_tag:
        product_description = product_description_tag.find_next('p').text
    else:
        product_description = 'No description available'

    category = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()
    review_rating = soup.find('p', class_='star-rating')['class'][1]
    image_url = soup.find('img')['src'].replace('../../', 'http://books.toscrape.com/')

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

def write_books_to_csv(books_data, category_name):
    # Define CSV file name
    csv_filename = f'{category_name}_books.csv'
    
    # Define CSV headers
    csv_headers = [
        'product_page_url',
        'universal_product_code (upc)',
        'book_title',
        'price_including_tax',
        'price_excluding_tax',
        'quantity_available',
        'product_description',
        'category',
        'review_rating',
        'image_url'
    ]

    # Write data to CSV file
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=csv_headers)
        writer.writeheader()
        writer.writerows(books_data)

    print(f'Data for category "{category_name}" has been written to {csv_filename}')

def monitor_books():
    home_url = base_url
    category_urls = get_category_urls(home_url)
    for category_url in category_urls:
        print(f"Extracting data for category: {category_url}")
        book_urls = get_book_urls(category_url)

        all_books_data = []

        # Loop through each book URL in the category
        for i, book_url in enumerate(book_urls, start=1):
            print(f"Processing book {i} of {len(book_urls)}: {book_url}")
            book_data = extract_book_info(book_url)
            if book_data:
                all_books_data.append(book_data)
            time.sleep(1)  # Optional delay to be polite to the server

        # Write the book data to CSV
        category_name = category_url.split('/')[-2]  # Extract category name from URL
        write_books_to_csv(all_books_data, category_name)

if __name__ == "__main__":
    monitor_books()
