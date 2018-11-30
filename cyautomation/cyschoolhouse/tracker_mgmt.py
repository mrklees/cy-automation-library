import os

import pandas as pd
import xlwings as xw

from . import simple_cysh as cysh
    

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
            wb = xw.Book(f"Z:\\{row['Informal Name']} Leadership Team Documents\\SY19 Coaching Log - {row['Informal Name']}.xlsx")
            fill_one_coaching_log_acm_rollup(wb)
            wb.save(f"Z:\\{row['Informal Name']} Leadership Team Documents\\SY19 Coaching Log - {row['Informal Name']}.xlsx")
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
    """ Multiply by Schools
    """
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
            wb.save(f"Z:\\{row['Informal Name']} Leadership Team Documents\\SY19 Coaching Log - {row['Informal Name']}.xlsx")
            #wb.save(f"Z:\ChiPrivate\Chicago Data and Evaluation\SY19\Tests\SY19 Coaching Log - {row['Informal Name']}.xlsx")
        except:
            print(f"Save failed {row['Informal Name']}")
            pass

        # Reset Sheets
        pos = 0
        for sheet_name in sheets_added:
            pos += 1
            wb.sheets[sheet_name].name = f'ACM{pos}'

def deploy_tracker(resource_type, containing_folder, school_ref_path = r'Z:\\ChiPrivate\\Chicago Data and Evaluation\\SY19\\SY19 School Reference.xlsx'):
    """ Distributes Excel tracker template to school team folders

    resource_type like 'SY19 Attendance Tracker' or 'SY19 Leadership Tracker'
    containing_folder like 'Team Documents' or 'Leadership Team Documents'
    """
    template_path = f'Z:\\ChiPrivate\\Chicago Data and Evaluation\\SY19\\Templates\\{resource_type} Template.xlsx'
    wb = xw.Book(template_path)

    school_ref_df = pd.read_excel(school_ref_path)

    for index, row in school_ref_df.iterrows():
        wb.sheets['Tracker'].range('A1').clear_contents()
        wb.sheets['Tracker'].range('A1').value = f"{resource_type} - {row['Informal Name']}"

        try:
            wb.save(f"Z:\\{row['Informal Name']} {containing_folder}\\{resource_type} - {row['Informal Name']}.xlsx")
        except:
            print(f"Save failed {row['Informal Name']}")
            pass

    wb.close()

def unprotect_ACM_validation_sheet(resource_type, containing_folder, school_ref_path = 'Z:\\ChiPrivate\\Chicago Data and Evaluation\\SY19\\SY19 School Reference.xlsx'):
    import win32com.client
    import pandas as pd

    xcl = win32com.client.Dispatch('Excel.Application')
    xcl.visible = True
    xcl.DisplayAlerts = False

    school_ref_df = pd.read_excel(school_ref_path)

    for index, row in school_ref_df.iterrows():
        wb = xcl.workbooks.open(f"Z:\\{row['Informal Name']} {containing_folder}\\{resource_type} - {row['Informal Name']}.xlsx")
        wb.Sheets('ACM Validation').Unprotect()
        wb.Close(True, xlsx_path)

    xcl.Quit()

def update_all_validation_sheets(resource_type, containing_folder, school_ref_path = 'Z:\\ChiPrivate\\Chicago Data and Evaluation\\SY19\\SY19 School Reference.xlsx'):
    school_ref_df = pd.read_excel(school_ref_path)

    staff_df = cysh.get_staff_df()
    staff_df['First_Name_Staff__c'] = staff_df['First_Name_Staff__c'] + " " + staff_df['Staff_Last_Name__c'].astype(str).str[0] + "."
    staff_df.sort_values('First_Name_Staff__c', inplace=True)
    staff_df = staff_df.loc[staff_df['Role__c'].str.contains('Corps Member|Team Leader') == True]

    if 'Attendance' in resource_type:
        att_df = cysh.get_student_section_staff_df(sections_of_interest='Coaching: Attendance')
        att_df.sort_values('Student_Name__c', inplace=True)

    for index, row in school_ref_df.iterrows():
        wb = xw.Book(f"Z:\\{row['Informal Name']} {containing_folder}\\{resource_type} - {row['Informal Name']}.xlsx")
        sheet_names = [x.name for x in wb.sheets]

        school_staff = staff_df.loc[staff_df['School'] == row['School']].copy()

        wb.sheets['ACM Validation'].clear_contents()
        wb.sheets['ACM Validation'].range('A1').options(index=False, header=False).value = school_staff[[
            'Individual__c', 'First_Name_Staff__c', 'Staff__c_Name'
        ]]

        if 'Student Validation' in sheet_names and 'Attendance' in resource_type:
            school_att_df = att_df.loc[att_df['School__c']==row['School']].copy()
            wb.sheets['Student Validation'].clear_contents()
            wb.sheets['Student Validation'].range('A1').options(index=False, header=False).value = school_att_df[[
                'Student_Name__c', 'Student__c'
            ]]

        try:
            wb.save(f"Z:\\{row['Informal Name']} {containing_folder}\\{resource_type} - {row['Informal Name']}.xlsx")
        except:
            print(f"Failed to update {resource_type} sheets for: {row['Informal Name']}")
            pass

        #wb.close()
        xw.apps.active.kill()
