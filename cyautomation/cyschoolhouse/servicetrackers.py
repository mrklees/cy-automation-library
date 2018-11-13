from pathlib import Path

import pandas as pd
from PyPDF2 import PdfFileMerger
import xlwings as xw

from . import simple_cysh as cysh

def get_section_enrollment_table(sections_of_interest):
    df = cysh.get_student_section_staff_df(sections_of_interest)

    # group by Student_Program__c, then sum ToT
    df = df.join(df.groupby('Student_Program__c')['Dosage_to_Date__c'].sum(), how='left', on='Student_Program__c', rsuffix='_r')

    # filter out inactive students
    df = df.loc[(df['Active__c']==True) & df['Enrollment_End_Date__c'].isnull()]

    # clean program names and set zeros
    df['Program__c_Name'] = df['Program__c_Name'].replace({'Tutoring: Math':'Math', 'Tutoring: Literacy':'ELA'})
    df['Dosage_to_Date__c_r'] = df['Dosage_to_Date__c_r'].fillna(value=0).astype(int)

    df['Dosage_to_Write'] = df['Dosage_to_Date__c_r'].astype(str) + "\r\n" + df['Program__c_Name']

    df.sort_values(by=[
        'School_Reference_Id__c', 'Staff__c_Name',
        'Program__c_Name', 'Student_Grade__c',
        'Student_Name__c',
    ], inplace = True)

    df = df[['School_Reference_Id__c', 'Staff__c_Name', 'Program__c_Name', 'Student_Name__c', 'Dosage_to_Write']]

    return df

def fill_and_save_one_acm_pdf(acm_df, acm_name, main_sht, header_sht, CP_sht, SEL_sht, att_sht, logf):
    # Write header
    header_sht.range('A1').options(index=False, header=False).value = acm_name

    # Write Course Performance
    df_acm_CP = acm_df.loc[acm_df['Program__c_Name'].isin(['Math', 'ELA'])].copy()
    if len(df_acm_CP) > 12:
        logf.write(f"Warning: More than 12 Math/ELA students for {acm_name}\n")
    CP_sht.range('B4:C15').clear_contents()
    CP_sht.range('B4').options(index=False, header=False).value = df_acm_CP[['Student_Name__c', 'Dosage_to_Write']][0:12]

    # Write SEL
    df_acm_SEL = acm_df.loc[acm_df['Program__c_Name'].str.contains("SEL")].copy()
    if len(df_acm_SEL) > 6:
        logf.write(f"Warning: More than 6 SEL students for {acm_name}\n")
    SEL_sht.range('B5:B10').clear_contents()
    SEL_sht.range('B5').options(index=False, header=False).value = df_acm_SEL['Student_Name__c'][0:6]

    # Write Attendance
    df_acm_attendance = acm_df.loc[acm_df['Program__c_Name'].str.contains("Attendance")].copy()
    att_sht.range('B4:B6, F4:F6').clear_contents()
    if len(df_acm_attendance['Student_Name__c']) > 6:
        logf.write(f"Warning: More than 6 Attendance students for {acm_name}\n")
    att_sht.range('B4').options(index=False, header=False).value = df_acm_attendance['Student_Name__c'][0:3]
    att_sht.range('F4').options(index=False, header=False).value = df_acm_attendance['Student_Name__c'][3:6]

    main_sht.api.ExportAsFixedFormat(0, str(Path(__file__).parent / 'temp' / f"{acm_name}.pdf"))

def merge_and_save_one_school_pdf(school_informal_name):
    # Merge team PDFs
    temp_files = []
    merger = PdfFileMerger()
    for filepath in (Path(__file__).parent / 'temp').iterdir():
        if '.pdf' in str(filepath):
            merger.append(str(filepath))
            temp_files.append(filepath)

    # Edit this write path to match your Sharepoint file structure
    merger.write(f"Z:\\{school_informal_name} Team Documents\\SY19 Weekly Service Trackers - {school_informal_name}.pdf")
    merger.close()

    # remove local data
    for filepath in temp_files:
        filepath.unlink()

def update_service_trackers(sch_ref_df_path='Z:\\ChiPrivate\\Chicago Data and Evaluation\\SY19\\SY19 School Reference.xlsx', start_row=0):
    """ Runs the entire Service Tracker publishing process
    """
    logf = open(Path(__file__).parent / 'log' / 'Service Tracker Log.log', "w")

    sch_ref_df = pd.read_excel(sch_ref_df_path)

    student_section_df = get_section_enrollment_table(
        sections_of_interest= [
            'Coaching: Attendance',
            'SEL Check In Check Out',
            'Tutoring: Literacy',
            'Tutoring: Math',
        ]
    )

    # Open Excel Template and define sheet references
    xlsx_path = Path(__file__).parent / 'templates' / 'Service Tracker Template.xlsx'
    wb = xw.Book(str(xlsx_path))

    main_sht = wb.sheets['Service Tracker']
    header_sht = wb.sheets['Header']
    CP_sht = wb.sheets['Course Performance']
    SEL_sht = wb.sheets['SEL']
    att_sht = wb.sheets['Attendance CICO']

    for filepath in (Path(__file__).parent / 'temp').iterdir():
        filepath.unlink()

    # Iterate through school names to build Service Tracker PDFs
    for school in student_section_df['School_Reference_Id__c'].unique()[start_row:]:
        logf.write(f"Writing Service Tracker: {school}\n")
        print(f"Writing Service Tracker: {school}\n")

        df_school = student_section_df.loc[student_section_df['School_Reference_Id__c'] == school].copy()

        for acm_name in df_school['Staff__c_Name'].unique():
            acm_df = df_school.loc[df_school['Staff__c_Name'] == acm_name].copy()

            try:
                fill_and_save_one_acm_pdf(acm_df, acm_name, main_sht, header_sht, CP_sht, SEL_sht, att_sht, logf)
            except Exception as e:
                logf.write(f"Error filling template or saving pdf for {acm_name}: {e}\n")
                print(f"Error filling template or saving pdf for {acm_name}: {e}\n")
                pass

        # Look up school's informal name
        school_informal_name = sch_ref_df.loc[sch_ref_df['School'] == school, 'Informal Name'].values[0]

        merge_and_save_one_school_pdf(school_informal_name)

    wb.close()

    logf.write("Completed script 'Weekly Service Tracker Update'\n")
    logf.close()
