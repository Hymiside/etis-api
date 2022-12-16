import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# import pandas as pd
import time
# from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

option = Options()
# option.add_argument('--headless')
browser = webdriver.Chrome(options=option)


def login_etis(email: str, password: str):
    browser.get('https://student.psu.ru/pls/stu_cus_et/stu.timetable')

    login = browser.find_element(By.ID, 'login')
    login.send_keys(email + Keys.RETURN)

    password1 = browser.find_element(By.ID, 'password')
    password1.send_keys(password + Keys.RETURN)

    share = browser.find_element(By.ID, 'sbmt')
    share.click()

    time.sleep(5)

    c = browser.get_cookie('session_id')
    browser.add_cookie({'domain': 'student.psu.ru', 'name': 'session_id', 'value': c['value'], 'sameSite': 'Strict'})

    browser.get('https://student.psu.ru/pls/stu_cus_et/stu.timetable')

    time.sleep(5)
    browser.get('https://student.psu.ru/pls/stu_cus_et/stu.teachplan')

    time.sleep(50)
