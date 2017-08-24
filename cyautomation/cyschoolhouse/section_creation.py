# -*- coding: utf-8 -*-
"""Automated Section Creation
Script for the automatic creation of sections in cyschoolhouse. Please ensure
you have all dependencies, and have set up the input file called "section-creator-input.csv"
in the input files folder.
"""
import csv
from cyschoolhousesuite import *
from selenium.webdriver.support.ui import Select
from time import sleep

# This is a key for some encoding that I do in the input form.  In the 'section'
# columns of the input form, use the key from this dictionary to correspond 
# to the particular section type you would like to create. 
section_info = {
        'Attendance':{'name':'Coaching: Attendance', 'nickname':'Attendance'},
        'Greatness':{'name':'50 Acts of Greatness', 'nickname':'Behavior'},
        'Leadership':{'name':'50 Acts of Leadership', 'nickname': 'Behavior'},
        'Math':{'name':'Tutoring: Math', 'nickname':'Math'},
        'ELA':{'name':'Tutoring: Literacy', 'nickname':'ELA'},
        'ELT':{'name':'Enrichment', 'nickname': 'ELT'}
    }

def import_parameters():
    """Imports input data from csv
    
    
    """
    with open('input_files/section-creator-input.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
        lst = list(reader)
    return lst

def nav_to_section_creation_form(driver):
    driver.get('https://cs17.salesforce.com/a1A/o')
    driver.find_element_by_name("new").click()
    sleep(2)

def input_staff_name(driver, staff_name):
    dropdown = Select(driver.find_element_by_id("j_id0:j_id1:staffID"))
    dropdown.select_by_visible_text(staff_name)

def fill_static_elements(driver):
    driver.find_element_by_id("j_id0:j_id1:startDateID").send_keys("08/14/2017")
    driver.find_element_by_id("j_id0:j_id1:endDateID").send_keys("06/15/2018")
    driver.find_element_by_id("j_id0:j_id1:freqID:1").click()
    driver.find_element_by_id("j_id0:j_id1:freqID:2").click()
    driver.find_element_by_id("j_id0:j_id1:freqID:3").click()
    driver.find_element_by_id("j_id0:j_id1:freqID:4").click()
    driver.find_element_by_id("j_id0:j_id1:freqID:5").click()
    dropdown = Select(driver.find_element_by_id("j_id0:j_id1:inAfterID"))
    dropdown.select_by_visible_text("In School")
    driver.find_element_by_id("j_id0:j_id1:totalDosageID").send_keys("900")
    sleep(2)

def select_subject(driver, section):
    section_name = section_info[section]['name']
    print(section_name)
    driver.find_element_by_xpath("//label[contains(text(), '"+ section_name +"')]").click()
    driver.find_element_by_xpath("//input[@value='Proceed']").click()

def save_section(driver):
    driver.find_element_by_css_selector('input.black_btn:nth-child(2)').click()
    sleep(2)

def update_nickname(driver, section):
    nickname = section_info[section]['nickname']
    driver.find_element_by_css_selector('#topButtonRow > input:nth-child(3)').click()
    sleep(2)
    driver.find_element_by_id("00N1a000006Syte").send_keys(nickname)
    driver.find_element_by_xpath("//input[@value=' Save ']").click()
    sleep(2)

def create_single_section(driver, parameter):
    nav_to_section_creation_form(driver)
    select_subject(driver, parameter['Section'])
    input_staff_name(driver, parameter['ACM'])
    fill_static_elements(driver)
    save_section(driver)
    update_nickname(driver, parameter['Section'])
        
# runs the entire test script
def selenium_test_section_creation():
    params = import_parameters()
    driver = get_driver()
    open_cyschoolhouse18_sb(driver)
    for p in params:
        create_single_section(driver, p)
    #driver.quit()
    
if __name__ == '__main__':
    selenium_test_section_creation()