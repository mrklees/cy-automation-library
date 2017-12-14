# -*- coding: utf-8 -*-
from selenium.webdriver.support.ui import WebDriverWait
import PageObjects.locators as loc

class BasePageElement(object):
    """Base page class that is initialized on every page object class."""
    
    def __set__(self, obj, value):
        """Sets the text to the value supplied"""
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(*self.locator))
        driver.find_element(*self.locator).send_keys(value)
        
    def __get__(self, obj, owner):
        """Gets the text of the specified object"""
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(*self.locator))
        element = driver.find_element(*self.locator)
        return element.get_attribute('value')
    
class OktaUsernameElement(BasePageElement):
    """This class contains the locator for the username box"""
    locator = loc.OktaLoginPageLocators.USERNAME
    
class OktaPasswordElement(BasePageElement):
    """This class contains the locator for the username box"""
    locator = loc.OktaLoginPageLocators.PASSWORD
    
class CyshSearchElement(BasePageElement):
    locator = loc.CyshHomePageLocators.SEARCH_BOX
    
class IaNameSearch(BasePageElement):
    locator = loc.IndicatorAreaLocators.NAME_SEARCH