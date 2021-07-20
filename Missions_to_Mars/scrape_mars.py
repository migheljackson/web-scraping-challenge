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
    mars_image_url='https://marshemispheres.com'


    # initiating the webdriver. Parameter includes the path of the webdriver.
    driver = webdriver.Chrome('chromedriver.exe') 
    
    #Get newest article
    driver.get(news_url)
    
    time.sleep(5)
    
    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")


    articles=soup.find('div',class_='list_text')
    newest_date = articles.find('div',class_='list_date').text
    newest_title = articles.find('div',class_='content_title').text
    newest_blurb = articles.find('div',class_='article_teaser_body').text

    
    #Get featured space image
    driver.get(space_image_url)
    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")

    featured_image=soup.find('img',class_="headerimage fade-in").get('src')
    featured_image_url=f'{space_image_url}{featured_image}'


    #Get Mars facts
    mars_facts_scrape=pd.read_html(mars_url)
    mars_df=pd.DataFrame(mars_facts_scrape[1])
    mars_df=mars_df.rename(columns={0:"Stats",
                                    1:"Mars"})
    mars_df=mars_df.set_index('Stats')
    #Convert to html table string
    mars_html_table = mars_df.to_html().replace('\n', '')


    #Get Mars Hemisphere images
    link_text_list=['Cerberus','Schiaparelli','Syrtis','Valles']

    hemisphere_image_urls=[]

    for link in link_text_list:
        driver.get(mars_image_url)
        driver.find_element_by_partial_link_text(link).click()
        currenturl=driver.current_url
        driver.get(currenturl)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        hemi_image=soup.find('img',class_="wide-image").get('src')
        hemi_image_url=f'{mars_image_url}/{hemi_image}'
        hemi_title=soup.find('h2',class_="title").text
        hemi_dict={"title":hemi_title,"img_url":hemi_image_url}
        hemisphere_image_urls.append(hemi_dict)

    #Store data in a dictionary
    mars_scrape_data= {
        "newest_article_date":newest_date,
        "newest_article_title":newest_title,
        "newest_article_blurb":newest_blurb,
        "space_featured_img":featured_image_url,
        "mars_data_table":mars_html_table,
        "hemisphere_image_urls":hemisphere_image_urls
    }


    driver.quit()

    return mars_scrape_data

    

