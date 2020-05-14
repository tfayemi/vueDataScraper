import bs4 as bs
import urllib.request
from urllib.request import urlopen as uReq
import json
from lxml import html
import requests
import re
import sys


#sauce = urllib.request.urlopen('https://www.makeupalley.com/product/searching.asp').read()
#soup = bs.BeautifulSoup(sauce, 'lxml')


filename = "makeupalley.json"
product_urls = []
json_data = ""
products_scraped = 0 

#mine_comments function is *UNUSED*, left for deeper comment scraping if required. 
def mine_comments(page):
    page_users = []
    page_comments = []
    item_id = ""
    reviews = 100
    comment_data = '\"comments\": {'
    
    product_sauce = urllib.request.urlopen(page).read()
    product_soup = bs.BeautifulSoup(product_sauce, 'lxml')

    #Get number of reviews
    for p in product_soup.find_all('p'):
        if "reviews" in str(p):
            if "class" not in str(p):
                reviews = int(p.text.strip('reviews'))


    #Aquire Item ID
    #Split URL
    page_split = page.split("/")
    #Comment Page URLs
    comment_page_urls = []
    #for each element in the split-string...
    for item in page_split:
        if "ItemId" in item:
            item_id = item
            if reviews < 10:
                next_url = "https://www.makeupalley.com/product/showreview.asp/page=1/pagesize=10/%s" %item_id
                comment_page_urls.append(next_url)
            else:
                for i in range(1, int(reviews/10)+1):
                    #create the new URL for the comments page.
                    next_url = "https://www.makeupalley.com/product/showreview.asp/page=%s/pagesize=10/%s" %(i, item_id)
                    #add the url to our existing list of urls to parse for comments!
                    comment_page_urls.append(next_url)

    
    #For each URL in our list now, collect all the user data on the page
    #And all the comment data on the page, in two distinct arrays.
    for url in comment_page_urls:
        url_sauce = urllib.request.urlopen(url).read()
        page_soup = bs.BeautifulSoup(url_sauce, 'lxml')
        #Add each user on the page to the user array. Or I guess, techincally, list.
        for user in page_soup.find_all('a', class_ = 'track_User_Profile'):
            page_users.append(user.text.encode('utf-8'))
        #Add each comment on the page to the comment array.
        for comment in page_soup.find_all('p', class_ = "break-word"):
            page_comments.append(comment.text.encode('utf-8'))
        #Extra loop to catch those tricky comments under a differnt class.
        for comment in page_soup.find_all('p', class_ = "1break-word"):
            page_comments.append(comment.text.encode('utf-8'))
        #Now, iterate through the users and commit the users + their corresponding comment,
        #To the data in JSON format to be returned by the function. Method. Whatever.
        for i in range(len(page_users)):
            try:
                comment_data = comment_data + "\"user\":" + "\"" + page_users[i].decode('ascii') + "\"" + "\n"
                try:
                    comment_data = comment_data + "\"comment\":" + "\"" + page_comments[i].decode('ascii') + "\"" + "\n"
                except UnicodeDecodeError:
                    comment_data = comment_data + "\"comment\":" + "\"" + str(page_comments[i]) + "\"" + "\n"                    
            except IndexError:
                print("IndexError on url: " + url + " ____Commenter: " + str(page_users[i]))
        
    return(comment_data)

def mine_page(page):
    img_no = 1
    data = ""
    reviews = 0
    page_users=[]
    page_comments = []
    comment_times = []
    
    try:
        product_sauce = urllib.request.urlopen(page).read()
    except UnicodeEncodeError:
        return('No Data Found')
    
    product_soup = bs.BeautifulSoup(product_sauce, 'lxml')
    
    #Product name
    for h1 in product_soup.find_all('h1'):
        if "MakeupAlley" not in str(h1):
            try:
                print(h1.text)
                data = data + "{\n\"product_name\" : " + " \"" + h1.text + "\"" + "\n"
            except UnicodeEncodeError:
                data = data + "{\n\"product_name\" : " + " \"" + str(h1) + "\"" + "\n"
    #Rating
    for h3 in product_soup.find_all('h3'):
        if 'class' not in str(h3):
            if 'Ingredients' not in str(h3):
                data = data + "\"Rating\" : " + h3.text + "\n"

    #Product Images
    for url in product_soup.find_all('a'):
        if 'data-lightbox' in str(url):
            img_url = url.get('href')
            data = data + "\"product_image_%s\" : " % (img_no) + " \"" + img_url + "\"" + "\n"
            img_no = img_no + 1
    
    #Item ID 
    page_split = page.split("/")
    #for each element in the split-string...
    for item in page_split:
        if "ItemId" in item:
            for value in item.split('='):
                if 'Item' not in value:
                    data = data + "\"product_id\":" + value + "\n"
                    
    #Number of Reviews
    for p in product_soup.find_all('p'):
        if "reviews" in str(p):
            if "class" not in str(p):
                reviews = int(p.text.strip('reviews'))
                data = data + "\"number_reviews\":" + p.text + "\n"
                
    #UPCCode
    match = re.search(r"[^a-zA-Z](id=\"UPCs\">)[^a-zA-Z]", str(product_soup))
    try:
        start = match.start(1) + 10
        UPC = str(product_soup)[start:start+12]
        data = data + "\"upc_code\": " + UPC + "\n"
    except AttributeError:
        UPC = "UPC UNAVAILABLE"
        data = data + "\"upc_code\": " + UPC + "\n"
            
    #Brand Name
    for a in product_soup.find_all('a', class_ = "track_BreadCrumbs_Brand"):
        data = data + "\"brand_name\":" + a.text + "\n"
        
    #Product Ingredients
    for span in product_soup.find_all('span'):
        if "hold-ingredients" in str(span):
            data = data + "\"ingredients\":" + "\"" +  span.text + "\"" + "\n"
        
    #Page Comments            
    for user in product_soup.find_all('a', class_ = 'track_User_Profile'):
        page_users.append(user.text.encode('utf-8'))
    for time in product_soup.find_all('p'):
        if "<span>on</span>" in str(time):
            comment_times.append(time.text)
    for comment in product_soup.find_all('p', class_ = "break-word"):
        page_comments.append(comment.text.encode('utf-8'))
    #Extra loop to catch those tricky comments under a different class.
    for comment in product_soup.find_all('p', class_ = "1break-word"):
        page_comments.append(comment.text.encode('utf-8'))
        
    data = data + "\"comments\": { \n"
    
    for i in range(len(page_users)):
            try:
                data = data + "\"user\":" + "\"" + page_users[i].decode('ascii') + "\"" + "\n"
                data = data + "\"timestamp\": " + "\"" + comment_times[i] + "\"" + "\n"
                try:
                    data = data + "\"comment\":" + "\"" + page_comments[i].decode('ascii') + "\"" + "\n"
                except UnicodeDecodeError:
                    data = data + "\"comment\":" + "\"" + str(page_comments[i]) + "\"" + "\n"                    
            except IndexError:
                print("IndexError on url: " + url + " ____Commenter: " + str(page_users[i]))

    return(data)


####### MAIN #########
print("Products Scraped...")
for i in range(1,68):
    split_ext = []
    product_url = 'https://www.makeupalley.com'
    sauce = urllib.request.urlopen("https://www.makeupalley.com/product/searching.asp/page=%s/pagesize=15/SD=/SC=/" %i)
    soup = bs.BeautifulSoup(sauce, 'lxml')
    for url in soup.find_all('a'):
        if "ItemId" in str(url):
            if "img" not in str(url):
                split_ext = str(url.get('href')).split("/")
                for i in range(len(split_ext)):
                    if "ItemId" in split_ext[i]:
                        split_ext.insert(i+1, "SortBy=helpful/AgeRange=/SkinToneType=")
                for i in range(len(split_ext)):
                    product_url = product_url + split_ext[i] + "/"
                if product_url not in product_urls:
                    product_urls.append(product_url)
                    json_data = json_data + mine_page(product_url)
                    data_file = open("makeupalley.json", 'a')
                    #print(json_data) #Left for testing purposes.
                    split_ext = []
                    product_url = 'https://www.makeupalley.com'
                    try:
                        data_file.write(json_data)
                        json_data = "" 
                        data_file.flush()
                    except UnicodeEncodeError:
                        print("Unicode encoding error")
                else:
                    split_ext = []
                    product_url = 'https://www.makeupalley.com'
    

print("Finished Scraping! Check JSON file for completed data.")
   
#Hope this works...