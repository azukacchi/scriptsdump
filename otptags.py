import re
from bs4 import BeautifulSoup
import os.path
from datetime import date
import requests
import csv
import time

delay = 6
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
filename = 'ao3tags.csv'
filepath = os.path.join(BASE_DIR, filename)

def tagcount():
    
    urls = [] # list of link to your otp tags

    today = date.today()
    counts = [today]
    for url in urls:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        # works count for a tag
        heading = soup.find('h2',{'class':'heading'}).get_text()
        regex1 = r'(?=(\d+) Works)'
        count = int(re.findall(regex1, heading)[0]) 
        counts.append(count)
        
        # number of works with a certain age rating ranging from
        # Teen and up, General, Not rated, Mature, Explicit
        regex2 = r'(?=\((\d+)\))'
        rating = soup.find('dd',{'id':'include_rating_tags'}).get_text()
        ratings = re.findall(regex2, rating)
        counts.append(', '.join(ratings))
        
        time.sleep(delay)

    data = [counts]

    with open(filepath, 'a') as csvfile:   
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(data)

if __name__ == '__main__':
    tagcount()
