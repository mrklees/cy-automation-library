"""Student Enrollment Script

We will eliminate yet another manual task for the Impact Analytics 
team by automating the enrollment of students into sections on cyschoolhouse.
"""

from time import sleep
import cyschoolhousesuite as cysh
from pandas import read_csv

def search_for_ACM(driver, sec_num):
    driver.find_element_by_class_name("searchTextBox").send
    return None

def input_data():
    data = read_csv('input_files/section-key.csv')
    return data.to_dict(orient='records')

def test_script():
    inputs = input_data()[0]
    driver = cysh.get_driver()
    cysh.open_cyschoolhouse18_sb(driver)

if __name__ == "__main__":
    print("Running Student Enrollment Script")
    print(input_data())
    