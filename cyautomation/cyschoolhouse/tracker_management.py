import pandas as pd
import simple_cysh as cysh
import os
import xlwings as xw # Excel must be closed prior to running script

def get_staff_df():
    staff_df = cysh.get_object_df('Staff__c', ['Individual__c', 'First_Name_Staff__c', 'Name', 'Organization__c', 'Role__c', 'Staff_Last_Name__c'], where="Site__c = 'Chicago'")
    # First Name plus Last Initial
    staff_df['First_Name_Staff__c'] = staff_df['First_Name_Staff__c'] + " " + staff_df['Staff_Last_Name__c'].astype(str).str[0] + "."
    del staff_df['Staff_Last_Name__c']

    schools_df = cysh.get_object_df('Account', ['Id', 'Name'])
    schools_df.rename(columns={'Id':'Organization__c', 'Name':'School'}, inplace=True)
    staff_df = staff_df.merge(schools_df, how='left', on='Organization__c')
    staff_df.sort_values('Name', inplace=True)
    
    return staff_df

def get_attendance_roster():
    program_df = cysh.get_object_df('Program__c', ['Id', 'Name'], rename_id=True, rename_name=True)
    student_section_df = cysh.get_object_df('Student_Section__c', ['Id', 'Name', 'Student_Name__c', 'Student__c', 'Program__c', 'School__c'], rename_id=True, rename_name=True)
    df = student_section_df.merge(program_df, how='left', on='Program__c')
    df = df.loc[df['Program__c_Name']=='Coaching: Attendance']
    df.sort_values('Student_Name__c', inplace=True)
    
    return df

def fill_one_coaching_log_acm_rollup(wb):
    sht = wb.sheets['ACM Rollup']
    sht.range('A:N').clear_contents()
    
    cols = [
        'Individual__c',
        'ACM',
        'Date',
        'Role',
        'Coaching Cycle',
        'Subject',
        'Focus',
        'Strategy/Skill',
        'Notes',
        'Action Steps',
        'Completed?',
        'Followed Up'
    ]

    sht.range('A1').value = cols

    sht.range(f'A2:A3000').value = "=INDEX('ACM Validation'!$A:$A, MATCH($B2, 'ACM Validation'!$C:$C, 0))"
    
    not_acm_sheets = [
        'Dev Tracker',
        'Dev Map',
        'ACM Validation',
        'ACM Rollup',
        'Calendar Validation',
        'Log Validation',
    ]
    
    acm_sheets = [x.name for x in wb.sheets if x.name not in not_acm_sheets]
    
    start_row = 2
    for sheet_name in acm_sheets:
        sheet_name = sheet_name.replace("'", "''")
        sht.range(f'B{start_row}:B{start_row + 300}').value = f"='{sheet_name}'!$A$1"
        sht.range(f'C{start_row}:L{start_row + 300}').value = f"='{sheet_name}'!A3"
        start_row += 300

def fill_all_coaching_log_acm_rollup(school_ref_df):
    for index, row in school_ref_df.iterrows():
        try:
            wb = xw.Book(f"Z:\{row['Informal Name']} Leadership Team Documents\SY19 Coaching Log - {row['Informal Name']}.xlsx")
            fill_one_coaching_log_acm_rollup(wb)
            wb.save(f"Z:\{row['Informal Name']} Leadership Team Documents\SY19 Coaching Log - {row['Informal Name']}.xlsx")
            wb.close()
        except:
            print(f"{row['Informal Name']} failed to generate ACM Rollup sheet")
            wb.close()
            pass

def prep_coaching_log():    
    wb.sheets['Dev Tracker'].range('A1,A5:L104').clear_contents()
    wb.sheets['ACM1'].range('A1,A3:J300').clear_contents()
    
    # Create ACM Copies
    for x in range(2,11):
        wb.sheets['ACM1'].api.Copy(Before=wb.sheets['Dev Map'].api)
        wb.sheets['ACM1 (2)'].name = f'ACM{x}'

def deploy_choaching_logs():
    ## Multiply by Schools
    for index, row in school_ref_df.iterrows():
        school_staff = staff_df.loc[(staff_df['School']==row['School']) & 
                                    staff_df['Role__c'].str.contains('Corps Member')]
        
        wb.sheets['Dev Tracker'].range('A1,A5:L104').clear_contents()
        wb.sheets['Dev Tracker'].range('A1').value = f"SY19 Coaching Log - {row['Informal Name']}"

        wb.sheets['ACM Validation'].range('A:N').clear()
        wb.sheets['ACM Validation'].range('A1').options(index=False, header=False).value = school_staff.copy()

        pos = 0
        sheets_added = []
        for staff_index, staff_row in school_staff.iterrows():
            pos += 1
            sht = wb.sheets[f'ACM{pos}']
            sht.name = staff_row['First_Name_Staff__c']
            sht.range('A1').value = staff_row['Name']
            sheets_added += [sht.name]

        try:
            wb.save(f"Z:\{row['Informal Name']} Leadership Team Documents\SY19 Coaching Log - {row['Informal Name']}.xlsx")
            #wb.save(f"Z:\ChiPrivate\Chicago Data and Evaluation\SY19\Tests\SY19 Coaching Log - {row['Informal Name']}.xlsx")
        except:
            print(f"Save failed {row['Informal Name']}")
            pass

        # Reset Sheets
        pos = 0
        for sheet_name in sheets_added:
            pos += 1
            wb.sheets[sheet_name].name = f'ACM{pos}'
        
def deploy_tracker(resource, containing_folder):
    """ Distributes Excel tracker template to school team folders
    
    resource like 'SY19 Attendance Tracker' or 'SY19 Leadership Tracker'
    containing_folder like 'Team Documents' or 'Leadership Team Documents'
    """
    template_path = f'Z:\ChiPrivate\Chicago Data and Evaluation\SY19\Templates\{resource} Template.xlsx'
    wb = xw.Book(template_path)
    
    school_ref_path = r'Z:\ChiPrivate\Chicago Data and Evaluation\SY19\SY19 School Reference.xlsx'
    school_ref_df = pd.read_excel(school_ref_path)
    
    for index, row in school_ref_df.iterrows():
        wb.sheets['Tracker'].range('A1').clear_contents()
        wb.sheets['Tracker'].range('A1').value = f"{resource} - {row['Informal Name']}"
        
        try:
            wb.save(f"Z:\{row['Informal Name']} {containing_folder}\{resource} - {row['Informal Name']}.xlsx")
        except:
            print(f"Save failed {row['Informal Name']}")
            pass
        
    wb.close()

def update_all_validation_sheets(resource, containing_folder):
    school_ref_path = r'Z:\ChiPrivate\Chicago Data and Evaluation\SY19\SY19 School Reference.xlsx'
    school_ref_df = pd.read_excel(school_ref_path)
    
    staff_df = get_staff_df()
    att_df = get_attendance_roster()
    
    for index, row in school_ref_df.iterrows():     
        wb = xw.Book(f"Z:\{row['Informal Name']} {containing_folder}\{resource} - {row['Informal Name']}.xlsx")
        sheet_names = [x.name for x in wb.sheets]
        
        school_staff = staff_df.loc[(staff_df['School']==row['School']) & 
                                    staff_df['Role__c'].str.contains('Corps Member')].copy()
        
        wb.sheets['ACM Validation'].range('A:F').clear_contents()
        wb.sheets['ACM Validation'].range('A1').options(index=False, header=False).value = school_staff
        
        if 'Student Validation' in sheet_names:
            school_att_df = att_df.loc[att_df['School__c']==row['School']].copy()
            wb.sheets['Student Validation'].range('A:B').clear_contents()
            wb.sheets['Student Validation'].range('A1').options(index=False, header=False).value = school_att_df[['Student_Name__c', 'Student__c']]
        
        try:
            wb.save(f"Z:\{row['Informal Name']} {containing_folder}\{resource} - {row['Informal Name']}.xlsx")
        except:
            print(f"Failed to update {resource} sheets for: {row['Informal Name']}")
            pass
        
        #wb.close()
        xw.apps.active.kill()
        