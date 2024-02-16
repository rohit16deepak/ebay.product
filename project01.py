import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_user_input():
    query = input("Enter your search query: ")
    max_pages = int(input("Enter the maximum number of pages to scrape: "))
    return query, max_pages

def construct_search_url(base_url, query):
    return f'{base_url}/sch/i.html?_from=R40&_nkw={query}'

def getpagedata(page, all_products):
    page_data = []
    for data in all_products:
        productName = data.find('h3', class_='s-item__title')
        if productName:
            productName = productName.text.strip()
        else:
            productName = 'product name not available'

        # Get seller information
        seller_info = data.find('span', class_='s-item__seller-info')
        if seller_info:
            seller_info_text = seller_info.text.strip()
            seller_rating = int(''.join(filter(str.isdigit, seller_info_text)))  # Extract seller rating
            if seller_rating >= minimum_ratings:
                # Check if seller offers products from specified brands
                seller_brands = [brand.lower() for brand in brands]
                if any(brand.lower() in seller_info_text.lower() for brand in seller_brands):
                    # Get product price
                    product_price = data.find('span', class_='s-item__price')
                    if product_price:
                        product_price = product_price.text.strip()
                        # Check if product price is above minimum
                        if float(product_price.replace('$', '').replace(',', '')) >= minimum_average_price:
                            # Get product subtitle
                            product_subtitle = data.find('div', class_='s-item__subtitle')
                            product_subtitle_text = product_subtitle.text.strip() if product_subtitle else 'Product subtitle not available'
                            # Handling total rating
                            product_total_rating = data.find('span', class_='s-item__reviews-count')
                            if product_total_rating:
                                product_total_rating = product_total_rating.text.strip()
                            else:
                                product_total_rating = '0'
                            # Get product shipping
                            product_shipping = data.find('span', class_='s-item__location s-item__itemLocation')
                            if product_shipping:
                                product_shipping = product_shipping.text.strip()
                            else:
                                product_shipping = 'Location not available'

                            # Create dictionary for product data
                            product = {'productName': productName,
                                       'productSubtitle': product_subtitle_text,
                                       'ProductPrice': product_price,
                                       'ProductTotalRating': product_total_rating,
                                       'productShipping': product_shipping,
                                       'productSeller': seller_info_text}
                            page_data.append(product)
    return page_data

query, max_pages = get_user_input()
base_url = "https://www.ebay.com"
url = construct_search_url(base_url, query)
brands = ["Rockshox", "Shimano", "raceface"]
minimum_ratings = 100  # Minimum number of ratings
minimum_average_price = 100  # Minimum average item price

totaldata = []

for page in range(1, max_pages + 1):
    r = requests.get(f"{url}&_pgn={page}")
    html = r.content
    soup = BeautifulSoup(html, 'html.parser')
    all_products = soup.find_all('div', class_='s-item__info')
    data = getpagedata(page, all_products)
    print("Page:", page)
    print("Number of items found on this page:", len(data))  # Check the number of items scraped on this page
    totaldata.extend(data)

# Check the total number of items scraped
print("Total number of items scraped:", len(totaldata))

# Writing data to Excel
datatable = pd.DataFrame(totaldata)
print(datatable.head())  # Print the first few rows of the DataFrame to check if it contains the expected data
datatable.to_excel(f"{query}_Products.xlsx", index=False)

