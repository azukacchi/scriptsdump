import pandas as pd
import re
from bs4 import BeautifulSoup
import os.path
from datetime import datetime
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import argparse

def webdr():
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    DRIVER_PATH = args.driver
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.get("https://www.goodreads.com/")

    USERNAME = args.uname
    PASSWORD = args.pw
    
    # login 
    driver.find_element_by_xpath("//input[@type='email']").send_keys(USERNAME)
    # password 
    driver.find_element_by_xpath("//input[@type='password']").send_keys(PASSWORD)
    # submit
    driver.find_element_by_xpath("//input[@type='submit']").click()
    time.sleep(15)

    # booklist 
    driver.find_element_by_xpath("//a[text()='My Books']").click()
    time.sleep(15)
    # pagecount 
    driver.find_element_by_xpath("//select[@name='per_page']/option[text()='75']").click()
    return driver.page_source

def main(pagesrc):
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    soup = BeautifulSoup(pagesrc, features="html.parser") 

    judul = soup.findAll('td',{'class':'field title'})
    penulis = soup.findAll('td',{'class':'field author'})
    tanggal = soup.findAll('td',{'class':'field date_read'})

    title = []
    author = []
    date = []

    for baris in judul:
        title.append(baris.find('a').get_text().strip())
    for baris in penulis:
        full = re.split(',',baris.find('a').get_text().strip())
        try: fullname = full[1].strip()+' '+full[0]
        except: fullname = baris.find('a').get_text().strip()
        author.append(fullname)

    for baris in tanggal:
        date.append(baris.find('span').get_text())

    tabel = {'Title':title, 'Author':author, 'Status':'Finished', 'Progress':'', 'Book type':'', 'Highlight':'','Year':date}
    df = pd.DataFrame(tabel)
    date2 = []
    for row in df.Year:
        try: row = datetime.strptime(row, "%b %d, %Y").strftime('%m/%d/%y')
        except:
            try: row = datetime.strptime(row, "%b %Y").strftime('%m/01/%y')
            except: row = '0'
        date2.append(row)
    df['Year'] = date2
    
    filename = args.filename
    csv_path = os.path.join(BASE_DIR, filename)
    if os.path.exists(csv_path):
        os.remove(csv_path)
    df.to_csv(csv_path, index=False)
    
    print('fin')
    
    return
  

if __name__ == '__main__':
    my_parser = argparse.ArgumentParser()

    my_parser.add_argument('uname',
                           action='store',
                           help='Goodreads username')
    my_parser.add_argument('pw',
                           action='store',
                           help='Goodreads password')
    my_parser.add_argument('driver',
                           action='store',
                           help='path to Selenium driver')
    my_parser.add_argument('-filename',
                           action='store',
                            default='Goodreads.csv',
                           help='saved csv filename')
    args = my_parser.parse_args()
    
    page = webdr()
    main(page)
