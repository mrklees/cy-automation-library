from configparser import ConfigParser
import os

from pathlib import Path
import pandas as pd

__all__ = [
    'USER_SITE',
    'SF_URL',
    'SF_USER',
    'SF_PASS',
    'SF_TOKN',
    'LOG_PATH',
    'TEMP_PATH',
    'TEMPLATES_PATH',
    'get_sch_ref_df',
]

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

LOG_PATH = str(Path(__file__).parent / 'log')
TEMP_PATH = str(Path(__file__).parent / 'temp')
TEMPLATES_PATH = str(Path(__file__).parent / 'templates')

def get_sch_ref_df(sch_df_path = 'Z:\\ChiPrivate\\Chicago Data and Evaluation\\SY19\\SY19 School Reference.xlsx'):
    sch_ref_df = pd.read_excel(sch_df_path)
    sch_ref_df = sch_ref_df.loc[~sch_ref_df['Informal Name'].isin(['CE', 'Onboarding'])]

    return sch_ref_df
