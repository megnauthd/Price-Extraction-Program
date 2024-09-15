# Book Price Monitoring System
Overview
This Python-based application extracts book data, including prices and images, from the "Books to Scrape" website. It scrapes data from all available categories and saves the data into structured CSV files, along with downloading and saving book cover images.

# Key Features:
Scrapes book data (title, price, availability, and more) from an online bookstore.
Downloads book cover images.
Saves data into CSV files organized by book category.
Logs actions and errors for monitoring.
Prerequisites
Before running this program, ensure that you have the following software installed:

Python 3.10 or higher
pip (Python package manager)
virtualenv (Optional but recommended)
Setup Instructions
1. Clone the Repository
First, clone the repository to your local machine:

bash
git clone https://github.com/megnauthd/Price-Extraction-Program.git
cd book-price-monitoring
2. Set Up the Virtual Environment
You can optionally use a virtual environment to avoid conflicts between dependencies. To create and activate a virtual environment, run the following commands:

On macOS/Linux:
bash

python3 -m venv venv
source venv/bin/activate
On Windows:
bash
python -m venv venv
venv\Scripts\activate
3. Install Dependencies
Once inside the virtual environment, install the required dependencies:

bash
pip install -r requirements.txt
Running the Application
After setting up the environment and installing dependencies, you can run the script:
bash
python3 book.py
The script will extract book data for all categories and save it into CSV files. It will also download the corresponding book cover images and store them in the appropriate folders.
Output
CSV Files: The program generates a separate CSV file for each book category containing details like book title, price, availability, and more. These files are named based on the category, e.g., fiction_books.csv.
Images: Book cover images are downloaded and saved locally in folders named after their corresponding categories.
Logging
A scraper.log file is created to track the actions of the scraper and log any errors that occur during the execution.

# How to Modify
If you'd like to modify the script or change the behavior:

Modify the URL: You can change the base URL in the book.py file to scrape data from other similar websites.
CSV Structure: Adjust the columns or modify the information extracted for each book in the extract_book_info function.
Troubleshooting
HTTP Errors: If the program fails due to HTTP issues, check the connection or server availability.
Permission Errors: Ensure you have write permissions to save CSV files and images in the directory.
Future Enhancements
Schedule automated runs of the scraper using cron jobs (Linux/macOS) or Task Scheduler (Windows).
Load the data into a database instead of CSV files for easier analysis and querying.
Add functionality to track price changes over time.
License
This project is licensed under the MIT License.