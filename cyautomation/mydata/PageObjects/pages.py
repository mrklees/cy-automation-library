# -*- coding: utf-8 -*-
from time import sleep

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
 
class MyDataLogin(BasePage):
    #title used to ensure the page has loaded before acting
    title = 'Oracle Business Intelligence Sign In'
    #Declare variables corresponding to the username and password box elements
    username = elem.MyDataUsernameElement()
    password = elem.MyDataPasswordElement()
    
    def click_login_button(self):
        element = self.driver.find_element(*loc.MyDataLoginPageLocators.GO_BUTTON)
        element.click()
        
class MyDataHome(BasePage):
    
    title = 'Oracle BI Interactive Dashboards - LAUSD Enterprise Reporting System'

class StudentRecord(BasePage):
    
    title = 'STH1A-Demographics - Oracle BI Publisher'
    
    def extract_credit_info(self):
        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe")))
        #self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        reqd = self.driver.find_element_by_css_selector('.textLayer > div:nth-child(175)').text
        cpltd = self.driver.find_element_by_css_selector('.textLayer > div:nth-child(176)').text
        ndd = self.driver.find_element_by_css_selector('.textLayer > div:nth-child(179)').text
        self.driver.switch_to_default_content()
        return reqd, cpltd, ndd