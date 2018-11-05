import pandas as pd
from configparser import ConfigParser
from pathlib import Path
from simple_salesforce import Salesforce

def init_sf_session(sandbox=False):
    creds_path = str(Path(__file__).parent / 'credentials.ini')
    
    config = ConfigParser()
    config.read(creds_path)
    
    if sandbox==True:
        sf_creds = config['Salesforce Sandbox']
    else:
        sf_creds = config['Salesforce']

    sf = Salesforce(
        instance_url=sf_creds['instance_url'],
        password=sf_creds['password'],
        username=sf_creds['username'],
        security_token=sf_creds['security_token']
    )

    return sf

sf = init_sf_session(sandbox=False)

def get_object_fields(object_name, sf=sf):
    one_id = sf.query(f"SELECT Id FROM {object_name} LIMIT 1")['records']
    if len(one_id) > 0:
        one_id = one_id[0]['Id']
    else:
        raise ValueError(f'Could not pull a record Id in order to identify fields of object {object_name}.')
    response = getattr(sf, object_name).get(one_id)
    fields = sorted(list(response.keys()))
    fields.remove('attributes')

    return fields

def get_object_df(object_name, field_list=None, where=None, rename_id=False, rename_name=False, year=None):
    if year is None or year=='SY19':
        if field_list is None:
            field_list = get_object_fields(object_name)

        querystring = f"SELECT {', '.join(field_list)} FROM {object_name}"

        if where is not None:
            querystring += f" WHERE {where}"

        query_return = sf.query_all(querystring)

        query_list = []
        for row in query_return['records']:
            record = []
            for column in field_list:
                col_data = row[column]
                record.append(col_data)
            query_list.append(record)

        df = pd.DataFrame(query_list, columns=field_list)

    else:
        valid_years = ['SY17', 'SY18', 'SY19']
        if year not in valid_years:
            raise ValueError(f'The year provided ({year}) must be one of: {", ".join(valid_years)}.')

        df = pd.read_csv(f'Z:\\ChiPrivate\\Chicago Data and Evaluation\\Whole Site End of Year Data\\Salesforce Objects\\{year}\\{object_name}.csv')
        if field_list is not None:
            df = df[field_list]

    if rename_id==True:
        df.rename(columns={'Id':object_name}, inplace=True)
    if rename_name==True:
        df.rename(columns={'Name':(object_name+'_Name')}, inplace=True)

    return df

def section_enrollment_sync(source_section, destination_section, enrollment_start_date, ACM_to_TL=False):
    """ Syncs student enrollment across different section types

    In Chicago, we use this to ensure students enrolled in 'Tutoring: Math' or 'Tutoring: Literacy' are also enrolled in 'DESSA'
    """

    if type(source_section) != str or type(destination_section) != str:
        raise ValueError(f'source_section and destination_section must be strings.')

    program_df = get_object_df('Program__c', ['Id', 'Name'], rename_id=True, rename_name=True)

    for x in [source_section, destination_section]:
        if x not in program_df['Program__c_Name'].tolist():
            raise ValueError(f'{x} is not a valid section type.')

    student_section_df = get_object_df('Student_Section__c', ['Id', 'Student__c', 'Section__c'])
    section_df = get_object_df('Section__c', ['Id', 'Name', 'School__c', 'Program__c', 'Intervention_Primary_Staff__c'], rename_id=True, rename_name=True)

    school_df = get_object_df('Account', ['Id', 'Name'])
    school_df = school_df.rename(columns={'Id':'School__c', 'Name':'School'})

    section_df = section_df.merge(school_df, how='left', on='School__c')
    section_df = section_df.merge(program_df, how='left', on='Program__c')

    student_section_df = student_section_df.merge(section_df, how='left', on='Section__c')

    # get students enrolled in source section
    source_enrollment_df = student_section_df.loc[student_section_df['Program__c_Name'] == source_section].copy()

    # get students enrolled in destination section
    dest_enrollment_df = student_section_df.loc[student_section_df['Program__c_Name'] == destination_section].copy()

    if ACM_to_TL == True:
        source_enrollment_df.loc[:,'key'] = source_enrollment_df[['Student__c', 'School']].astype(str).sum(axis=1)
        source_enrollment_df = source_enrollment_df.drop_duplicates('key')
        dest_enrollment_df.loc[:,'key'] = dest_enrollment_df[['Student__c', 'School']].astype(str).sum(axis=1)
    else:
        source_enrollment_df.loc[:,'key'] = source_enrollment_df[['Student__c', 'Intervention_Primary_Staff__c']].astype(str).sum(axis=1)
        dest_enrollment_df.loc[:,'key'] = dest_enrollment_df[['Student__c', 'Intervention_Primary_Staff__c']].astype(str).sum(axis=1)

    # get students enrolled in source section but not destination section
    to_enroll_df = source_enrollment_df.loc[~source_enrollment_df['key'].isin(dest_enrollment_df['key'])].copy()

    # get set of destination sections
    dest_section_df = section_df.loc[section_df['Program__c_Name'] == destination_section].copy()

    # merge in section ID to enroll in
    if ACM_to_TL == True:
        to_enroll_df = to_enroll_df.merge(dest_section_df[['School__c', 'Section__c']],
                                          how='left', on='School__c', suffixes=('_from', '_to_Enroll'))
    else:
        to_enroll_df = to_enroll_df.merge(dest_section_df[['Intervention_Primary_Staff__c', 'Section__c']],
                                          how='left', on='Intervention_Primary_Staff__c', suffixes=('_from', '_to_Enroll'))

    to_enroll_df = to_enroll_df.loc[~to_enroll_df['Section__c_to_Enroll'].isnull()]

    print(f"Enrolling {len(to_enroll_df)} students from {source_section} to {destination_section} sections.")

    results = []
    for index, row in to_enroll_df.iterrows():
        result = create_student_section(student__c = row['Student__c'], section__c = row['Section__c_to_Enroll'],
                                        enrollment_start_date = enrollment_start_date)
        results.append(result)

    return results


def create_student_section(student__c, section__c, enrollment_start_date):
    stu_sect_dict = {
        'Student__c':student__c,
        'Intervention_Enrollment_Start_Date__c':enrollment_start_date,
        'Enrollment_Start_Date__c':enrollment_start_date,
        'Section__c':section__c,
    }

    result = sf.Student_Section__c.create(stu_sect_dict)

    return result

def exit_student_section(student_section_id, exit_date, exit_reason, sf=sf):
    """
    exit_date in the format YYYY-MM-DD
    exit_reason used in CHI: 'School Year ended'
    """
    result = {}
    result['student_section_id'] = student_section_id
    result['Active__c'] = sf.Student_Section__c.update(student_section_id, {'Active__c':False})
    result['Enrollment_End_Date__c'] = sf.Student_Section__c.update(student_section_id, {'Enrollment_End_Date__c':exit_date})
    result['Section_Exit_Reason__c'] = sf.Student_Section__c.update(student_section_id, {'Section_Exit_Reason__c':exit_reason})

    return result

def undo_exit_student_section(student_section_id, sf=sf):
    result = {}
    result['student_section_id'] = student_section_id
    result['Active__c'] = sf.Student_Section__c.update(student_section_id, {'Active__c':True})
    result['Enrollment_End_Date__c'] = sf.Student_Section__c.update(student_section_id, {'Enrollment_End_Date__c':None})
    result['Section_Exit_Reason__c'] = sf.Student_Section__c.update(student_section_id, {'Section_Exit_Reason__c':None})

    return result

def exit_all_student_sections(exit_date, exit_reason, sf=sf):
    """
    exit_date in the format YYYY-MM-DD
    exit_reason used: 'School Year ended'
    """
    # load student/sections object from salesforce
    student_sections_df = get_object_df(
        'Student_Section__c',
        ['Id', 'Student__c', 'Section__c', 'Active__c', 'Enrollment_End_Date__c'],
        where = "Active__c = True"
    )

    n_exits = len(student_sections_df)
    print(f"{n_exits} student/sections to exit")

    # exit student sections
    results = []
    for index, row in student_sections_df.iterrows():
        if index % 100 == 0:
            print(f"{round((index+1)/n_exits*100)}% complete")

        result = exit_student_section(student_section_id=row['Id'],
                                      exit_date=exit_date,
                                      exit_reason=exit_reason)

        results.append(result)

    return results

object_reference = [
    'Name',
    'AcceptedEventRelation',
    'Account',
    'AccountContactRole',
    'AccountHistory',
    'AccountPartner',
    'AccountShare',
    'AccountTeamMember',
    'Account_Program__c',
    'ActivityHistory',
    'AdditionalNumber',
    'AggregateResult',
    'AppMenuItem',
    'ProcessInstanceWorkitem',
    'Assesment__c',
    'Assignment__c',
    'Assignment_Lib__c',
    'AssignmentRule',
    'Assignment_Standard__c',
    'AttachedContentDocument',
    'Attachment',
    'Attendance__c',
    'AuthSession',
    'Behavior_Incident__c',
    'BusinessHours',
    'BusinessProcess',
    'CallCenter',
    'CategoryNode',
    'ClientBrowser',
    'Cohort__c',
    'Consequence__c',
    'Contact',
    'ContactHistory',
    'ContactShare',
    'ContentDocument',
    'ContentDocumentHistory',
    'ContentDocumentLink',
    'ContentVersion',
    'ContentVersionHistory',
    'Course__c',
    'Course_Catalog__c',
    'Course_Weightings__c',
    'Course_Course_Catalog__c',
    'CustomBrand',
    'CustomBrandAsset',
    'Link_Settings__c',
    'Scontrol',
    'Dashboard',
    'DashboardComponent',
    'DeclinedEventRelation',
    'Default_Assignment_Weighting__c',
    'Document',
    'DocumentAttachmentMap',
    'EmailMessage',
    'EmailStatus',
    'EmailTemplate',
    'Enrollment_Tracking__c',
    'EOY_Progress__c',
    'ErrorMessages__c',
    'Event',
    'EventRelation',
    'EventWhoRelation',
    'ExternalDataUserAuth',
    'Field_Trip__Logistics__c',
    'FiscalYearSettings',
    'Folder',
    'ForecastShare',
    'ForecastingQuota',
    'Global_Error__c',
    'Grade__c',
    'Grade_Normalization__c',
    'OverrideSettings__c',
    'Grade_Scale_Catalog__c',
    'Grade_Scale_Catalog_Scale__c',
    'Group',
    'GroupMember',
    'Account_Program__History',
    'Assignment__History',
    'Assignment_Lib__History',
    'Assignment_Standard__History',
    'Attendance__History',
    'Behavior_Incident__History',
    'Cohort__History',
    'Consequence__History',
    'Course__History',
    'Enrollment_Tracking__History',
    'EOY_Progress__History',
    'Grade__History',
    'Grade_Normalization__History',
    'Indicator_Area__History',
    'Indicator_Area_Student__History',
    'Intervention_Session__History',
    'Intervention_Session_Result__History',
    'Meals_Setup__History',
    'Notification__History',
    'Picklist_Value__History',
    'Program__History',
    'Section__History',
    'Section_Grade__History',
    'Section_ReportingPeriod__History',
    'Session__History',
    'Setup__History',
    'Staff__History',
    'Staff_Section__History',
    'Standard__History',
    'Standard_Grade__History',
    'Student__History',
    'Student_Behavior__History',
    'Student_Program__History',
    'Student_Section__History',
    'Team__History',
    'Team_Staff__History',
    'Threshold__History',
    'HoldingObj__c',
    'Holiday',
    'Idea',
    'IdeaComment',
    'Indicator_Area__c',
    'Indicator_Area_Student__c',
    'InstalledMobileApp',
    'Intervention_Session__c',
    'Intervention_Session_Result__c',
    'Interventions_Settings__c',
    'BrandTemplate',
    'LoginIp',
    'MailmergeTemplate',
    'ExternalSocialAccount',
    'Meals_Setup__c',
    'Name',
    'Network',
    'NetworkMember',
    'NetworkMemberGroup',
    'Note',
    'NoteAndAttachment',
    'CombinedAttachment',
    'Notification__c',
    'Notification_Settings__c',
    'OpenActivity',
    'Period__c',
    'Period',
    'Picklist_Value__c',
    'pictureHelper__c',
    'Points_Settings_v2__c',
    'Proactive_CS__c',
    'ProcessDefinition',
    'ProcessInstance',
    'ProcessInstanceHistory',
    'ProcessInstanceStep',
    'ProcessNode',
    'Program__c',
    'Purged_Object__c',
    'QueueSobject',
    'QuoteTemplateRichTextData',
    'RecentlyViewed',
    'TopicAssignment',
    'RecordType',
    'Report',
    'UserRole',
    'Room__c',
    'S3_Credentials_Name__c',
    'Schedule__c',
    'Schedule_Day__c',
    'Schedule_Group__c',
    'Schedule_Template__c',
    'Scheduled_Section__c',
    'SchoolForce_Settings__c',
    'Section__c',
    'Section_Grade__c',
    'Section_ReportingPeriod__c',
    'Section_Standard__c',
    'Session__c',
    'Setup__c',
    'Course__Share',
    'Course_Catalog__Share',
    'Grade_Normalization__Share',
    'Program__Share',
    'Setup__Share',
    'Staff__Share',
    'SharingControls__c',
    'Skill__c',
    'SocialPersona',
    'SocialPersonaHistory',
    'Staff__c',
    'Staff_Section__c',
    'Standard__c',
    'Standard_Grade__c',
    'Strand_Grade__c',
    'StreamingChannel',
    'StreamingChannelShare',
    'Student__c',
    'Student_Reporting_Period__c',
    'Student_Behavior__c',
    'Student_Program__c',
    'Student_Section__c',
    'Survey__c',
    'Survey_Question__c',
    'SurveyQuestionResponse__c',
    'SurveyTaker__c',
    'sevenpts__Popup_Message__c',
    'Task',
    'TaskPriority',
    'TaskRelation',
    'TaskStatus',
    'TaskWhoRelation',
    'Team__c',
    'Team_Staff__c',
    'Term__c',
    'Threshold__c',
    'Time_Element__c',
    'Topic',
    'TriggerSettings__c',
    'UndecidedEventRelation',
    'User',
    'UserAccountTeamMember',
    'UserLogin',
    'sevenpts__User_Popup_Message__c',
    'UserPreference',
    'UserProfile',
    'UserRecordAccess',
    'UserShare',
    'Value__c',
    'Vote',
    'Community'
]

object_reference.sort()
