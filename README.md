# City Year Automation Library

Welcome!  This is a home for automation projects which are being developed by members of the City Year Python Community. A current primary focus is web automation.  Many tasks that are given to impact points involve needless amounts of repetitive activity on SalesForce or in other contexts.  Using tools like Selenium we can automate many of these tasks.  Our goal is to create wrappers which allows a user to pass in some parameters in the form of a csv, and have Selenium create sections, enroll students, and make focus list changes based on that. 

## Table of Contents
    
    1. selenium-testing
       a. Contains a couple scripts used as a proof of concept of a few different 
       features of Selenium.  Currently there is a file, seleniumsuite, which 
       contains some of the more general navigation functions, and then two test 
       files currently being used.  First the cysh-file-dl-testing script demonstrates 
       how to use a get request to download a file after logging into Okta and 
       cyschoolhouse using Selenium. Second, the cysh-section-creation-testing 
       script demonstrates the creation of a single section using a csv input.
    2. cyschoolhouse
       a. Contains scripts for automating actions in cyschoolhouse. In current development.
    3. excel-updater
       a. A tool for updating Excel Workbooks. Can currently update excel workbooks, 
       handle sheet protection and hiding, and provides a structure for writing 
       functions to update specific workbooks in a particular order.  

## Dependencies

For projects 1 and 2, the main dependencies are [Selenium](http://selenium-python.readthedocs.io/) and [selenium-requests](https://github.com/cryzed/Selenium-Requests) which are available via pip.  Make sure to follow the Selenium install instruction carefully, particularly in making sure that you have the appropriate driver for the browser you would like to use. The current scripts expect you to use Firefox, which uses the [gecko driver](https://github.com/mozilla/geckodriver/releases). Besides that, all other packages used are a part of the python core. 

For the excel updater we ustilize the win32 api in order to essentially send commands to Excel as if we were VBA or something more native.  To use this script you will need to [download and install Build 221 from sourceforge.](https://sourceforge.net/projects/pywin32/files/pywin32/)

## How to contribute!

The easiest way to get started is to dive into the code, and when you find something that doesn't make sense post an issue!  If you keep getting an error when you're running the code, post an issue!  This doesn't require any coding beyond trying to get the scripts to run.  

If you want to contribute code to the project, the easiest thing would be to reach out to Alex at aperusse@cityyear.org and [get added to the taiga](https://tree.taiga.io/project/mrklees-cy-web-automation-library/). There you can view our current backlog of features and the progress of development. 
