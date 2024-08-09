import requests
from bs4 import BeautifulSoup
import csv
import os

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

# Main script to extract data for all categories
home_url = 'http://books.toscrape.com/index.html'
category_urls = get_category_urls(home_url)

# Create a directory to store the CSV files
os.makedirs('book_data', exist_ok=True)

for category_url in category_urls:
    # Get the category name for file naming
    category_name = category_url.split('/')[-2]
    
    print(f'Extracting data for category: {category_name}')

    # Get all book URLs in the current category
    book_urls = get_book_urls(category_url)

    # List to hold all extracted data for this category
    all_books_data = []

    # Extract data for each book in the category
    for book_url in book_urls:
        book_data = extract_book_info(book_url)
        all_books_data.append(book_data)

    # Write the data to a CSV file for the current category
    with open(f'book_data/{category_name}_books_info.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=all_books_data[0].keys())
        writer.writeheader()
        writer.writerows(all_books_data)

    print(f'Data for category "{category_name}" has been written to book_data/{category_name}_books_info.csv')

print('Data extraction for all categories is complete.')
