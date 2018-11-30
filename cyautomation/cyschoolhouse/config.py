from configparser import ConfigParser
import os

from pathlib import Path


USER_SITE = 'Chicago'

SANDBOX = False

creds_path = str(Path(__file__).parent / 'credentials.ini')

config = ConfigParser()
config.read(creds_path)

if SANDBOX == False:
    SF_URL = "https://na82.salesforce.com"
    sf_creds = config['Salesforce']

elif SANDBOX == True:
    SF_URL = "https://cs59.salesforce.com"
    sf_creds = config['Salesforce Sandbox']

SF_USER = sf_creds['username']
SF_PASS = sf_creds['password']
SF_TOKN = sf_creds['security_token']
