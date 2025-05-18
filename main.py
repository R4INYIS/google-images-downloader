# -----------------------------------------------------------------------------
# Script to automatically download images from Ecosia based on parameters
# defined in the webs.csv file.
#
# webs.csv structure (semicolon separated):
# Google Search;Number of Images;Image to start;Folder Name;Quality
# - Google Search: Search term (e.g., "Coches")
# - Number of Images: Number of images to download (e.g., 10)
# - Image to start: Index of the image to start from (e.g., 1)
# - Folder Name: Name of the folder to save the images (e.g., 2)
# - Quality: Minimum image quality (1 = 800px, 2 = 1000px, 3 = 1280px)
#
# The script creates a folder for each search, downloads images filtered by
# minimum resolution, and logs any errors or warnings.
# -----------------------------------------------------------------------------

from bs4 import BeautifulSoup
import csv
import os
import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import re
import random
import math

# List to store search parameters read from webs.csv
webs = []
# List to log errors or warnings during execution
log = []
# Default minimum resolution (will be set per search)
dim = 1280

# Selenium Chrome options configuration
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--ignore-certificate-errors-spki-list')
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument('--ignore-ssl-errors')
patron = re.compile(r'\..{2,3}g/')

# Path to ChromeDriver executable
driver_path = Service("C:\chromedriver-win64\chromedriver.exe")

# Read search parameters from webs.csv
with open(f"webs.csv", 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=";")
    for row in reader:
        webs.append([row[0], row[1], row[2], row[3], row[4]])
    # Skip header
    webs = webs[1:]

# Iterate over each search defined in webs.csv
for info in range(len(webs)):
    try:
        # Create folder for images (if it doesn't exist)
        os.mkdir(f'./{webs[info][3]}')
    except:
        pass
    # Start Chrome browser with Selenium
    driver = webdriver.Chrome(service=driver_path, options=chrome_options)
    # Perform image search on Ecosia
    driver.get(f"https://www.ecosia.org/images?q={webs[info][0]}")
    driver.maximize_window()
    sleep(2)
    # Calculate how many scrolls are needed to load enough images
    ndown = int(webs[info][1])+int(webs[info][2])
    if ndown <= 20:
        ndown = ndown + 30
    for i in range(ndown):
        driver.execute_script(f"window.scrollBy(0, 100);")
        sleep(.05)
    sleep(.5)
    # Get the HTML of the image results page
    source = driver.page_source
    driver.quit()
    
    # Set minimum resolution based on Quality field
    if webs[info][4] == '1':
        dim = 800
    elif webs[info][4] == '2':
        dim = 1000
    elif webs[info][4] == '3':
        dim = 1280
        
    if True:
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(source, 'lxml')
        divs = soup.find_all('article')
        # Start index for images (Image to start)
        n = int(webs[info][2])
        print(dim)
        # Download images until reaching the requested number (Number of Images)
        while len(os.listdir(f'./{webs[info][3]}')) < int(webs[info][1]):
            try:
                a = divs[n].find('a')
            except:
                # If not enough images with the required resolution, lower the minimum resolution
                n = 1
                dim -= 200
                if dim < 800:
                    log.append(f'Problem in search {webs[info][0]}: not enough images with the required resolution')
                a = divs[n].find('a')
                
            # Get image resolution
            div = divs[n].find('div', class_="image-result__dimensions")
            result = int(div.get_text().split('×')[0])
            
            # Filter by minimum resolution
            if result >= dim:
                link = a['href']
                if '?' in link:
                    link = link.split('?')[0]
                print(link)
                try:
                    img = requests.get(link)
                except:
                    log.append('error')
                
                if img.status_code == 200:
                    name = link.split("/")
                    name = name[-1].strip()
                    try:
                        if name[-1] != 'g' and name[-1] != 'p':
                            name = f'{i}.jpg'
                    except:
                        pass
                    try:
                        if '.' in name:
                            open(f'./{webs[info][3]}/{name}','wb').write(img.content)
                    except:
                        pass
            
            n += 1
    # Wait before the next search
    sleep(20)
    # Log if not all requested images were downloaded
    if len(os.listdir(f'./{webs[info][3]}')) != int(webs[info][1]):
        log.append(f'Search for {webs[info][0]} failed, downloaded {len(os.listdir(f"./{webs[info][3]}"))} images out of {webs[info][1]}')
        
# Print log of errors or warnings
print(log)