# -*- coding: utf-8 -*-

from pathlib import Path
from seleniumrequests import Firefox

import PageObjects.pages as page

def extract_key():
    """Extract SSO Information from keyfile
    
    One practice I use here is to store my SSO in a keyfile instead of either
    entering it in the cmd prompt on each run or hardcoding it in the program. 
    Keyfile should be formatted like so:
        'descript:cityyear sso/user:aperusse/pass:p@ssw0rd'
    Simply replace the username and password with your credentials and then save
    it as keyfile.txt
    """
    key_file_path = '/'.join([str(Path.home()), 'Desktop/keyfile.txt'])
    with open(key_file_path) as file:
        keys = file.read()
    split_line = keys.split("/")
    entries = [item.split(":")[1] for item in split_line]
    desc, user, pwd = entries
    return user, pwd

class BaseImplementation(object):
    """Base Implementation object
    
    It's an important feature of every implementation that it either take an 
    existing driver or be capable of starting one
    """
    def __init__(self, driver=None):
        if driver == None:
            self.driver = Firefox()
        else:
            self.driver = driver

class OktaLogin(BaseImplementation):
    """Implementation script for logging into Okta."""
    
    user, pwd = extract_key()
    
    def set_up(self):
        self.driver.get("https://cityyear.okta.com")
        
    def enter_credentials(self, username, password):
        login_page = page.OktaLoginPage(self.driver)
        assert login_page.page_is_loaded()
        login_page.username = username
        login_page.password = password
        login_page.click_login_button()
    
    def check_logged_in(self):
        homepage = page.OktaHomePage(self.driver)
        assert homepage.page_is_loaded()
        
    def login(self):
        """Runs all steps to login to Okta"""
        self.set_up()
        self.enter_credentials(self.user, self.pwd)
        self.check_logged_in()
    
class SectionEnrollment(OktaLogin):
    """Implementation script for Section Enrollment"""
    from pandas import read_excel
    
    data = read_excel('input_files/student-enrollment-records.xlsx')
    
    def launch_cyschoolhouse(self):
        # Login via okta
        self.login()
        # Nav from Okta home to cyschoolhouse
        Okta = page.OktaHomePage(self.driver)
        assert Okta.page_is_loaded()
        Okta.launch_cyschoolhouse()
        
    def search_for_a_section(self, section):
        cysh_home = page.CyshHomePage(self.driver)
        assert cysh_home.page_is_loaded()
        cysh_home.set_search_filter("Sections")
        cysh_home.search_bar = section
        cysh_home.click_search_button()