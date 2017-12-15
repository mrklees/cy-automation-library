# -*- coding: utf-8 -*-

from selenium.webdriver.common.by import By

class MyDataLoginPageLocators(object):
    """A class for the locators in the Okta login page"""
    GO_BUTTON = (By.ID, 'idlogon')
    USERNAME = (By.ID, 'sawlogonuser')
    PASSWORD = (By.ID, 'sawlogonpwd')