# -*- coding: utf-8 -*-
from collections import defaultdict
from pathlib import Path
from seleniumrequests import Firefox
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from time import sleep
import sys
from pandas import read_excel
from tqdm import tqdm

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
    key_dict = defaultdict(None)
    key_file_path = '/'.join([str(Path.home()), 'Desktop/keyfile.txt'])
    with open(key_file_path) as file:
        keys = file.read()
    split_keys = keys.split("\n")
    for keyline in split_keys:
        split_line = keyline.split("/")
        desc, user, pas = [item.split(":")[1] for item in split_line]
        key_dict[desc] = user, pas
    return key_dict

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

class MyDataLogin(BaseImplementation):
    
    user, pw = extract_key()['mydata sso']
    
    def set_up(self):
        """Navigate to City Year Okta login"""
        self.driver.get('http://getdata.lausd.net/')
        
    def enter_credentials(self):
        """Enter credentials for Okta Login"""
        login_page = page.MyDataLogin(self.driver)
        assert login_page.page_is_loaded()
        login_page.username = self.user
        login_page.password = self.pw
        sleep(2)
        login_page.click_login_button()
    
    def check_logged_in(self):
        """Confirm login"""
        homepage = page.MyDataLogin(self.driver)
        assert homepage.page_is_loaded()
        
    def login(self):
        """Runs all steps to login to Okta"""
        self.set_up()
        self.enter_credentials()           
        
class StudentRecord(MyDataLogin):
    
    students = read_excel('~/Desktop/EWI Model/ag progress.xlsx')['Student ID'].values
    record_stack = []
    
    def get_student_record(self, student_id):
        self.driver.get('https://getdata.lausd.net/xmlpserver/MyData/Student_History/STH1A-Demographics.xdo?_xmode=2&_xpt=2&_xf=pdf&_paramsstudent_did=' + str(student_id))
    
    def get_all_student_credits(self):
        self.login()
        for student_id in tqdm(self.students):
            self.get_student_record(student_id)
            StudentRecord = page.StudentRecord(self.driver)
            StudentRecord.wait_for_page_to_load()
            sleep(2)
            r, c, n = StudentRecord.extract_credit_info()
            self.record_stack.append([student_id, r, c, n])