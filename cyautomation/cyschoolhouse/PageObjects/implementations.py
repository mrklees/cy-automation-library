# -*- coding: utf-8 -*-

from pathlib import Path
from seleniumrequests import Firefox
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from time import sleep
import sys

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


class Okta(BaseImplementation):
    """Object for handingling Okta
    
    Wraps all processes for logging into Okta and navigation.
    """
    
    user, pwd = extract_key()
    
    def set_up(self):
        """Navigate to City Year Okta login"""
        self.driver.get("https://cityyear.okta.com")
        
    def enter_credentials(self, username, password):
        """Enter credentials for Okta Login"""
        login_page = page.OktaLoginPage(self.driver)
        assert login_page.page_is_loaded()
        login_page.username = username
        login_page.password = password
        login_page.click_login_button()
    
    def check_logged_in(self):
        """Confirm login"""
        homepage = page.OktaHomePage(self.driver)
        assert homepage.page_is_loaded()
        
    def login(self):
        """Runs all steps to login to Okta"""
        self.set_up()
        self.enter_credentials(self.user, self.pwd)
        self.check_logged_in()
        
    def launch_cyschoolhouse(self):
        """Script for logging into Okta and cyschoolhouse"""
        # Login via okta
        self.login()
        # Nav from Okta home to cyschoolhouse
        Okta = page.OktaHomePage(self.driver)
        assert Okta.page_is_loaded()
        Okta.launch_cyschoolhouse()

class SectionEnrollment(Okta):
    """Implementation script for Section Enrollment"""
    from pandas import read_excel
    
    data = read_excel('input_files/student-enrollment-records.xlsx')
    
    def search_for_a_section(self, section):
        """Should only be used from the cyschoohouse homepage"""
        cysh_home = page.CyshHomePage(self.driver)
        assert cysh_home.page_is_loaded()
        cysh_home.set_search_filter("Sections")
        cysh_home.search_bar = section
        cysh_home.click_search_button()
        
class IndicatorAreaEnrollment(Okta):
    """Implementation object for Indicator Area Enrollment"""
    from pandas import read_excel
    
    data = read_excel
    ut_files/indiactor_area_roster.xlsx')
    student_list = data['Student: Student ID'].unique()
    
    def nav_to_form(self):
        """Initial setup script for IA enrollment.
        
        Goes through login for Okta as well as navigating to the form and 
        ensuring the page is loaded appropriately
        """
        self.launch_cyschoolhouse()
        cysh_home = page.CyshHomePage(self.driver)
        assert cysh_home.page_is_loaded()
        
        self.driver.get("https://c.na24.visual.force.com/apex/IM_Indicator_Areas")
        ia_form = page.CyshIndicatorAreas(self.driver)
        ia_form.wait_for_page_to_load()
    
    def get_student_details(self, student_id):
        """Returns a students details including school, grade, name, and ia list given their id"""
        student_records = self.data[self.data['Student: Student ID'] == student_id]
        school = student_records.School.unique()[0]
        grade = student_records['Student: Grade'].unique()[0]
        name = student_records['Student: Student Last Name'].unique()[0]
        ia_list = student_records['Indicator Area'].values
        return school, grade, name, ia_list
    
    def enroll_student(self, student_id):
        """Handles the enrollment process of all IAs for a single student"""
        ia_form = page.CyshIndicatorAreas(self.driver)
        ia_form.wait_for_page_to_load()
        school, grade, name, ia_list = self.get_student_details(student_id)
        ia_form.select_school(school)
        sleep(1)
        ia_form.select_grade(str(grade))
        sleep(1)
        for ia in ia_list:
            ia_form.name_search = name
            sleep(3)
            self.assign_ias(student_id, ia)
            sleep(2)
        ia_form.save()
    
    def assign_ias(self, student_id, ia):
        """Assign an IA for a single student and indicator"""
        ia_form = page.CyshIndicatorAreas(self.driver)
        ia_form.wait_for_page_to_load()
        ia_form.select_student(student_id)
        sleep(3)
        ia_form.assign_indicator_area(ia)
        
    def enroll_all_students(self):
        """Executes the full IA enrollment"""
        self.nav_to_form()
        self.error_count = 0
        for student_id in self.student_list:
            if self.error_count == 5:
                self.error_count = 0
                self.driver.quit()
                self.driver = Firefox()
                self.nav_to_form()
                
            try:
                self.enroll_student(student_id)
            except TimeoutException:
                print("Timeout Failure on student: {}".format(student_id))
                self.error_count += 1
                
            except StaleElementReferenceException:
                print("Stale Element failure on student: {}".format(student_id))
                self.error_count += 1
                
            except:
                print("Caught a {} error on student: {}".format(sys.exc_info(), student_id))
                self.error_count += 1