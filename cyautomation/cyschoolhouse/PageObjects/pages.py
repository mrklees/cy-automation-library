# -*- coding: utf-8 -*-
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import PageObjects.locators as loc
import PageObjects.elements as elem

class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""
    
    def __init__(self, driver):
        self.driver = driver
        
    def wait_for_page_to_load(self):
        WebDriverWait(self.driver, 10).until(EC.title_contains(self.title))
        
class OktaLoginPage(BasePage):
    """Actions for the Okta Login Page"""
    
    title = 'Sign In'
    #Declare variables corresponding to the username and password box elements
    username = elem.OktaUsernameElement()
    password = elem.OktaPasswordElement()
    
    def is_login_page(self):
        self.wait_for_page_to_load()
        return self.title in self.driver.title
    
    def click_login_button(self):
        element = self.driver.find_element(*loc.OktaLoginPageLocators.GO_BUTTON)
        element.click()

class OktaHomePage(BasePage):        
    """Actions for the Okta Homepage"""
    
    title = 'My Applications'
    
    def is_logged_in(self):
        self.wait_for_page_to_load()
        return 'My Applications' in self.driver.title