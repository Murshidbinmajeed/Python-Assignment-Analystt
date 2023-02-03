import json
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests
import numpy as np

def get_p_name(soup):

    try:
        title = soup.find("span", attrs={"id":"productTitle"})
        title_value = title.text
        title_str = title_value.strip()
    except AttributeError:
        title_str=""
    return title_str
def get_price(soup):
    try:
        price=soup.find("span",attrs={'class':'a-price-whole'}).string.strip()
    except AttributeError:
        price=""
    return price

def get_rating(soup):
    try:
        rating=soup.find('span',attrs={'class':'a-icon-alt'}).text.strip()
    except AttributeError:
        rating=""
    return rating
def get_no_ofrating(soup):
    try:
        Rcount=soup.find('span',attrs={'id':'acrCustomerReviewText'}).text.strip()
    except AttributeError:
        Rcount=""
    return Rcount
def get_prod_desc(soup):
    try:
        description = soup.find('div', attrs={'id': 'feature-bullets'}).text.strip()
    except AttributeError:
        description = ""
    return description
def get_ASIN(soup):
    try:
        asin = soup.find(id='detailBulletsWrapper_feature_div').text.strip()
    except AttributeError:
        asin=""
    return asin
def get_manufacture(soup):
    try:
        manf = soup.find(id='detailBulletsWrapper_feature_div').text.strip()
    except AttributeError:
        manf = ""
    return manf


if __name__ == '__main__':
    for i in range(0,20):
        URL = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"
        URL = URL+str(i)
        HEADER = ({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
        webpage = requests.get(URL, headers=HEADER)
        soup = BeautifulSoup(webpage.content, "html.parser")

        links = soup.find_all("a", attrs={
            'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
        list_of_links = []
        for link in links:
            list_of_links.append(link.get('href'))

        data = {"P_url": [], "P_name": [], "P_price": [], "P_rating": [], "P_noOfrating": [],'P_decs':[],'ASIN':[],'Manufturer':[]}

        for link in list_of_links:
            new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADER)
            new_soup = BeautifulSoup(new_webpage.content, 'html.parser')

            data['P_url'].append(new_webpage)
            data['P_name'].append(get_p_name(new_soup))
            data['P_price'].append(get_price(new_soup))
            data['P_rating'].append(get_rating(new_soup))
            data['P_noOfrating'].append(get_no_ofrating(new_soup))
            data['P_decs'].append(get_prod_desc(new_soup))
            data['ASIN'].append(get_ASIN(new_soup))
            data['Manufturer'].append(get_manufacture(new_soup))

amz_df=pd.DataFrame.from_dict(data)
amz_df['P_name'].replace('',np.nan,inplace=True)
amz_df=amz_df.dropna(subset=['P_name'])
amz_df.to_csv("pythonassignment.csv",header=True,index=False)


