#!/bin/python

#Enter the URL you would like to scrape: https://example.com
#Enter the keyword you want to search for: privacy
#Enter the crawling depth (e.g., 2): 2

#Starting crawl...

#Keyword 'privacy' found at: https://example.com/privacy-policy
#Keyword in URL: https://example.com/privacy-policy
#Found URL: https://example.com/terms
#Found URL: https://example.com/contact

# Helps in printing my the banner
def banner():
    print('''
 	        ######### #    ##########         ########   #  ####  ######    ####     ######  ######## ######
       		###	    #  #                 #          #         #     #  #    #    #     # #        #     #
		###          # ##########   ###   #######  #          # ####  ########   ######  ######## # ####
		###         #  #            ###          #  #         # #    #        #  #       #        #  #
		######### #    ##########         #######    #  ####  #   # #          # #       ######## #    #
                                 
                                                          DE.SCRAPER

                                               Author: Victor (@Oluwa_data)\n''')


banner()

import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from termcolor import colored

# 
visited_urls = set()

def spider_urls(url, keyword, depth=2, current_depth=0):
    if current_depth > depth or url in visited_urls:
        return
    
    visited_urls.add(url)
   
    # Handle HTTP errors    
    try:
        response = requests.get(url)
        response.raise_for_status()

    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return

    except KeyboardInterrupt:
        print(colored("keyboard has interrupted", "blue"))
        sys.exit() 

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Check keyword in page content
        if keyword.lower() in soup.get_text().lower():
            print(f"Keyword '{keyword}' found at: {url}")
        
        # Extract and process links
        found_urls = set()
        for tag in soup.find_all("a", href=True):
            href = tag.get("href")
            full_url = urljoin(url, href)
            # Normalize and filter URLs
            if full_url.startswith("http") and full_url not in visited_urls:
                if keyword.lower() in full_url.lower():
                    print(f"Keyword in URL: {full_url}")
                found_urls.add(full_url)
        
        # Recursively crawl found URLs with depth control
        for next_url in found_urls:
            spider_urls(next_url, keyword, depth, current_depth + 1)

# Input from user
url = input(colored("Enter the URL you would like to scrape: ", "blue")).strip()
keyword = input(colored("Enter the keyword you want to search for: ", "blue")).strip()
depth = int(input(colored("Enter the crawling depth (e.g., 2): ", "blue")).strip())

# Start crawling
print(colored("\nStarting crawl...\n", "green"))
spider_urls(url, keyword, depth)

