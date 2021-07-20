# Dependencies
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pymongo
import pandas as pd


def scrape():
    # URL of pages to be scraped
    news_url = 'https://redplanetscience.com/'
    space_image_url= 'https://spaceimages-mars.com/'
    mars_url='https://galaxyfacts-mars.com/'


    # initiating the webdriver. Parameter includes the path of the webdriver.
    driver = webdriver.Chrome('chromedriver.exe') 
    driver.get(news_url)

    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")

    #Get newest article
    articles=soup.find('div'),class_="list_text")
    newest_date = articles.find('div',class_='list_date')
    newest_title = articles.find('div',class_='list_date')
    newest_blurb = articles.find('div',class_='list_date')