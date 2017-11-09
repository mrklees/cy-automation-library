# -*- coding: utf-8 -*-

from selenium.webdriver.common.by import By

class OktaLoginPageLocators(object):
    """A class for the locators in the Okta login page"""
    GO_BUTTON = (By.ID, 'okta-signin-submit')
    USERNAME = (By.ID, 'okta-signin-username')
    PASSWORD = (By.ID, 'okta-signin-password')
    
class CyshHomePageLocators(object):
    """The cyschoohouse homepage locators"""
    SEARCH_FILTER = (By.ID, 'sen')
    SEARCH_BOX = (By.ID, 'sbstr')
    SEACH_BUTTON = (By.NAME, "search")