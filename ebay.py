import requests
from bs4 import BeautifulSoup
import pandas as pd

# Taking user input for the query
query = str(input("Enter your search query : "))

# Constructing the eBay search URL with the query
url = f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw={query}&_sacat=0'
itemlist = []

r = requests.get(url)
html = r.content

soup = BeautifulSoup(html, 'html.parser')

# Adjusted the class name to match the eBay page structure
all_products = soup.find_all('div', class_='s-item__info')

def getpagedata(page):
    page_data = []
    for data in all_products:
        productName = data.find('div', class_='s-item__title')
        if productName:
            productName=productName.text.strip()
        else:
            productName='product name not available'
        productStatus = data.find('span',class_="SECONDARY_INFO")
        if productStatus:
            productStatus=productStatus.text.strip()
        else:
            productStatus='Product subtitle not available'
        
        # Handling total rating
        ProductTotalRating = data.find('span', class_='s-item__reviews-count')
        if ProductTotalRating:
            ProductTotalRating = ProductTotalRating.text.strip()
        else:
            ProductTotalRating = '0'
        
        ProductPrice = data.find('span', class_='s-item__price')
        if ProductPrice:
            ProductPrice = ProductPrice.text.strip()
        else:
            ProductPrice = 'Price not available'
        productshiping=data.find('span',class_='s-item__location s-item__itemLocation')
        if productshiping:
            productshiping=productshiping.text.strip()
        else:
            productshiping='location not available'
        productseller=data.find('span',class_='s-item__seller-info')
        if productseller:
            productseller=productseller.text.strip()
        else:
            productseller='seller not available'
        
        products = {'productName': productName, 
                    'productStatus': productStatus, 
                    'ProductPrice': ProductPrice,  
                    'ProductTotalRating': ProductTotalRating,
                    'productshiping':productshiping,
                    'product seller':productseller}
        page_data.append(products)
    return page_data

totalPages = int(input("Enter no. pages to scrap: "))
totaldata = []
page = 1
while page <= totalPages:
    data = getpagedata(page)
    print("Page:", page)
    totaldata.extend(data)
    page += 1  

# Writing data to Excel
datatable = pd.DataFrame(totaldata)
datatable.to_excel(f"{query}_product.xlsx", index=False)
