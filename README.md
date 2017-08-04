# City Year Python Library

Welcome!  This is a home for coding projects which are being developed by members of the City Year Python Community. A current primary focus is web automation.  Many tasks that are given to impact points involve needless amounts of repetitive activity on SalesForce or in other contexts.  Using tools like Selenium we can automate many of these tasks.  Our goal is to create wrappers which allows a user to pass in some parameters in the form of a csv, and have Selenium create sections, enroll students, and make focus list changes based on that. 

## Table of Contents
    
    1. selenium-testing
       a. Contains a couple scripts used as a proof of concept of a few different features of Selenium.  Currently there is a file, seleniumsuite, which contains some of the more general navigation functions, and then two test files currently being used.  First the cysh-file-dl-testing script demonstrates how to use a get request to download a file after logging into Okta and cyschoolhouse using Selenium. Second, the cysh-section-creation-testing script demonstrates the creation of a single section using a csv input.
    2. cyschoolhouse
       a. Contains scripts for automating actions in cyschoolhouse. In current development.

## Dependencies
The main dependencies are Selenium and selenium-requests.  Make sure to follow the Selenium install instruction carefully, particularly in making sure that you have the appropriate driver for the browser you would like to use. The current scripts expect you to use Firefox, which uses the gecko driver. Besides that, all other packages used are a part of the python core. 

## How to contribute!

The easiest way to get started is to dive into the code, and when you find something that doesn't make sense post an issue!  If you keep getting an error when you're running the code, post an issue!  This doesn't require any coding beyond trying to get the scripts to run.  

For those who want to start contributing code, its time to fork the project.
