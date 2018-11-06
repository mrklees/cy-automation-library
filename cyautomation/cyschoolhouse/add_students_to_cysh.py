import os
from time import sleep

import numpy as np

import simple_cysh as cysh
from cyschoolhousesuite import *
from selenium.webdriver.support.ui import Select
from sendemail import send_email

sf = cysh.init_sf_session(sandbox=False)

## This is how the task would be accomplished via salesforce API, if only I could edit the fields:
#
# df = pd.read_excel(r'C:\Users\City_Year\Downloads\New Students for cyschoolhouse(1-11).xlsx')
# school_df = get_cysh_df('Account', ['Id', 'Name'])
# df = df.merge(school_df, how='left', left_on='School', right_on='Name')
# 
# drop_ids = []
# for index, row in df.iterrows():
#     search_result = cysh.query(f"SELECT Id FROM Student__c WHERE Local_Student_ID__c = '{row['Student CPS ID']}'")
#     if len(search_result['records']) > 0:
#         drop_ids.append(row['Student CPS ID'])
# df = df.loc[~df['Student CPS ID'].isin(drop_ids)]
# 
# for index, row in df.iterrows():
#     stu_dict = {
#         'Local_Student_ID__c':str(row['Student CPS ID']),
#         'School__c':row['Id'],
#         'Name':(row['Student First Name'] + ' ' + row['Student Last Name']),
#         'Student_Last_Name__c':row['Student Last Name'],
#         'Grade__c':str(row['Student Grade Level']), 
#         #'School_Name__c':row['Name_y'],
#     }


def import_parameters(xlsx_path, enrollment_date):
    """Imports input data from xlsx
    """
    df = pd.read_excel(xlsx_path, converters={'*REQ* Grade':int})

    column_rename = {
        'Student CPS ID':'*REQ* Local Student ID',
        'Student First Name':'*REQ* First Name',
        'Student Last Name':'*REQ* Last Name',
        'Student Grade Level':'*REQ* Grade',
    }

    df.rename(columns=column_rename, inplace=True)
    
    df["*REQ* Student Id"] =  df['*REQ* Local Student ID']
    df["*REQ* Entry Date"] = enrollment_date
    df["*REQ* Type"] = 'Student'
    df["Date of Birth"] = np.nan
    df["Gender"] = np.nan
    df["Ethnicity"] = np.nan
    df["Disability Flag"] = np.nan
    df['ELL'] = np.nan

    col_order = [
        'School',
        '*REQ* Student Id',
        '*REQ* Local Student ID',
        '*REQ* First Name',
        '*REQ* Last Name',
        '*REQ* Grade',
        'Date of Birth', #nan
        'Gender', #nan
        'Ethnicity', #nan
        'Disability Flag', #nan
        'ELL', #nan
        '*REQ* Entry Date',
        '*REQ* Type',
    ]

    df = df[col_order]
    
    return df

def remove_extant_students(df, sf=sf):
    local_student_id_col = '*REQ* Local Student ID'
    drop_ids = []
    for index, row in df.iterrows():
        search_result = sf.query(f"SELECT Id FROM Student__c WHERE Local_Student_ID__c = '{row[local_student_id_col]}'")
        
        if len(search_result['records']) > 0:
            drop_ids.append(row[local_student_id_col])
            
        del search_result
            
    df = df.loc[~df[local_student_id_col].isin(drop_ids)]
    
    return df

def input_file(driver, path_to_csv):
    driver.find_element_by_xpath('//*[@id="selectedFile"]').send_keys(path_to_csv)
    driver.find_element_by_xpath('//*[@id="j_id0:j_id42"]/div[3]/div[1]/div[6]/input[2]').click()

def insert_data(driver):
    driver.find_element_by_xpath('//*[@id="startBatchButton"]').click()
    
def intervention_student_setup(xlsx_dir, xlsx_name, enrollment_date, sf=sf):
    """ Runs the entire student upload process.
    """
    xlsx_path = os.path.join(xlsx_dir, xlsx_name)
    
    params = import_parameters(xlsx_path, enrollment_date)
    params = remove_extant_students(params)
    
    setup_df = cysh.get_object_df('Setup__c', ['Id', 'School__c'], rename_id=True, rename_name=True)
    school_df = cysh.get_object_df('Account', ['Id', 'Name'])
    setup_df = setup_df.merge(school_df, how='left', left_on='School__c', right_on='Id'); del school_df
    setup_df = setup_df.loc[~setup_df['Id'].isnull()]
    
    sch_ref_df = pd.read_excel('Z:\\ChiPrivate\\Chicago Data and Evaluation\\SY19\\SY19 School Reference.xlsx')
    
    if len(params) > 0:
        driver = get_driver()
        open_cyschoolhouse19(driver)

        for school_name in params['School'].unique():
            # Write csv
            path_to_csv = os.path.join(xlsx_dir, f"SY19 New Students for CYSH - {school_name}.csv")
            df_csv = params.loc[params["School"]==school_name].copy()
            df_csv.drop(["School"], axis=1, inplace=True)
            df_csv.to_csv(path_to_csv, index=False, date_format='%m/%d/%Y')

            # Navigatge to student enrollment page
            setup_id = setup_df.loc[setup_df['Name']==school_name, 'Setup__c'].values[0]
            driver.get(f'https://c.na30.visual.force.com/apex/CT_core_LoadCsvData_v2?setupId={setup_id}&OldSideBar=true&type=Student')
            sleep(2)

            input_file(driver, path_to_csv)
            sleep(2)

            insert_data(driver)
            sleep(2)

            # Publish
            # Seems to work, but not completely sure if script 
            # pauses until upload is complete, both for the "Insert Data"
            # phase, and the "Publish Staff/Student Records" phase.

            driver.get(f'https://c.na30.visual.force.com/apex/schoolsetup_staff?setupId={setup_id}')
            driver.find_element_by_css_selector('input.red_btn').click()
            sleep(3)

            os.remove(path_to_csv)

        to_addrs = sch_ref_df.loc[sch_ref_df['School'].isin(params['School']), 'Manager Email'].tolist()

        send_email(
            to_addrs = list(set(to_addrs)),
            subject = 'New student(s) now in cyschoolhouse',
            body = 'The student(s) you submitted have been successfully uploaded to cyschoolhouse.'
        )

        #driver.quit()

def update_student_External_Id(sf=sf):
    """ Updates 'External_Id__c' field to 'CPS_' + 'Local_Student_ID__c'. Triggers external integrations at HQ.
    """
    school_df = cysh.get_object_df('Account', ['Id', 'Name'])
    student_df = cysh.get_object_df('Student__c', ['Id', 'Local_Student_ID__c', 'External_Id__c'], where=f"School__c IN ({str(school_df['Id'].tolist())[1:-1]})")
    
    if sum(student_df['Local_Student_ID__c'].duplicated()) > 0:
        raise ValueError(f'Error: Duplicates exist on Local_Student_ID__c.')
    
    student_df = student_df.loc[student_df['External_Id__c'].isnull() & (student_df['Local_Student_ID__c'].str.len()==8)]
    
    results = []
    for index, row in student_df.iterrows():
        result = sf.Student__c.update(row['Id'],{'External_Id__c':('CPS_' + row['Local_Student_ID__c'])})
        results.append(result)
        
    return results