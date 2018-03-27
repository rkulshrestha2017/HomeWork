
# coding: utf-8

# ## Mission to Mars

# In[1]:


from bs4 import BeautifulSoup
import pymongo
from splinter import Browser
import requests
import time
import pandas as pd

def scrape():

    # ## NASA Mars News

    # In[2]:


    #set up splinter browser

    executable_path = {'executable_path': 'driver/chromedriver'}
    browser = Browser('chrome', **executable_path, headless = False)

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    #pull html text and parse
    html_code = browser.html
    soup = BeautifulSoup(html_code, "html.parser")

    #grab needed info
    news_title = soup.find('div', class_="bottom_gradient").text
    news_p = soup.find('div', class_="rollover_description_inner").text

    time.sleep(30)
    # # Latest Featured Image

        # Featured Image URL & visit
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

        #navigate to link
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(30)

    browser.click_link_by_partial_text('more info')

    #get html code once at page
    image_html = browser.html

    #parse
    soup = BeautifulSoup(image_html, "html.parser")

    #find path and make full path
    image_path = soup.find('figure', class_='lede').a['href']
    featured_image_url = "https://www.jpl.nasa.gov/" + image_path


    # ## Mars Weather

    # In[5]:


    marsweather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(marsweather_url)

    weather_html = browser.html

    soup = BeautifulSoup(weather_html, 'html.parser')

    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text


    # ## Mars Facts

    # In[6]:


    #mars facts url and splinter visit
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)

    #get html
    facts_html = browser.html

    soup = BeautifulSoup(facts_html, 'html.parser')
    #soup


    # In[7]:


    #get the entire table
    table_data = soup.find('table', class_="tablepress tablepress-id-mars")


    # In[8]:


    #find all instances of table row
    table_all = table_data.find_all('tr')

    #set up lists to hold td elements which alternate between label and value
    labels = []
    values = []

    #for each tr element append the first td element to labels and the second to values
    for tr in table_all:
        td_elements = tr.find_all('td')
        labels.append(td_elements[0].text)
        values.append(td_elements[1].text)


    # In[9]:


    #make a data frame and view
    mars_facts_df = pd.DataFrame({
        "Label": labels,
        "Values": values
    })


    # In[10]:


    mars_facts_df


    # In[11]:


    # get html code for DataFrame
    fact_table = mars_facts_df.to_html(header = False, index = False)
    fact_table


    # ## Mars Hemispheres

    # In[12]:


    # new url
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(usgs_url)

    usgs_html = browser.html

    soup = BeautifulSoup(usgs_html, "html.parser")

    # gets class holding hemisphere picture
    items = soup.find("div",{"class":"collapsible results"}).find_all("div",{"class":"item"})

    #setup list to hold dictionaries
    hemisphere_image_urls =[]

    for item in items:
        img_main_url = "https://astrogeology.usgs.gov"+item.find("a")["href"]
        img_title = item.find("div",{"class":"description"}).find("a").find("h3").text
        browser.visit(img_main_url)
        time.sleep(2)
        img_soup = BeautifulSoup(browser.html,"html.parser")
        download_item = img_soup.find("div",{"class":"downloads"})
        hemisphere_item = {
        "title":img_title,
        "img_url": download_item.find("li").find("a")["href"]
        }
        hemisphere_image_urls.append(hemisphere_item)

    #print(hemisphere_image_urls)
            
    mars_dict = {
            "id": 1,
            "news_title": news_title,
            "news_p": news_p,
            "featured_image_url": featured_image_url,
            "mars_weather": mars_weather,
            "fact_table": fact_table,
            "hemisphere_images": hemisphere_image_urls
        }
    return mars_dict

scrape()
