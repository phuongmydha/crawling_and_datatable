from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

from time import sleep
import pickle
import requests
from bs4 import BeautifulSoup

# 0. Khai báo 
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # maximum cửa sổ khi bắt đầu chạy 
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
service = Service(executable_path='/Users/leduchau/Desktop/crawl/chromedriver-mac-arm64/chromedriver')
browser = webdriver.Chrome(service=service,options= chrome_options) # defind driver with options 

# 1. Open FB
browser.get('https://www.facebook.com')

# 2. Try to login
email_input = browser.find_element(By.ID, 'email') # tìm thẻ có id= email 
password_input = browser.find_element(By.ID, 'pass') # tìm thẻ có id= pass 
email_input.send_keys('youremail') # nhap email
password_input.send_keys('yourpassword') # nhap email

password_input.send_keys(Keys.ENTER) # nhap password 
sleep(5)

pickle.dump(browser.get_cookies(), open("my_cookie.pkl", "wb") )
sleep(10)