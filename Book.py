import requests
from bs4 import BeautifulSoup
import csv

# URL of the book page to scrape
book_url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

# Send a GET request to the book page
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

# Define the CSV file headers
headers = [
    'product_page_url', 'universal_product_code (upc)', 'book_title',
    'price_including_tax', 'price_excluding_tax', 'quantity_available',
    'product_description', 'category', 'review_rating', 'image_url'
]

# Write the data to a CSV file
with open('book_info.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerow([
        product_page_url, upc, book_title, price_including_tax,
        price_excluding_tax, quantity_available, product_description,
        category, review_rating, image_url
    ])

print('Data has been written to book_info.csv')
