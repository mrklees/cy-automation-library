# -*- coding: utf-8 -*-
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By

import PageObjects.locators as loc
import PageObjects.elements as elem

class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""
    
    def __init__(self, driver):
        self.driver = driver
        
    def wait_for_page_to_load(self):
        WebDriverWait(self.driver, 100).until(EC.title_contains(self.title))
      
    def page_is_loaded(self):
        self.wait_for_page_to_load()
        return self.title in self.driver.title
        
class OktaLoginPage(BasePage):
    """Actions for the Okta Login Page"""
    
    #title used to ensure the page has loaded before acting
    title = 'Sign In'
    #Declare variables corresponding to the username and password box elements
    username = elem.OktaUsernameElement()
    password = elem.OktaPasswordElement()
    
    def click_login_button(self):
        element = self.driver.find_element(*loc.OktaLoginPageLocators.GO_BUTTON)
        element.click()

class OktaHomePage(BasePage):        
    """Actions for the Okta Homepage"""
    
    #title used to ensure the page has loaded before acting
    title = 'My Applications'
    
    #Functions for launching various applications.  It's important that we 
    def launch_cyschoolhouse(self):
        self.driver.get("https://cityyear.okta.com/home/salesforce/0oao08nxmQCYJQHUHCBU/46?fromHome=true")
        
    def launch_cyschoolhouse_sandbox(self):
        self.driver.get("https://cityyear.okta.com/home/salesforce/0oa1dt5ae7mOkRt3O0h8/46?fromHome=true")
        
class CyshHomePage(BasePage):
    """Actions for the cyschoolhouse Home Page"""
    
    title = 'Salesforce - Unlimited Edition'
    search_bar = elem.CyshSearchElement()
    
    def set_search_filter(self, filter):
        """Changes to the filter type on the search function"""
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'sen')))
        filters = Select(self.driver.find_element(*loc.CyshHomePageLocators.SEARCH_FILTER))
        filters.select_by_visible_text(filter)
    
    def click_search_button(self):
        button = self.driver.find_element(*loc.CyshHomePageLocators.SEACH_BUTTON)
        button.click()
        
class CyshIndicatorAreas(BasePage):
    
    def nav_to_IA_enroller(self):
        self.driver.get("https://c.na24.visual.force.com/apex/IM_Indicator_Areas")