# -*- coding: utf-8 -*-
"""Selenium Suite

The purpose of this file is provide wrappers for many of the common tasks performed
with Selenium.  Increases the reusability of the code and lets me spread out some of
the code into different files.

This code was largely for testing purposes.   
"""

from seleniumrequests import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""Configuration Variables

The below variables are used to configure some machine specific details. Unfortunately
I don't know how we can avoid needing some of these variables for the potentially
arbitrary machine and file system we might get.  
"""
# Location of the file with my SSO username and password
key_file_path = 'C:/Users/aperusse/Desktop/keyfile.txt'

def extract_key():
    """Extract SSO Information from keyfile
    
    One practice I use here is to store my SSO in a keyfile instead of either
    entering it in the cmd prompt on each run or hardcoding it in the program. 
    """
    with open(key_file_path) as file:
        keys = file.read()
    split_line = keys.split("/")
    entries = [item.split(":")[1] for item in split_line]
    desc, user, pwd = entries
    return user, pwd

def get_driver():
    return Firefox()

# Login to a form using the standard element names "username" and "password"
def standard_login(driver):
    user, pwd = extract_key()
    driver.find_element_by_name("username").send_keys(user)
    driver.find_element_by_name("password").send_keys(pwd + Keys.RETURN)
    return driver

# Script for logging into Salesforce via the front door.  Takes an active driver.
def open_okta(driver):
    # Open Okta login
    driver.get("https://cityyear.okta.com")
    # Input login
    driver = standard_login(driver)
    # Wait for next page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "app-link")))
    # Check that we aren't in the login page anymore
    assert 'login' not in driver.current_url
    return driver

# opens cyschoolhouse assuming that we are at the okta login
def open_cyschoolhouse17(driver):
    driver.implicitly_wait(10)
    driver = open_okta(driver)
    driver.get("https://cityyear.okta.com/home/salesforce/0oa19u4wnhzgPqjtw0h8/46?fromHome=true")
    # Wait for next page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "tsidLabel")))
    assert 'salesforce' in driver.current_url
    return driver

def open_cyschoolhouse18_sb(driver):
    driver.implicitly_wait(10)
    driver = open_okta(driver)
    driver.get("https://cityyear.okta.com/home/salesforce/0oa1dt5ae7mOkRt3O0h8/46?fromHome=true")
    # Wait for next page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "tsidLabel")))
    assert 'salesforce' in driver.current_url
    return driver