# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 07:47:08 2018

@author: aptus
"""

import os
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from time import sleep
from dateutil.parser import parse
import string
import traceback
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
location_address = 'Kongens gate 2 Trondheim, 7011 Norge'
driver = webdriver.Chrome(dir_path+'/chromedriver.exe')
driver.get('https://www.latlong.net/')
inputEle = driver.find_element_by_css_selector('body > main > div:nth-child(3) > div.col-7.graybox > form > input')
inputEle.send_keys(location_address)
driver.find_element_by_css_selector('body > main > div:nth-child(3) > div.col-7.graybox > form > button').click()

try:
    WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                   'Timed out waiting for PA creation ' +
                                   'confirmation popup to appear.')

    alert = driver.switch_to.alert
    print(alert.accept())
    print("alert accepted")
    driver.close()
except TimeoutException:
    print("no alert")
    lat=driver.find_element_by_css_selector('body > main > div:nth-child(3) > div.col-7.graybox > div > div > input').get_attribute('value')
    lng=driver.find_element_by_css_selector('body > main > div:nth-child(3) > div.col-7.graybox > div > div:nth-child(2) > input').get_attribute('value')
    print(lat)
    print(lng)
