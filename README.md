# City Year Automation Library

The City Year Automation library is an effort to create a toolbox of automation scripts for solving various problems faced
by Impact Analytics points. Users of this library will need some basic understanding of Python, but the design of the
library is such that most of the coding is already done in some wrapper functions.  An IA point trying to implement these
tools should typically just need to write some small functions for their specific use case and perhaps load some data into a
specified format in Excel.

## Packages

* `cyschoolhouse`
 * An adapter for cyschoolhouse (Salesforce) that supports automated actions and database queries. This package is largely a set of helper functions built around the [simple-salesforce](https://github.com/simple-salesforce/simple-salesforce) package. Currently supports section creation, student uploads, syncing student enrollment across multiple sections, and sending email.
* `excel-updater`
 * A tool for updating Excel Workbooks. Can currently update excel workbooks, handle sheet protection and hiding, and provides a structure for writing functions to update specific workbooks in a particular order.
* `selenium-testing` (testing only)
  * This folder is largely a set of testing scripts used as a proof of concept of a few different features of Selenium, and is only relevant if you're interested in some of the more advanced features that are being tested.  

## Set-up

Install Python. If you are new to Python, [see here](README-setup-python.md).

Install GitHub and clone this repository to your computer. In your console, create a virtual environment (optional but recommended), navigate to the repository's root directory, and run `pip install -r requirements.txt`. This will install all the third party Python packages that are required for these tools.

Some scripts are used to manipulate files in cyconnect (SharePoint). This requires that the user map SharePoint as a network drive. Follow [this visual guide](README-setup-cyc.md) to set it up.

## cyschoolhouse Package

Files and folders mentioned in this section are relative to `./cyautomation/cyschoolhouse`.

* `cyschoolhousesuite.py`
 * A suite of wrapper functions for tasks common to anything involved in automating cyschoolhouse.  Allows user to call functions like `open_cyschoolhouse` instead of making direct calls to selenium.
* `section_creation.py`
 * The set of wrapper functions for creating sections.
* `service_trackers.py`
  * Generates pdf reports for each AmeriCorps Member on which they can manually track their weekly service implementation.
* `input_files` folder
  * Contains Excel workbooks that contain data to be uploaded. Theses are typically not used in Chicago.
* `templates` folder
  * Contains Excel workbooks that are populated by scripts and then written to cyconnect (SharePoint).

### Set-up

#### Credentials

Create a file called `credentials.ini`. Format this file as:
```
[Salesforce]
username = <your Salesforce username>
password = <your Salesforce password>
security_token = <your Salesforce security token>

[Salesforce Sandbox] # optional
username = <your Salesforce Sandbox username>
password = <your Salesforce Sandbox password>
security_token = <your Salesforce Sandbox security token>

[Single Sign On] # optional, currently used only to send emails
username = <your Okta username>
password = <your Okta username>
```

You can find this information in Salesforce under your user settings ([visual guide](README-setup-sf.md)). Your username should be similar to `username@cityyear.org.cyschorgb`. The password may not be the same as your Okta single sign-on password. You may need to trigger a password reset in order to obtain the password associated with your Salesforce account. To do so, submit a [service ticket](https://mycityyear.force.com/ServiceDesk/500/o).

#### Config

In `config.py`, you can toggle settings such as entering the sandbox environment (`SANDBOX = True`) and setting your city location (`USER_SITE = 'Chicago'`). Some scripts are specialized to Chicago's functions and file structure, and they are only available to Chicago users. However, different city users are encouraged to explore these scripts and adapt them to your use case.

## Usage

For more examples on how Chicago uses these scripts in production, see `CHI-schedule.py`.

``` python
import cyautomation.cyschoolhouse as cysh

# Return a DataFrame of object records with all fields
cysh.get_object_df(object_name='Staff__c')

# Return a list of fields for a given object
cysh.get_object_fields(object_name='Staff__c')

# Return a DataFrame of object records with specific fields
cysh.get_object_df(
    object_name='Staff__c',
    field_list=['Individual__c', 'Name', 'CreatedDate', 'Reference_Id__c', 'Site__c', 'Role__c']
  )

# Return a DataFrame with a filter
cysh.get_object_df(
    object_name='Staff__c',
    field_list=['Individual__c', 'Name', 'Role__c'],
    where=f"Site__c = 'Chicago'"
)
```

## Dependencies

Two important dependencies are [Selenium](http://selenium-python.readthedocs.io/) and
[selenium-requests](https://github.com/cryzed/Selenium-Requests) which are available via pip. The implementation of selenium in this repository expects you to use the Firefox browser with
[gecko driver](https://github.com/mozilla/geckodriver/releases). This driver is provided here at `./geckodriver/geckodriver.exe`. If you don't trust this executable, you can replace it with the version provided [here](https://github.com/mozilla/geckodriver/releases).

## Contribute

The easiest way to get started is to dive into the code, and when you find something that doesn't make sense, post an issue.  If
you keep getting an error when you're running the code, post an issue.  This doesn't require any coding beyond trying to get the scripts to run.

If you want to contribute code to the project, follow the traditional [GitHub workflow](https://guides.github.com/introduction/flow/):
1. fork the repository
* create a branch with a descriptive name
* implement your code improvements
* submit a pull request

Alternatively, reach out to Alex at aperusse@cityyear.org or Chris at chrisluedtke@gmail.com.
