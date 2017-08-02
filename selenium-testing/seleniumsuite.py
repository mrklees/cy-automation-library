# -*- coding: utf-8 -*-
import time
import csv
import os
from contextlib import closing

from seleniumrequests import Firefox
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Extract my username and password from a local file.  Makes sure I don't upload
# the username and password to GitHub. 
def extract_key():
    with open('C:/Users/perus/Desktop/keyfile.txt') as file:
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