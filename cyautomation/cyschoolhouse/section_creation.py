# -*- coding: utf-8 -*-
"""Automated Section Creation
Script for the automatic creation of sections in cyschoolhouse. Please ensure
you have all dependencies, and have set up the input file called "section-creator-input.csv"
"""
import csv
from cyschoolhousesuite import *
from selenium.webdriver.support.ui import Select

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
    with open('input_files/section-creator-input.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
        lst = list(reader)
    return lst

def nav_to_section_creation_form(driver):
    driver.get('https://cs17.salesforce.com/a1A/o')
    driver.find_element_by_name("new").click()
    return driver

def input_staff_name(driver, staff_name):
    dropdown = Select(driver.find_element_by_id("j_id0:j_id1:staffID"))
    dropdown.select_by_visible_text(staff_name)
    return driver

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
    return driver

def select_subject(driver, section):
    section_name = section_info[section]['name']
    driver.find_element_by_xpath("//*[contains(text(), '"+ section_name +"')]").click()
    driver.find_element_by_xpath("//input[@value='Proceed']").click()
    return driver

# runs the entire test script
def selenium_test_section_creation():
    params = import_parameters()
    driver = get_driver()
    driver = open_cyschoolhouse18_sb(driver)
    driver = nav_to_section_creation_form(driver)
    driver = select_subject(driver, params[0]['Section'])
    driver = input_staff_name(driver, params[0]['ACM'])
    driver = fill_static_elements(driver)
    driver.quit()
    
if __name__ == '__main__':
    selenium_test_section_creation()