# -*- coding: utf-8 -*-
'''
Selenium testing module. We're doing some important testing here on how 
to utilize selenium with requests.  The ultimate goal of this script will be
to prove that Selenium can meet 

'''
# Core python
import time
import csv
import os

# The local 
from seleniumsuite import *

from seleniumrequests import Firefox
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# downloads a file using a GET request.    
def download_testfile(driver):
    url = 'https://na30.salesforce.com/00O360000069dSu?export=1&enc=UTF-8&xf=csv'
    fileloc = "testfile.csv"
    response = driver.request('GET', url)
    decoded = response.content.decode('utf-8')
    cr = csv.reader(decoded.splitlines(), delimiter=',')
    my_list = list(cr)
    with open(fileloc, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=",", quotechar='"')
        for row in my_list:
            #print(row)
            writer.writerow(row)
    return driver

# runs the entire test script
def selenium_test_file_dl():
    driver = get_driver()
    driver = open_cyschoolhouse17(driver)
    driver = download_testfile(driver)
    driver.quit()
    
if __name__ == "__main__":
    selenium_test_file_dl()