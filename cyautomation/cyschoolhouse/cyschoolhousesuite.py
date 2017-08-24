# -*- coding: utf-8 -*-
"""cyschoolhouse Suite
This suite is a set of helper functions which address the broader task of 
accessing data on cyschoolhouse. This will include navigation functions, logins,
and other common tasks we can antipicate needing to do for multiple products. 
"""

from pathlib import Path
import getpass
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
key_file_path = '/'.join([str(Path.home()), 'Desktop/keyfile.txt'])
gecko_path = '/'.join([str(Path.home()), 'GitHub/cy-automation-library/geckodriver/geckodriver.exe'])


def extract_key():
    """Extract SSO Information from keyfile
    
    One practice I use here is to store my SSO in a keyfile instead of either
    entering it in the cmd prompt on each run or hardcoding it in the program. 
    Keyfile should be formatted like so:
        'descript:cityyear sso/user:aperusse/pass:p@ssw0rd'
    Simply replace the username and password with your credentials and then save
    it as keyfile.txt
    """
    with open(key_file_path) as file:
        keys = file.read()
    split_line = keys.split("/")
    entries = [item.split(":")[1] for item in split_line]
    desc, user, pwd = entries
    return user, pwd

def request_key():
    print('Please enter your City Year Okta credential below.')
    print('It is used for sign in only and is not stored in any way after the script closes.')
    user = input('Username:')
    # If you run from the cmd prompt, it won't show your password.  It will in an interactive
    # console though, so keep that in mind. 
    pwd = getpass.getpass()
    return user, pwd

def get_driver():
    return Firefox(executable_path=gecko_path)

# Login to a form using the standard element names "username" and "password"
def standard_login(driver):
    # User preference on how login is collected. It's probably a little more secure
    # to enter the user/pass every time, however that will require that you be
    # there to initialize the script.  If you intend to run on a schedule then
    # be prepared to store your credentials in a file.  Ideally, we would have 
    # slightly better security around that filer.
    user, pwd = extract_key()
    #user, pwd = request_key()
    driver.find_element_by_name("username").send_keys(user)
    driver.find_element_by_name("password").send_keys(pwd + Keys.RETURN)
    return driver

# Script for logging into Salesforce via the front door.  Takes an active driver.
def open_okta(driver):
    # Open Okta login
    driver.get("https://cityyear.okta.com")
    # Input login
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
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

if __name__ == '__main__':
    driver = get_driver()
    driver = open_cyschoolhouse18_sb(driver)