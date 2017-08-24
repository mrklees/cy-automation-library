# cyschoolhouse Automater

These scripts are used to automate the filling of forms and downloading of data from cyschoolhouse. 

## Table of Contents

    1. cyschoolhousesuite.py
        a. A suite of wrapper functions for tasks common to anything involved in automating cyschoolhouse.  Allows 
        us to call functions like "open_cyschoolhouse" instead of making direct calls to selenium. 
    2. section_creation.py
        a. The set of wrapper functions for creating sections.
    3. input_files
        a. A folder which contains the data that fills the forms for section creation etc... 


## Dependencies
The main dependencies are [Selenium](http://selenium-python.readthedocs.io/) and 
[selenium-requests](https://github.com/cryzed/Selenium-Requests) which are available via pip.  Make sure to follow the 
Selenium install instruction carefully, particularly in making sure that you have the appropriate driver for the browser 
you would like to use. The current scripts expect you to use Firefox, which uses the 
[gecko driver](https://github.com/mozilla/geckodriver/releases). Besides that, all other packages used are a part of the python core.
