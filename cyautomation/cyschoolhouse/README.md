# cyschoolhouse Automater

These scripts are used to automate the filling of forms and downloading of data from cyschoolhouse.

## Table of Contents

1. `cyschoolhousesuite.py`
 * A suite of wrapper functions for tasks common to anything involved in automating cyschoolhouse.  Allows user to call functions like "open_cyschoolhouse" instead of making direct calls to selenium.
* `section_creation.py`
 * The set of wrapper functions for creating sections.
* `input_files` folder
 * A folder which contains the data that fills the forms for section creation etc...

## Set-up

First, create a file in this directory called `credentials.ini`. Format this file as follows.
```
[Salesforce]
username = <your Salesforce username>
password = <your Salesforce password>
security_token = <your Salesforce security token>

['Salesforce Sandbox']
username = <your Salesforce Sandbox username>
password = <your Salesforce Sandbox password>
security_token = <your Salesforce Sandbox security token>

[Single Sign On] # Currently used only to send emails if you choose to do so.
username = <your Okta username>
password = <your Okta username>
```
You can find this information in Salesforce under your user settings. Your username should be similar to `username@cityyear.org.cyschorgb`. The password may not be the same as your single sign-on password through Okta. You may need to trigger a password reset in order to obtain the password associated with your Salesforce account. To do so, [submit a service ticket](https://mycityyear.force.com/ServiceDesk/500/o).

Second, review the details in `config.py`. In this file, you can toggle settings such as entering the sandbox environment (`SANDBOX = True`) and ignoring Chicago-specific functions (`CHICAGO_USER = False`).

## Usage
``` python
import cyschoolhouse as cysh

# Return a DataFrame of object records with all fields
cysh.get_object_df(object_name='Staff__c')

# Return a list of fields for a given object
cysh.get_object_fields(object_name='Staff__c')

# Return a DataFrame of object records with specific fields
cysh.get_object_df(object_name='Staff__c', field_list=['Individual__c', 'Name', 'CreatedDate', 'Reference_Id__c', 'Site__c', 'Role__c'])

# Return a DataFrame with a filter
cysh.get_object_df(object_name='Staff__c', field_list=['Individual__c', 'Name', 'Role__c'], where=f"Site__c = 'Chicago'")
```

## Dependencies
The main dependencies are [Selenium](http://selenium-python.readthedocs.io/) and
[selenium-requests](https://github.com/cryzed/Selenium-Requests) which are available via pip.  Make sure to follow the
Selenium install instruction carefully, particularly in making sure that you have the appropriate driver for the browser
you would like to use. The current scripts expect you to use Firefox, which uses the
[gecko driver](https://github.com/mozilla/geckodriver/releases). Besides that, all other packages used are a part of the python core.
