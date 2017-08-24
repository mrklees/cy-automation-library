# City Year Automation Library

The City Year Automation library is an effort to create a toolbox of automation scripts for solving various problems faced
by Impact Analytics points. Users of this library will need some basic understanding of Python, but the design of the 
library is such that most of the coding is already done in some wrapper functions.  An IA point trying to implament these
tools should typically just need to write some small functions for their specific use case and perhaps load some data into a
specified format in Excel.

To dive into the tools, navigate into cyautomation and then select the relavant folder. A brief description of each tool is below,
but more detailed read me files exist for each product in their respective folders.  

## Table of Contents

    0. selenium-testing (testing only)
       a. This folder is largely a set of testing scripts used as a proof of concept of a few different features of 
       Selenium, and is only relevant if you're interested in some of the more advanced features that are being tested.  
    1. cyschoolhouse (in development)
       a. Contains scripts for automating actions in cyschoolhouse. Section creation is the main 
       focus of development right now. After that student enrollment and indicator areas. 
    2. excel-updater (in production)
       a. A tool for updating Excel Workbooks. Can currently update excel workbooks, handle sheet protection and 
       hiding, and provides a structure for writing functions to update specific workbooks in a particular order.  
       
## How to contribute!

The easiest way to get started is to dive into the code, and when you find something that doesn't make sense post an issue!  If 
you keep getting an error when you're running the code, post an issue!  This doesn't require any coding beyond trying to get the scripts to run.  

If you want to contribute code to the project, the easiest thing would be to reach out to Alex at aperusse@cityyear.org 
and [get added to the taiga](https://tree.taiga.io/project/mrklees-cy-web-automation-library/). There you can view our current 
backlog of features and the progress of development. 
