from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import urllib
import time
import requests
import os
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

print('''
          .___               ___ ._______  .______  .____/\              
          : __|     .___    |   |: .___  \ : __   \ :   /  \             
          | : |     :   | /\|   || :   |  ||  \____||.  ___/             
          |   |     |   |/  :   ||     :  ||   :  \ |     \              
          |   |     |   /       | \_. ___/ |   |___\|      \             
          |___|     |______/|___|   :/     |___|    |___\  /             
                            :       :                    \/              
                            :                                            
                                                                         
_____._.___.__  ._______.______  ._______     _____._._______  ._______  
\__ _:|:   |  \ : .____/: __   \ : .____/     \__ _:|: .___  \ : .___  \ 
  |  :||   :   || : _/\ |  \____|| : _/\        |  :|| :   |  || :   |  |
  |   ||   .   ||   /  \|   :  \ |   /  \       |   ||     :  ||     :  |
  |   ||___|   ||_.: __/|   |___\|_.: __/       |   | \_. ___/  \_. ___/ 
  |___|    |___|   :/   |___|       :/          |___|   :/        :/     
                                                        :         :      
                                                                                                                                                                                       
''')

s = Service("./chromedriver")
driver = webdriver.Chrome(service=s)
url = "https://twitter.com/search?q=new%20work%20badge&src=typed_query" #Add '&f=live' for streaming
driver.get(url)


# https://chromedriver.storage.googleapis.com/index.html?path=98.0.4758.102/

time.sleep(5)

imageLinkArrays = []

SCROLL_PAUSE_TIME = 3

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    images = driver.find_elements_by_tag_name('img')
    #images = driver.find_element(By.TAG_NAME, "img")
    try:

        for image in images:
            if (link := image.get_attribute("src")) is not  None and "https://pbs.twimg.com/media" in link: #make sure to install python3.8 to use the walrus
                imageLinkArrays.append(link)
    except StaleElementReferenceException as e:
        raise e

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    time.sleep(SCROLL_PAUSE_TIME)
    
    new_height = driver.execute_script("return document.body.scrollHeight")   
    if new_height == last_height:
        break
    last_height = new_height

uniqueSets = set(imageLinkArrays)

counter = 0
badges = "./badges/"
os.chdir(badges)
print(len(imageLinkArrays))
print(len(uniqueSets))
print("Getting new work badges")
for i in uniqueSets:
    urllib.request.urlretrieve(i, str(counter)+".jpg")
    counter = counter + 1

driver.close()
os.system("lsix")