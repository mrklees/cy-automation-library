# -*- coding: utf-8 -*-
"""

"""
import os
import updater
import logging
from time import time

def update_large_engine(excel):
    path = "P:\\Update Zone\\Databases"
    files = ["FY18 Five Col to Enrollment Report Transformation.xlsx"]    
    os.chdir(path)
    for file in files:
        updater.update_single_workbook(file, path, excel, timer=60)

def update_small_engines(excel):
    path = "P:\\Update Zone\\Databases"
    files = ["2018 FL Engine.xlsm"]    
    excel = updater.open_excel()
    os.chdir(path)
    for file in files:
        updater.update_single_workbook(file, path, excel)

def update_fl_workbooks(excel):
    path = "P:\\Update Zone\\Refresh Zone\\FL Workbooks"
    updater.update_all(path, excel=excel)
  
def update_deployment_workbook(excel):
    paths = ["P:\\Update Zone\\Refresh Zone\\Deployment Workbooks SEC",
            "P:\\Update Zone\\Refresh Zone\\Deployment Workbooks ELEM"]
    protections = [{"protect" : ["Dashboard", "LineSelection"],
                   "veryhide" : ["ClassLookup", "ACMLookups", "TeacherLookup", "Parameters"]},
                   {"protect" : ["Dashboard", "ElemLineSelection"],
                   "veryhide" : ["ACMLookups", "TeacherLookup", "Parameters"]}]
    for i, path in enumerate(paths):
        updater.update_all(path, timer=30, excel=excel, protection=protections[i])
        
def update_all():
    excel = updater.open_excel()
    logging.info("{}:Updating Large Engines".format(time()))
    update_large_engine(excel)
    logging.info("{}:Updating Small Engines".format(time()))
    update_small_engines(excel)
    logging.info("{}:Updating FL Workbooks".format(time()))
    update_fl_workbooks(excel)
    logging.info("{}:Updating Deployment Workbook".format(time()))
    update_deployment_workbook(excel)
    updater.close_excel_by_force(excel)
    
if __name__ == "__main__":
    updater.configure_log()
    excel = updater.open_excel()
    logging.info("{}:Updating Deployment Workbook".format(time()))
    update_deployment_workbook(excel)
    updater.close_excel_by_force(excel)