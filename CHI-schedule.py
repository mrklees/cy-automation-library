# TODOs:
# * for cysh.student.upload_all(), need to login to salesforce with 2FA
# * every week or so, need to update authentication to cyconnect server for file explorer

import schedule
import time

import cyautomation.cyschoolhouse as cysh

def m_tu_w_th_scripts():
    ## sync enrollment in DESSA sections
    result = cysh.student_section.enrollment_sync(
        source_section = 'Tutoring: Math',
        destination_section = 'DESSA',
        enrollment_start_date = '2018-09-05',
        ACM_to_TL = True
    )

    result = cysh.student_section.enrollment_sync(
        source_section = 'Tutoring: Literacy',
        destination_section = 'DESSA',
        enrollment_start_date = '2018-09-05',
        ACM_to_TL = True
    )

    ## sync enrollment in MIRI sections
    result = cysh.student_section.enrollment_sync(
        source_section = 'Tutoring: Math',
        destination_section = 'Math Inventory',
        enrollment_start_date = '2018-09-05'
    )

    result = cysh.student_section.enrollment_sync(
        source_section = 'Tutoring: Literacy',
        destination_section = 'Reading Inventory',
        enrollment_start_date = '2018-09-05'
    )

    result = cysh.student.upload_all(
        xlsx_dir = 'Z:\\ChiPrivate\\Chicago Data and Evaluation\\SY19',
        xlsx_name = 'SY19 New Students for cyschoolhouse.xlsx',
        enrollment_date='8/3/2018',
    )

    result = cysh.student.update_student_External_Id()

    return None

def monday_morn_script():
    result = cysh.tracker_mgmt.update_all_validation_sheets(
        resource_type='SY19 Coaching Log', containing_folder='Leadership Team Documents'
    )

    result = cysh.tracker_mgmt.update_all_validation_sheets(
        resource_type='SY19 Leadership Tracker', containing_folder='Leadership Team Documents'
    )

    result = cysh.tracker_mgmt.update_all_validation_sheets(
        resource_type='SY19 Attendance Tracker', containing_folder='Team Documents'
    )

    ## ToT Audit -- could be a Power BI report, but would need ACM access
    result = cysh.tot_audit.fix_T1T2ELT()
    tot_error_df = cysh.tot_audit.get_error_table()
    result = cysh.tot_audit.write_error_tables_to_cyconnect(tot_error_df)

    counts = tot_error_df.groupby(['School', 'Error'])['ACM'].count().reset_index(level='Error').rename(columns={'ACM':'Count'})
    counts.to_excel(r'Z:\Impact Analytics Team\SY19 ToT Audit Error Counts.xlsx')

    result = cysh.servicetrackers.update_service_trackers()

    return None

schedule.every().monday.at("00:00").do(
    m_tu_w_th_scripts
)

schedule.every().monday.at("00:30").do(
    monday_morn_script
)

schedule.every().tuesday.at("00:00").do(
    m_tu_w_th_scripts
)

schedule.every().wednesday.at("00:00").do(
    m_tu_w_th_scripts
)

schedule.every().thursday.at("00:00").do(
    m_tu_w_th_scripts
)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
