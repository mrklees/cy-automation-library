# -*- coding: utf-8 -*-
"""Automated Section Creation
Script for the automatic creation of sections in cyschoolhouse. Please ensure
you have all dependencies, and have set up the input file called "section-creator-input.xlsx"
in the input files folder.
"""
import logging, os

import pandas as pd
from selenium.webdriver.support.ui import Select

from .cyschoolhousesuite import *


def import_parameters():
    """Import configuration data from Excel.
    """
    data = pd.read_excel(os.path.join(os.path.dirname(__file__), 'input_files/section-creator-input.xlsx'))
    data['Start_Date'] = pd.to_datetime(data['Start_Date']).dt.strftime('%m/%d/%Y')
    data['End_Date'] = pd.to_datetime(data['End_Date']).dt.strftime('%m/%d/%Y')
    data.fillna('', inplace=True)
    data.replace('NaT', '', inplace=True)
    return data.to_dict(orient='records')

def input_staff_name(driver, staff_name):
    """Selects the staff name from the drop down
    """
    dropdown = Select(driver.find_element_by_id("j_id0:j_id1:staffID"))
    dropdown.select_by_visible_text(staff_name)

def fill_static_elements(driver, insch_extlrn, start_date, end_date, target_dosage):
    """Fills in the static fields in the section creation form

    Includes the start/end dat, days of week, if time is in or out of school,
    and the estimated amount of time for that section.
    """
    driver.find_element_by_id("j_id0:j_id1:startDateID").send_keys(start_date)
    driver.find_element_by_id("j_id0:j_id1:endDateID").send_keys(end_date)
    driver.find_element_by_id("j_id0:j_id1:freqID:1").click()
    driver.find_element_by_id("j_id0:j_id1:freqID:2").click()
    driver.find_element_by_id("j_id0:j_id1:freqID:3").click()
    driver.find_element_by_id("j_id0:j_id1:freqID:4").click()
    driver.find_element_by_id("j_id0:j_id1:freqID:5").click()
    dropdown = Select(driver.find_element_by_id("j_id0:j_id1:inAfterID"))
    dropdown.select_by_visible_text(insch_extlrn)
    driver.find_element_by_id("j_id0:j_id1:totalDosageID").send_keys(str(target_dosage))

def select_school(driver, school):
    """ Selects the school name from section creation form
    """
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "j_id0:j_id1:school-selector")))
    dropdown = Select(driver.find_element_by_id("j_id0:j_id1:school-selector"))
    dropdown.select_by_visible_text(school)

def select_subject(driver, section_name):
    """ Selects the section type
    """
    driver.find_element_by_xpath("//label[contains(text(), '"+ section_name +"')]").click()

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@value='Proceed']")))
        driver.find_element_by_xpath("//input[@value='Proceed']").click()
    except:
        print("Hopefully it's okay")

def save_section(driver):
    """ Saves the section
    """
    driver.find_element_by_css_selector('input.black_btn:nth-child(2)').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                    '/html/body/div[1]/div[3]/table/tbody/tr/td[2]/div[4]/div[1]/table/tbody/tr/td[2]/input[5]')))

def update_nickname(driver, nickname):
    driver.find_element_by_css_selector('#topButtonRow > input:nth-child(3)').click()
    sleep(2)
    driver.find_element_by_id("00N1a000006Syte").send_keys(nickname)
    driver.find_element_by_xpath("//input[@value=' Save ']").click()
    sleep(2)

def create_single_section(school, acm, sectionname, insch_extlrn, start_date, end_date, target_dosage, nickname=None, driver=None):
    """ Creates one single section
    """
    if driver is None:
        driver = get_driver()
        open_cyschoolhouse(driver)
    driver.get('https://na30.salesforce.com/a1v/e')
    select_school(driver, school)
    sleep(2)
    select_subject(driver, sectionname)
    sleep(2.5)
    input_staff_name(driver, acm)
    fill_static_elements(driver, insch_extlrn, start_date, end_date, target_dosage)
    sleep(1)
    save_section(driver)
    logging.info(f"Created {parameter['SectionName']} section for {parameter['ACM']}")
    if 'Nickname' in parameter.keys():
        if parameter['Nickname'] != "":
            update_nickname(driver, parameter['Nickname'])

def section_creation(driver=None):
    """ Runs the entire script.
    """
    params = import_parameters()

    if driver is None:
        driver = get_driver()
        open_cyschoolhouse(driver)

    for index, row in params.iterrows():
        try:
            create_single_section(driver, school=row['School'], acm=row['ACM'], sectionname=row['SectionName'],
                insch_extlrn=row['In_School_or_Extended_Learning'], start_date=row['Start_Date'], end_date=row['End_Date'],
                target_dosage=row['Target_Dosage'])
        except:
            print(f"Section creation failed: {row['ACM']}, {row['SectionName']}")
            logging.error(f"Section creation failed: {row['ACM']}, {row['SectionName']}")
            driver.get('https://na30.salesforce.com/')
            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present())
                driver.switch_to.alert.accept()
                sleep(2)
            except TimeoutException:
                print("No alert")
            continue
    driver.quit()

if __name__ == '__main__':
    section_creation()
