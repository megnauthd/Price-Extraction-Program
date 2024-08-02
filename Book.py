import requests
from bs4 import BeautifulSoup
import pandas as pd

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

# Print the extracted information for debugging
print(f'product_page_url: {product_page_url}')
print(f'universal_product_code (upc): {upc}')
print(f'book_title: {book_title}')
print(f'price_including_tax: {price_including_tax}')
print(f'price_excluding_tax: {price_excluding_tax}')
print(f'quantity_available: {quantity_available}')
print(f'product_description: {product_description}')
print(f'category: {category}')
print(f'review_rating: {review_rating}')
print(f'image_url: {image_url}')

# Create a dictionary with the extracted data
data = {
    'product_page_url': [product_page_url],
    'universal_product_code (upc)': [upc],
    'book_title': [book_title],
    'price_including_tax': [price_including_tax],
    'price_excluding_tax': [price_excluding_tax],
    'quantity_available': [quantity_available],
    'product_description': [product_description],
    'category': [category],
    'review_rating': [review_rating],
    'image_url': [image_url]
}

# Convert the dictionary to a pandas DataFrame
df = pd.DataFrame(data)

# Write the DataFrame to a CSV file
df.to_csv('book_info.csv', index=False)

print('Data has been written to book_info.csv')
