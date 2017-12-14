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
    
class IndicatorAreaLocators(object):
    """The locators for the Indicator Area form"""
    ADD_BUTTON = (By.CSS_SELECTOR, '.drk_blue_btn')
    PAGE_TITLE = (By.CSS_SELECTOR, '#schoolforce-wrapper > h1:nth-child(2)')
    SCHOOL_SELECT = (By.ID, 'j_id0:j_id1:SchoolSelect')
    NAME_SEARCH = (By.CSS_SELECTOR, '#StudentsTable_filter > label:nth-child(1) > input:nth-child(1)')
    ATTENDANCE = (By.ID, 'j_id0:j_id1:j_id95:0')
    BEHAVIOR = (By.ID, 'j_id0:j_id1:j_id95:1')
    ELA = (By.ID, 'j_id0:j_id1:j_id95:2')
    MATH = (By.ID, 'j_id0:j_id1:j_id95:3')
    ADD_INDICATOR = (By.CSS_SELECTOR, '#content > center:nth-child(1) > input:nth-child(1)')
    SAVE = (By.CSS_SELECTOR, 'div.content:nth-child(3) > input:nth-child(1)')
    GRADE_SELECT = (By.ID, 'j_id0:j_id1:gradeList')                 