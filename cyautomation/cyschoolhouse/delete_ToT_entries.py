
# coding: utf-8

# In[26]:



from cyschoolhousesuite import *
from selenium.webdriver.support.ui import Select
import pandas as pd

# xlsx requires column "Time ID" with ISR records to delete as well as a column 'z_DELETED?' for reading in the status of whether the ISR entry has been deleted or null
path_to_xlsx = "Z:\\ChiPrivate\\Chicago Reports and Evaluation\\SY18\\SY18 ToT Audit\\ToT instances to delete.xlsx"

def import_parameters(path_to_xlsx):
    """Imports input data from xlsx
    """
    df = pd.read_excel(path_to_xlsx)
    df = df[pd.isnull(df['z_DELETED?'])]
    return df

def nav_to_ISR_record(driver, ISR_num):
    driver.find_element_by_xpath('//*[@id="sbstr"]').clear()
    driver.find_element_by_xpath('//*[@id="sbstr"]').send_keys(ISR_num)
    driver.find_element_by_xpath('//*[@id="sbstr"]').send_keys(Keys.RETURN)
    
def click_delete(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="topButtonRow"]/input[4]')))
    driver.find_element_by_xpath('//*[@id="topButtonRow"]/input[4]').click()
    EC.alert_is_present
    driver.switch_to.alert.accept()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[3]/table/tbody/tr/td[2]/div[2]/form/div/span/span[1]/input')))
   

# runs the entire test script
def selenium_test_intervention_setup():
    params = import_parameters(path_to_xlsx)
    driver = get_driver()
    open_cyschoolhouse18(driver)
    
    for ISR_num in params['Time ID'].unique():
        nav_to_ISR_record(driver, ISR_num)
        click_delete(driver)

    #driver.quit()
    
if __name__ == '__main__':
    selenium_test_intervention_setup()

