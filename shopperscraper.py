'''
Created on Jul 24, 2017

@author: ToluwaFayemi
'''
import bs4 as bs
import urllib.request
from urllib.request import urlopen as uReq
import json
from lxml import html
import requests

filename = "shoppers_data.json"
product_urls = []
json_data = "" 

def mine_page(page):
    #img_no = 1
    data = ""
    page_users = []
    page_comments = []
    
    product_sauce = urllib.request.urlopen(page).read()
    product_soup = bs.BeautifulSoup(product_sauce, 'lxml')
    
    #Product Name
    for h1 in product_soup.find_all('div', class_ = "hidden", itemprop = "name"):
        data = data + "{\n\"product_name\" : " + " \"" + h1.text + "\"" + "\n"
        print(h1.text)
        
    #Rating
    for rating in product_soup.find_all('span', itemprop = 'ratingValue', limit = 1):
        data = data + "\"rating\" : " + rating.text + "\n"
        
    #ProductID/ProductSKU
    for data_script in product_soup.find_all('script'):
        if 'ecommerce' in str(data_script):
            data_elements=data_script.text.split("\n")
            for elem in data_elements:
                if "productSKU" in elem:
                    broken_elem = elem.split("?")
                    second_broken_elem = broken_elem[1].split("\"")
                    data = data + "\"product_SKU\":" + second_broken_elem[1] + "\n"
                                    
    #Page Comments
    data = data + "\"comments\": {\n"
    for comment_section in product_soup.find_all('div', id = "bvseo-reviewsSection"):
        for user in comment_section.find_all('span', itemprop = "author"):
            page_users.append(user.text.encode('utf-8'))
        for comment in product_soup.find_all('span', itemprop = "description"):
            page_comments.append(comment.text.encode('utf-8'))
            
    for i in range(0, len(page_users)):
        try:
            data = data + "\"users\":" + "\"" + page_users[i].decode('ascii') + "\"" + "\n"
            data = data + "\"comment\":" + "\"" + page_comments[i].decode('ascii') + "\"" + "\n"    
        except UnicodeDecodeError:
            data = data + "\"users\":" + "\"" + str(page_users[i]) + "\"" + "\n"
            data = data + "\"comment\":" + "\"" + str(page_comments[i]) + "\"" + "\n"    
    
    return(data)


print("Products Scraped...")
for i in range(0,23):
    url = 'https://www.beautyboutique.ca/Categories/Makeup/c/MakeUp?page=' + str(i) + '&q=%3Atrending&text=&sort=trending&facetType='
    sauce = urllib.request.urlopen(url)
    soup= bs.BeautifulSoup(sauce, 'lxml')
    for extension in soup.find_all('a', class_ = 'product-img'):
        product_url = "https://www.beautyboutique.ca" + str(extension.get('href'))
        if product_url not in product_urls:
            product_urls.append(product_url)
            try:
                json_data = json_data + mine_page(product_url)
                #print(json_data) #Left for testing purposes.
                data_file = open("shoppers.json", 'a')
            except urllib.error.HTTPError:
                json_data = json_data + "\n\n - MISSING LINK - \n\n"
            try:
                data_file.write(json_data)
                json_data = "" 
                data_file.flush()
            except UnicodeEncodeError:
                print("Unicode Encode Error")
                
print("Finished Scraping! Check JSON file for completed data.")
        