# -*- coding: utf-8 -*-
"""CYLA Updater

This script utilizes the wrappers developed on top of the win32 api and executes 
the desired updates.  While the wrappers would allow you to point the updater at
the top folder in the folder structure and update everything, some differentiation
between different types of Excel workbooks might be required. For example, the standard
wait time is 8 seconds, however CYLA's larger engine files takes up to 60 seconds to refresh,
and I have had to separate out those files and set their timer's specifically.  This
approach also allows me to set the order of refreshes, which is a useful feature. 
"""
import os
import win32_wrapper
import logging
from time import time

def update_large_engine(excel):
    """Update very large Engines

    This function updates all files in the specified files list.  The key reason for making this a
    function of its own is in setting the timer to be 90 seconds instead of the standard 8.  This is 
    because the queries take an extremely long time for these engines to update.  
    
    """
    path = "P:\\Update Zone\\Databases"
    files = ["FY18 Five Col to Enrollment Report Transformation.xlsx"]    
    os.chdir(path)
    for file in files:
        win32_wrapper.update_single_workbook(file, path, excel, timer=90)

def update_small_engines(excel):
    path = "P:\\Update Zone\\Databases"
    files = ["2018 FL Engine.xlsm"]    
    excel = win32_wrapper.open_excel()
    os.chdir(path)
    for file in files:
        win32_wrapper.update_single_workbook(file, path, excel)

def update_fl_workbooks(excel):
    path = "P:\\Update Zone\\Refresh Zone\\FL Workbooks"
    win32_wrapper.update_all(path, excel=excel)
  
def update_deployment_workbook(excel):
    paths = ["P:\\Update Zone\\Refresh Zone\\Deployment Workbooks SEC",
             "P:\\Update Zone\\Refresh Zone\\Deployment Workbooks ELEM"]
    protections = [{"protect" : ["Dashboard", "LineSelection"],
                   "veryhide" : ["ClassLookup", "ACMLookups", "TeacherLookup", "Parameters"]},
                   {"protect" : ["Dashboard", "ElemLineSelection"],
                   "veryhide" : ["ACMLookups", "TeacherLookup", "Parameters"]}]
    for i, path in enumerate(paths):
        win32_wrapper.update_all(path, timer=30, excel=excel, protection=protections[i])
        
def update_all():
    excel = win32_wrapper.open_excel()
    logging.info("{}:Updating Large Engines".format(time()))
    update_large_engine(excel)
    logging.info("{}:Updating Small Engines".format(time()))
    update_small_engines(excel)
    logging.info("{}:Updating FL Workbooks".format(time()))
    update_fl_workbooks(excel)
    logging.info("{}:Updating Deployment Workbook".format(time()))
    update_deployment_workbook(excel)
    win32_wrapper.close_excel_by_force(excel)
    
if __name__ == "__main__":
    print('Loaded')