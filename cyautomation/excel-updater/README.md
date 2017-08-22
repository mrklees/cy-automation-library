# Excel Updater Readme

The only dependency for this tool besides python 3.x is the win32 api. To 
install the api [download and install Build 221 from sourceforge.](https://sourceforge.net/projects/pywin32/files/pywin32/)
After that you will have all dependencies installed and everything in win32 wrapper should work. The key next step
is to create a file like the example provide: cyla_updater.py.  This file utilizes the functions in the win32 wrapper
in order to update single or sets of workbooks. Documentation in the win32 wrapper can be reviewed for some details on
what each function does and what it expects as arguments.  The intent is that you will be able to copy and paste a function 
from cyla_updater and simply change the file path to get it to work. 
