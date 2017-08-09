# -*- coding: utf-8 -*-
'''
Excel Updated

Author: Alex Perusse
'''
# Python Core packages
import os
from time import sleep
from datetime import datetime
import sys
import logging

# win32 API 
import win32com.client as win32
import win32process
import win32gui
import win32api
import win32con

def open_excel():
    # Create a connector to Excel
    try:
        excel = win32.gencache.EnsureDispatch("Excel.Application")
        logging.debug("Launched Excel")
    except:
        logging.critical("Failed to launch Excel, quit")
        return None
    #excel = win32.Dispatch("Excel.Application")
    #excel = win32.dynamic.Dispatch("Excel.Application")
    excel.Visible = True
    excel.DisplayAlerts = False
    return excel

def open_workbook(fp, excel):
    """Wraps some of the boilerplate that we have to open and work with Excel.
    
    Args:
        fp (str): Filepath of workbook to open
    Returns:
        win32 Excel Application driver: active driver to the open instance of Excel
        Excel Workbook Socket: The open socket to the workbook we opened
    """
    # Leverages the connector to open a particular workbook
    try:
        wb = excel.Workbooks.Open(fp)
        logging.debug("Opened " + fp)
    except:
        logging.critical("Failed to open workbook")
        sys.exit(1)
        
    return wb

def refresh_save_quit(wb):
    """Refreshes, saves, and closes an open Excel workbook
    
    Args:
        wb (Excel Workbook Socket): The open socket to workbook to refresh
    """
    wb.RefreshAll()
    wb.Save()
    logging.debug("refreshed and saved workbook; closing")
    wb.Close(False)
    
def search_tree(parent_dir):
    """Searches the desginated parent dir and all subfolder, extracting the 
    filepaths and names of all files
    
    Args:
        parent_dir (str): The filepath of the parent directory
        
    Return:
        list: The list of 3-tuples with the dirpath, dirnames, and filesnames of 
        each child directory. 
    """
    children = [(dirpath, dirnames, filenames) for dirpath, dirnames, filenames in os.walk(parent_dir)]
    return children        

def get_all_filepaths(file_tree):
    """ Construct the list of all files in terms of their filepath
    
    Args:
        file_tree (list): the list of tuples from search_tree
    Returns:
        list: the list of strings of all files as absolute file paths
    """
    return ['\\'.join([path, file]) for (path, child_dirs, files) in file_tree for file in files if file.endswith('.xlsm')]

def update_all(parent_dir):
    all_files = search_tree(parent_dir)
    excel = open_excel()
    for path, child_dirs, files in all_files:
        os.chdir(path)
        print(path, child_dirs, files)
        for file in files:
            print(file)
            if is_file_checked_out(file):
                continue
            wb = open_workbook('\\'.join([path, file]), excel)
            sleep(3)
            if is_pq_available(excel):
               refresh_save_quit(wb)
            else:
                print("PowerQuery has been closed.  Please force close and open Excel.")
                break
            sleep(3)
    close_excel_by_force(excel)

def is_pq_available(excel):
    return excel.COMAddIns("Microsoft.Mashup.Client.Excel").Connect

def close_excel_by_force(excel):
    # Get the window's process id's
    hwnd = excel.Hwnd
    t, p = win32process.GetWindowThreadProcessId(hwnd)
    # Ask window nicely to close
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    # Allow some time for app to close
    sleep(3)
    # If the application didn't close, force close
    try:
        handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, p)
        if handle:
            win32api.TerminateProcess(handle, 0)
            win32api.CloseHandle(handle)
    except:
        pass

def configure_log():
    logging.basicConfig(filename='log/updater.log', level=logging.DEBUG)
    logging.info("Log of run on " + datetime.now().isoformat())

def is_file_checked_out(filename):
    try: 
        os.rename(filename, 'tempfile.xlsx')
        os.rename('tempfile.xlsx', filename)
        return False
    except OSError:
        logging.debug(filename + ' is still open. Has not been refreshed.')
        return True

if __name__ == '__main__':
    fp = 'P:\\Update Zone\\Testing Zone'
    #fp = 'C:\\Users\\aperusse\\Desktop\\FiveFiles'
    configure_log()
    update_all(fp)