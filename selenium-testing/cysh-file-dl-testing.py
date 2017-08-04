# -*- coding: utf-8 -*-
'''
Selenium testing module. We're doing some important testing here on how 
to utilize selenium with requests.  The ultimate goal of this script will be
to prove that Selenium can meet 

'''
# Core python
import time
import csv
import os
import json

# The local 
from seleniumsuite import *

from seleniumrequests import Firefox
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# downloads a file using a GET request.    
def download_testfile_get(driver):
    url = 'https://na30.salesforce.com/00O360000069dSu?export=1&enc=UTF-8&xf=csv'
    fileloc = "testfile.csv"
    response = driver.request('GET', url)
    decoded = response.content.decode('utf-8')
    cr = csv.reader(decoded.splitlines(), delimiter=',')
    my_list = list(cr)
    with open(fileloc, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=",", quotechar='"')
        for row in my_list:
            #print(row)
            writer.writerow(row)
    return driver

# downloads a file using a POST request.
def download_testfile_post(driver):
    # Ended up going into the request body and adding the rt= to the right of the ? in the URL.  It actually worked!
    url = 'https://na30.salesforce.com/00O360000069dSu?rt=070360000002Cq2&last_modified_user_id=005360000027qPE&last_modified_by=Serhii+Pryshchepa&last_modified_date=6%2F21%2F2016+1%3A52+PM&scope=organization&colDt_c=0723600000M50GL&colDt_q=custom&colDt_s=&colDt_e=&enc=UTF-8&xf=localecsv&export=Export&co=1&ct=none&ctitle=&cp=b&cs=default&cs2=&cs3=&cs4=&chda=no&chum=no&chsa=mbars&cd0=&cd1=&csize=3&cfsize=12&ctsize=18&tfg=0&fg=0&bg1=16777215&bg2=16777215&bgdir=2&l=1&sal=yes&cdbr0=&cdbr1=&chsv=no&chsp=no&chst=no&cheh=no&chco=no&Yman=no&cr_summary0=&cr_lowcolor0=12735572&cr_midcolor0=12763732&cr_highcolor0=5554772&cr_lowbk0=&cr_highbk0=&cr_summary1=&cr_lowcolor1=12735572&cr_midcolor1=12763732&cr_highcolor1=5554772&cr_lowbk1=&cr_highbk1=&cr_summary2=&cr_lowcolor2=12735572&cr_midcolor2=12763732&cr_highcolor2=5554772&cr_lowbk2=&cr_highbk2=&duel0=0723600000M50GZ%2C0723600000M50GJ%2C0723600000M50Gg%2C0723600000M50Gc%2C0723600000M50Gd%2C0723600000M50Gi%2C0723600000M50GL%2C0723600000M50Ho&format=tt&sideBySide=false&show_subtotals=false&show_grandtotal=false&pc0=0723600000M50GZ&pn0=co&pv0=Cumulative+ADA&cc0=false&ss0=&irpe0=true&pc1=&pn1=&pv1=&cc1=false&ss1=&irpe1=true&pc2=&pn2=&pv2=&cc2=false&ss2=&irpe2=true&pc3=&pn3=&pv3=&cc3=false&ss3=&irpe3=true&pc4=&pn4=&pv4=&cc4=false&ss4=&irpe4=true&pc5=&pn5=&pv5=&cc5=false&ss5=&irpe5=true&pc6=&pn6=&pv6=&cc6=false&ss6=&irpe6=true&pc7=&pn7=&pv7=&cc7=false&ss7=&irpe7=true&pc8=&pn8=&pv8=&cc8=false&ss8=&irpe8=true&pc9=&pn9=&pv9=&cc9=false&ss9=&irpe9=true&pc10=&pn10=&pv10=&cc10=false&ss10=&irpe10=true&pc11=&pn11=&pv11=&cc11=false&ss11=&irpe11=true&pc12=&pn12=&pv12=&cc12=false&ss12=&irpe12=true&pc13=&pn13=&pv13=&cc13=false&ss13=&irpe13=true&pc14=&pn14=&pv14=&cc14=false&ss14=&irpe14=true&pc15=&pn15=&pv15=&cc15=false&ss15=&irpe15=true&pc16=&pn16=&pv16=&cc16=false&ss16=&irpe16=true&pc17=&pn17=&pv17=&cc17=false&ss17=&irpe17=true&pc18=&pn18=&pv18=&cc18=false&ss18=&irpe18=true&pc19=&pn19=&pv19=&cc19=false&ss19=&irpe19=true&pc20=&pn20=&pv20=&cc20=false&ss20=&irpe20=true&pc21=&pn21=&pv21=&cc21=false&ss21=&irpe21=true&pc22=&pn22=&pv22=&cc22=false&ss22=&irpe22=true&pc23=&pn23=&pv23=&cc23=false&ss23=&irpe23=true&details=yes&currency=000&bool_filter=&sort=&sortdir=down&topn=all&c_0=0723600000M50GZ&c_1=0723600000M50GJ&c_2=0723600000M50Gg&c_3=0723600000M50Gc&c_4=0723600000M50Gd&c_5=0723600000M50Gi&c_6=0723600000M50GL&c_7=0723600000M50Ho&cnt=8&v=142&id=00O360000069dSu&cust_name=Cumulative+ADA+Tabular&cust_devName=Cumulative_ADA_Tabular&ns=&cust_desc=&cust_owner=00l36000000OmLc&save_drill=&entity=&child=&reln=&_CONFIRMATIONTOKEN=VmpFPSxNakF4Tnkwd09DMHdOVlF5TXpvd01qbzFNaTQxTkRsYSxkRzFoclMzbGxzU0F1NmV5SzFsUjVlLFpXTXdNRGsz&saveAndSched='
    fileloc = "testfile.csv"
    response = driver.request('POST', url)
    decoded = response.content.decode('utf-8')
    cr = csv.reader(decoded.splitlines(), delimiter=',')
    my_list = list(cr)
    with open(fileloc, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=",", quotechar='"')
        for row in my_list:
            #print(row)
            writer.writerow(row)
    return driver

# runs the entire test script
def selenium_test_file_dl():
    driver = get_driver()
    driver = open_cyschoolhouse17(driver)
    driver = download_testfile_post(driver)
    driver.quit()
    
if __name__ == "__main__":
    selenium_test_file_dl()