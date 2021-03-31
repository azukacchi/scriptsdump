from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import time
import argparse

delay = 6

def main():
    
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    DRIVER_PATH = args.driver # path to chromedriver.exe
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.get("https://archiveofourown.org/users/login")


    USERNAME = args.uname # your ao3 username
    PASSWORD = args.pw # your ao3 password

    # driver.refresh()
    time.sleep(delay)
    check = driver.find_element_by_xpath("//input[@id='tos_agree']")
    check_visible = WebDriverWait(driver, 2).until(lambda driver : check.is_displayed())
    check.click()
    agree = driver.find_element_by_xpath("//button[@id='accept_tos']").click()
    time.sleep(delay)

    login = driver.find_element_by_xpath("//input[@id='user_login']").send_keys(USERNAME)
    password = driver.find_element_by_xpath("//input[@id='user_password']").send_keys(PASSWORD)
    submit = driver.find_element_by_xpath("//input[@value='Log in']").click()
    
    action = ActionChains(driver)
 
    firstLevelMenu = driver.find_element_by_xpath("//a[@class='dropdown-toggle']")
    action.move_to_element(firstLevelMenu).perform()
    
    secondLevelMenu = driver.find_element_by_xpath("//a[contains(text(),'My History')]")
    secondLevelMenu.click()
    
    totalwords = []
    totalfics = []
    while True:
        words, fics = countwords(driver)
        totalwords.append(words)
        totalfics.append(fics)
        next_page_btn = driver.find_elements_by_xpath("//a[@rel='next']")
        if len(next_page_btn) < 1:
            break
        else:
            time.sleep(delay)
            next_page_btn = driver.find_element_by_xpath("//a[@rel='next']")
            WebDriverWait(driver, 2).until(lambda driver : next_page_btn.is_displayed())
            next_page_btn.click()
    
    print(f'Based on your History, you have read total of {sum(totalfics)} fics and {sum(totalwords)} words.')
    
    return

def countwords(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    words = [int(word.get_text().replace(',', '')) for word in soup.findAll('dd',{'class':'words'})]
    return sum(words), len(words)

if __name__ == '__main__':
    my_parser = argparse.ArgumentParser()

    my_parser.add_argument('uname',
                           action='store',
                           help='AO3 username')
    my_parser.add_argument('pw',
                           action='store',
                           help='AO3 password')
    my_parser.add_argument('driver',
                           action='store',
                           help='path to Selenium driver')
    
    args = my_parser.parse_args()
    main()
