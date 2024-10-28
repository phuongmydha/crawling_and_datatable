from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import csv
import re
import random
import pickle
from time import sleep

# 0. Define Browser
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
service = Service(executable_path='/Users/leduchau/Desktop/crawl/chromedriver-mac-arm64/chromedriver')
browser = webdriver.Chrome(service=service, options=chrome_options)

# 1. Open FB
browser.get('https://www.facebook.com')
sleep(random.randint(3, 5))

# 2. Load cookies from file
cookies = pickle.load(open("my_cookie.pkl", "rb"))
for cookie in cookies:
    browser.add_cookie(cookie)

sleep(random.randint(4, 6))

# 3. Refresh the browser 
browser.get('https://www.facebook.com')
sleep(random.randint(3, 5))

# 4. Crawl review

# Function to search posts related to BOSCH
def search_bosch_posts(browser):
    search_url = "https://www.facebook.com/search/posts?q=review%20bosch&filters=eyJycF9hdXRob3I6MCI6IntcIm5hbWVcIjpcIm1lcmdlZF9wdWJsaWNfcG9zdHNcIixcImFyZ3NcIjpcIlwifSJ9"
    browser.get(search_url)
    sleep(random.randint(3, 5))

    # Load existing links from the CSV file into a set
    existing_links = set()
    try:
        with open('post_links_new.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            existing_links = {row[0] for row in reader}
    except FileNotFoundError:
        pass  # If the file doesn't exist, we start with an empty set

    with open('bosch_review_link.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Scroll to load more posts
        for _ in range(100):  # Adjust for more results if needed
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            feed = soup.find('div', attrs={'role': 'feed'})
            if feed:
                posts = feed.find_all('div', attrs={'data-virtualized': 'false'})
                for post in posts:
                    post_link = post.find('a', href=True)
                    if post_link:
                        link = post_link['href']
                        post_match = re.search(r"multi_permalinks=(\d+)", link)
                        group_match = re.search(r"groups/(\d+)", link)
                        if post_match:
                            post_id = post_match.group(1)
                            group_id = group_match.group(1)
                            full_post_link = f"https://www.facebook.com/groups/{group_id}/posts/{post_id}"
                            if full_post_link not in existing_links:
                                writer.writerow([full_post_link])
                                existing_links.add(full_post_link)
                                print(f"Link crawl: {full_post_link}")
                        else:
                            if link not in existing_links:
                                writer.writerow([link])
                                existing_links.add(link)
                                print(f"Link crawl: {link}")

            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(random.randint(1, 4))
        print("Crawl data post link successfully")

bosch_post_links = search_bosch_posts(browser)

# Close Browser
browser.close()