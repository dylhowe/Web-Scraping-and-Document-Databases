
# coding: utf-8

# In[55]:


from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import pymongo
import time



# In[57]:

def scrape():
    
    executable_path = {'executable_path':'C:/Users/dhowe/GWDC201805DATA3-Class-Repository-DATA/Homework/11-Web-Scraping-and-Document-Databases (Week 13)/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #get Mars News article title and teaser
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    time.sleep(5)

    #find the title and teaser text for the first article
    article_title = soup.find('div', class_='content_title').text
    article_teaser = soup.find('div', class_='article_teaser_body').text


    # In[58]:


    #get url for fullsize featured image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #click to the featured image
    browser.click_link_by_partial_text('FULL IMAGE')

    #find html for image
    img_full_str = str(soup.find('article', class_='carousel_item')["style"])

    #slice string to get the url extension
    begin= img_full_str.find("/")
    end=img_full_str.find("');")
    img_url_ext = img_full_str[begin:end]

    #append url extension to base url
    img_url="https://www.jpl.nasa.gov" + img_url_ext


    # In[59]:


    #Get the most recent Mars weather update from twitter
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #find text from the most recent tweet
    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text


    # In[60]:


    #Get the table of Mars Facts
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #read the table to a dataframe, set index, and write to HTML
    facts_df = pd.read_html(url, encoding="utf-8-sig")[0].set_index(0)

    facts_html = facts_df.to_html()


    # In[61]:


    #Get Mars hemisphere titles and images
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #create list for dicts
    titles_urls = []

    #get titles and links
    titlereturn = soup.find_all('h3')

    for title in titlereturn:
        
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        #save title text
        titletext=title.text
        
        #click to full image
        browser.click_link_by_partial_text(titletext)
        
        #save full image URL
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        #append url extension to base url
        img_end=str(soup.find_all("img", class_="wide-image")[0]["src"])
        imgurl = "https://astrogeology.usgs.gov" + img_end
        
        #go back to homepage
        browser.click_link_by_partial_text("Back")
        
        #save title and url pair to list of dicts
        titles_urls.append({"title":titletext, "img_url":imgurl})

    output = {"article_title": article_title, 
              "article_teaser": article_teaser,
              "big_img_url": img_url, 
              "mars_weather": mars_weather, 
              "facts_html": facts_html, 
              "titles_urls": titles_urls}

    return(output)


    

