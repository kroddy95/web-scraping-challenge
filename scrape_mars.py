# Scrape the data
from splinter import Browser
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape():
    # NASA Mars News
    nasa_url = 'https://mars.nasa.gov/news'

    response = requests.get(nasa_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_title = soup.find(class_='content_title').text.strip()
    news_p = soup.find(class_='rollover_description_inner').text.strip()

    # JPL Mars Featured Image
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless = True)

    browser.visit(jpl_url)
    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured_image_url = soup.find(class_='button fancybox')["data-fancybox-href"]

    browser.quit()

    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image_url

    # Mars Facts
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)

    facts_df = tables[0]

    facts_df.set_index(0, inplace=True)

    facts_df.to_html('mars_facts.html')

    # Mars Hemispheres
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless = True)

    browser.visit(hemisphere_url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all(class_='description')

    hemisphere_image_urls = []

    # For all the descriptions on the page, open another browser to get the full jpg link
    for result in results:
        link = 'https://astrogeology.usgs.gov' + result.find('a')['href']
        
        executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
        browser = Browser('chrome', **executable_path, headless = True)

        browser.visit(link)
        time.sleep(1)
        
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
    
        # Get the title
        title = soup.find(class_='title').text.strip()
        title = title.replace('Enhanced','')
        title = title.strip()
    
        # Get the image link
        img = soup.find(class_='downloads')
        img_url = img.find('a')['href']
        
        # Create the dictionary and append to the list
        dict = {'title':title, 'img_url':img_url}
        hemisphere_image_urls.append(dict)
        
        browser.quit()

    browser.quit()

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    return mars_data
