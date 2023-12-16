from bs4 import BeautifulSoup
import requests


page = "https://www.ebay.co.uk/itm/126234336851?hash=item1d64271e53:g:RNUAAOSwse9leYGK&amdata=enc%3AAQAIAAAAsG1nSN%2Fxk2hV0Rp1sYNOY2IrNOmdy%2FEQWOC9RSjNE4TVpKIJr0BBdE5wKQA5yVieNl2OlaIxd4ITNs4dmMWmwfdjCGVqRHzRWFWa5sl3GpEHYR1P3RA7v5U%2BOIKbUBSeKYuGMLew1L7ultJNZF9YXqHdwA54%2B2XLVml1v6AgBbxVEyMUcwAmbem461dRQNAEwcWhGwGWkB74DkEmga4lm71OzrHYLVZO2AG27IAly5lK%7Ctkp%3ABlBMUJiYuvaNYw"
sale_item_name_regex = {"name" :"h1", "class_" : "_2qrJF"}
seller_description_regex = {"name": "div",  "class_" :  "_3cRjW"}
seller_block_regex = {"name": "div", "class_": "vim x-about-this-seller"}
seller_name_regex = {"name": "div", "id": "ds_div"}
seller_url_regex = {}
date_regex = {}
price_regex = {"name" :  "span", "data-hook" :  "formatted-primary-price"}
attributes_regex = {}

page_link = str(requests.get(page).text.encode('utf-8'))
soup = BeautifulSoup(page_link, 'html.parser', from_encoding='utf-8')
#print(soup.prettify())
item_name = soup.find(**seller_name_regex)

print(item_name)
#print(soup.find(**seller_name_regex))
