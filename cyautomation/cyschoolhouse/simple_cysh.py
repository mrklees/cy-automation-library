from configparser import ConfigParser
from pathlib import Path

import pandas as pd
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
        raise ValueError(f'Could not pull a record Id in order to identify fields of object `{object_name}`.')
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

def get_section_df(sections_of_interest):
    if type(sections_of_interest)==str:
        sections_of_interest = list(sections_of_interest)

    section_df = get_object_df('Section__c', ['Id', 'Name', 'Intervention_Primary_Staff__c', 'Program__c'], rename_id=True, rename_name=True)

    program_df = get_object_df('Program__c', ['Id', 'Name'], rename_id=True, rename_name=True)

    df = section_df.merge(program_df, how='left', on='Program__c')

    df = df.loc[df['Program__c_Name'].isin(sections_of_interest)]

    return df

def get_student_section_staff_df(sections_of_interest):
    if type(sections_of_interest)==str:
        sections_of_interest = [sections_of_interest]

    # load salesforce tables
    program_df = get_object_df('Program__c', ['Id', 'Name'], where=f"Name IN ({str(sections_of_interest)[1:-1]})", rename_id=True, rename_name=True)

    student_section_df = get_object_df('Student_Section__c', [
        'Id', 'Name', 'Student_Program__c', 'Program__c', 'Section__c',
        'Active__c', 'Enrollment_End_Date__c', 'Student__c',
        'Student_Name__c', 'Dosage_to_Date__c', 'School_Reference_Id__c',
        'Student_Grade__c', 'School__c'
    ], where=f"Program__c IN ({str(program_df['Program__c'].tolist())[1:-1]})", rename_id=True, rename_name=True)

    section_df = get_object_df(
        'Section__c',
        ['Id', 'Intervention_Primary_Staff__c'],
        where=f"Program__c IN ({str(program_df['Program__c'].tolist())[1:-1]})", rename_id=True
    )
    staff_df = get_object_df('Staff__c', ['Id', 'Name'], rename_id=True, rename_name=True)

    # merge salesforce tables
    df = student_section_df.merge(section_df, how='left', on='Section__c')
    df = df.merge(staff_df, how='left', left_on='Intervention_Primary_Staff__c', right_on='Staff__c')
    df = df.merge(program_df, how='left', on='Program__c')

    df = df.loc[df['Program__c_Name'].isin(sections_of_interest)]

    return df

def get_staff_df():
    school_df = get_object_df('Account', ['Id', 'Name'])
    school_df.rename(columns={'Id':'Organization__c', 'Name':'School'}, inplace=True)

    staff_df = get_object_df(
        'Staff__c',
        ['Id', 'Individual__c', 'Name', 'First_Name_Staff__c', 'Staff_Last_Name__c', 'Role__c', 'Email__c', 'Organization__c'],
        where=f"Organization__c IN ({str(school_df['Organization__c'].tolist())[1:-1]})",
        rename_name=True, rename_id=True
    )

    staff_df = staff_df.merge(school_df, how='left', on='Organization__c')

    return staff_df

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
