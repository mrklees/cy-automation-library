# These are the libraries needed in the current implamentation
from selenium import webdriver # Selenium provides the framework we'll use to send scripts to Firefox.
from selenium.webdriver.common.keys import Keys
from time import sleep # A handy function we'll use to programm some wait time

# You will need to provide values for each of these variables for the script to work.
username = '' # usr/pass so that the script can log in to cyschoolhouse as you
password = ''
reportKey = "00O360000069dlN" # This value comes from the end of the URL of the report you're trying to pull.
downloadLocation = '~/GitHub/CYPY/CYSH Report Pipeline/'

# This block creates a Firefox profile which helps manage where files will download.
fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.download.dir",downloadLocation)
fp.set_preference("browser.helperApps.neverAsk.saveToDisk","text/csv")


driver = webdriver.Firefox(firefox_profile=fp) # Start Firefox with my profile created above
driver.get("https://cityyear.okta.com/login/do-login") # Navigate to login URL

#print(driver.title) #for testing purposes

# A note on navigating a webpage with selenium.  Frequently in creating these types of scripts you will need to view of a webpage in order to figure out what tag you are looking for.  I use either Firebug in Firefox or the built-in inspector in chrome (just right click on a webpage and choose Inspect).
elem = driver.find_element_by_name("username") # Finds the field in the HTML of the page by looking for the line where the name attribute is 'username'.
elem.clear() # Clears anything that may have already been in the field
elem.send_keys(username) # Mimics keystrokes to send your username to the correct field

elem = driver.find_element_by_name('password') # Same pattern as password
elem.clear()
elem.send_keys(password)

elem.send_keys(Keys.RETURN) # Presses the Enter key

sleep(4) # Waits 4 seconds for Okta to load

#After waiting it will try to click on the cyschoolhouse FY17 button.  I'm not sure if this current method will work for everyone.
try:
    elem = driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div/div[2]/ul[2]/li[12]/a/img')
    elem.click()
except:
    sleep(4)
    elem = driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div/div[2]/ul[2]/li[12]/a/img')
    elem.click()

sleep(6) # Waits 6 seconds for cyschoolhosue to load

for handle in driver.window_handles: #iterates through each window
    driver.switch_to_window(handle)
    if driver.title == "City Year - My Applications": driver.close() # if that window is the okta page, close it.

#print(driver.title)

driver.get("".join(["https://na30.salesforce.com/",reportKey,"?export=1&enc=UTF-8&xf=csv"])) # Export the desired report in csv form.