# -*- coding: utf-8 -*-
import os
import updater

def update_large_engine():
    path = "P:\\Update Zone\\Databases"
    files = ["FY18 Five Col to Enrollment Report Transformation.xlsx"]    
    excel = updater.open_excel()
    os.chdir(path)
    for file in files:
        updater.update_single_workbook(file, path, excel, timer=60)

def update_fl_engines():
    path = "P:\\Update Zone\\Databases"
    files = ["2018 FL Engine.xlsm"]    
    excel = updater.open_excel()
    os.chdir(path)
    for file in files:
        updater.update_single_workbook(file, path, excel)

def update_fl_workbooks():
    path = "P:\\Update Zone\\Refresh Zone\\FL Workbooks"
    updater.update_all(path)
    
def update_all():
    update_large_engine()
    update_fl_engines()
    update_fl_workbooks()
    
if __name__ == "__main__":
    update_all()