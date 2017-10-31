
# coding: utf-8

# In[74]:

from cyschoolhousesuite import *
from selenium.webdriver.support.ui import Select
from time import sleep
import pandas as pd
import numpy as np

path_to_xlsx = "Z:\\ChiPrivate\\Chicago Data and Evaluation\\SY18\\"
xlsx_name = "SY18 Students to Upload to cyschoolhouse.xlsx"

def import_parameters():
    """Imports input data from xlsx
    """
    df = pd.read_excel(path_to_xlsx + xlsx_name, converters={'*REQ* Grade':int})

    df = df[pd.isnull(df["STATUS"]) & pd.notnull(df["*REQ* School"])]
    df["Entry Date"] = "7/1/2017"
    df["Email Address"] = np.nan
    df["Address"] = np.nan
    df["City"] = np.nan
    df["State"] = np.nan
    df["Zip"] = np.nan
    df["Phone"] = np.nan
    df["*REQ* Type"] = "Student"
    df["Local Student ID"] = df["*REQ* Student Id"]
    df["ELL"].replace([0.0, 1.0],["FALSE", "TRUE"], inplace=True)

    cols = ['STATUS',
            '*REQ* School',
            '*REQ* Student Id',
            '*REQ* First Name',
            '*REQ* Last Name',
            '*REQ* Grade',
            'Date of Birth',
            'Gender',
            'Ethnicity',
            'Disability Flag',
            'ELL',
            'Entry Date',
            'Email Address',
            'Address',
            'City',
            'State',
            'Zip',
            'Phone',
            '*REQ* Type',
            'Local Student ID']

    df = df[cols]
    
    return df

def write_csv(params, path_to_xlsx, school_name):
    df_csv = params[params["*REQ* School"]==school_name]
    df_csv.drop(["STATUS","*REQ* School"], axis=1, inplace=True)
    df_csv["*REQ* Student Id"] = range(0, len(df_csv))
    df_csv.to_csv(path_to_xlsx + school_name + ".csv", index=False, date_format='%m/%d/%Y')

def nav_to_intervention_setup(driver):
    # Maybe not the best url:
    driver.get('https://c.na24.visual.force.com/apex/IM_InterventionsSetup?sfdc.tabName=01r1a000000QQ87')
    sleep(2)
    
def input_school_name(driver, school_name):
    dropdown = Select(driver.find_element_by_id("j_id0:j_id49:schools"))
    dropdown.select_by_visible_text(school_name)
    sleep(2)
    
def load(driver):
    driver.find_element_by_css_selector('input.drk_blue_btn').click()
    sleep(2)
    
def load_from_csv(driver):
    driver.find_element_by_css_selector('input.black_btn').click()
    sleep(2)
    
def choose_student_object(driver):
    driver.switch_to.window(driver.window_handles[1])
    dropdown = Select(driver.find_element_by_id("j_id0:j_id42:objectTypeSelect"))
    dropdown.select_by_visible_text('Student Holding Object Template')
    sleep(2)
    
def input_file(driver, school_name, path_to_xlsx):
    driver.find_element_by_xpath('//*[@id="selectedFile"]').send_keys(path_to_xlsx + school_name + ".csv")
    driver.find_element_by_xpath('//*[@id="j_id0:j_id42"]/div[3]/div[1]/div[6]/input[2]').click()
    sleep(2)

def insert_data(driver):
    driver.find_element_by_xpath('//*[@id="startBatchButton"]').click()
    sleep(2)
    
def publish(driver):
    # navigate back to first tab
    driver.switch_to.window(driver.window_handles[0])
    # click button to publish
    driver.find_element_by_css_selector('input.red_btn').click()
    sleep(2)
    
# runs the entire test script
def selenium_test_intervention_setup():
    params = import_parameters()
    driver = get_driver()
    open_cyschoolhouse18(driver)
    
    # For testing
    # school_name = ""
    
    for school_name in params['*REQ* School'].unique():
        write_csv(params, path_to_xlsx, school_name)

        nav_to_intervention_setup(driver)
        input_school_name(driver, school_name)
        load(driver)
        load_from_csv(driver)
        choose_student_object(driver)
        input_file(driver, school_name, path_to_xlsx)
        insert_data(driver)
        publish(driver)
        """Seems to work, but not completely sure if script 
        pauses until upload is complete, both for the "Insert Data"
        phase, and the "Publish Staff/Student Records" phase.
        """        
        os.remove(path_to_xlsx + school_name + ".csv")

    #driver.quit()
    
if __name__ == '__main__':
    selenium_test_intervention_setup()

