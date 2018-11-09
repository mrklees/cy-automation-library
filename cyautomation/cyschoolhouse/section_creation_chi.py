import pandas as pd

import simple_cysh as cysh

def academic_sections_to_create():
    """
    Gather ACM deployment docs to determine which 'Tutoring: Math' and 'Tutoring: Literacy' sections to make
    """
    xl = pd.ExcelFile(r'Z:\Impact Analytics Team\SY19 ACM Deployment.xlsx')

    df_list = []
    for sheet in xl.sheet_names:
        if sheet != 'Sample Deployment':
            df = xl.parse(sheet).iloc[:,0:6]
            df['Informal School Name'] = sheet
            df_list.append(df)
            del df
    acm_dep_df = pd.concat(df_list)

    acm_dep_df.rename(columns={
        'ACM Name':'ACM',
        'Related IA (ELA/Math)':'SectionName'
    }, inplace=True)

    acm_dep_df = acm_dep_df

    acm_dep_df = acm_dep_df.loc[~acm_dep_df['ACM'].isnull() & ~acm_dep_df['SectionName'].isnull()]

    acm_dep_df['ACM'] = acm_dep_df['ACM'].str.strip()
    acm_dep_df['SectionName'] = acm_dep_df['SectionName'].str.strip().str.upper()

    acm_dep_df.loc[acm_dep_df['SectionName'].str.contains('MATH'), 'SectionName_MATH'] = 'Tutoring: Math'
    acm_dep_df.loc[acm_dep_df['SectionName'].str.contains('ELA'), 'SectionName_ELA'] = 'Tutoring: Literacy'

    acm_dep_df.loc[~acm_dep_df['SectionName'].str.contains('MATH|ELA')]

    acm_dep_df = acm_dep_df.fillna('')

    acm_dep_df = acm_dep_df[['ACM', 'Informal School Name', 'SectionName_MATH', 'SectionName_ELA']].groupby(['ACM', 'Informal School Name']).agg(lambda x: ''.join(x.unique()))
    acm_dep_df.reset_index(inplace=True)

    acm_dep_df = pd.melt(acm_dep_df, id_vars=['ACM', 'Informal School Name'], value_vars=['SectionName_MATH', 'SectionName_ELA'])
    acm_dep_df = acm_dep_df.loc[~acm_dep_df['value'].isnull() & (acm_dep_df['value'] != '')]
    acm_dep_df = acm_dep_df.sort_values('ACM')
    
    return acm_dep_df

def non_CP_sections_to_create(sections_of_interest=['Coaching: Attendance', 'SEL Check In Check Out']):
    """
    Produce table of sections to create, with the assumption that all 'Corps Member' roles should have 1 of each section.
    """
    program_df = cysh.get_object_df('Program__c', ['Id', 'Name'], rename_id=True, rename_name=True)

    school_df = cysh.get_object_df('Account', ['Id', 'Name'])
    school_df.rename(columns={'Id':'School__c', 'Name':'School'}, inplace=True)

    staff_df = cysh.get_object_df('Staff__c', ['Id', 'Name', 'Role__c', 'Organization__c'], where="Site__c='Chicago'", rename_name=True)
    staff_df = staff_df.merge(school_df, how='left', left_on='Organization__c', right_on='School__c')

    section_df = cysh.get_object_df('Section__c', ['Id', 'Name', 'Intervention_Primary_Staff__c', 'Program__c'], rename_id=True, rename_name=True)
    section_df = section_df.merge(program_df, how='left', on='Program__c')
    section_df = section_df.merge(staff_df, how='left', left_on='Intervention_Primary_Staff__c', right_on='Id')

    section_df['key'] = section_df['Intervention_Primary_Staff__c'] + section_df['Program__c_Name']

    acm_df = staff_df.loc[staff_df['Role__c'].str.contains('Corps Member')==True].copy()

    section_deployment = pd.DataFrame.from_dict({'SectionName': sections_of_interest})
    section_deployment['key'] = 1

    acm_df['key'] = 1

    acm_df = acm_df.merge(section_deployment, on='key')
    acm_df['key'] = acm_df['Id'] + acm_df['SectionName']

    acm_df = acm_df.loc[~acm_df['key'].isin(section_df['key'])]

    acm_df.rename(columns={'Staff__c_Name':'ACM'}, inplace=True)

    acm_df = acm_df[['School', 'ACM', 'SectionName']]
    acm_df['In_School_or_Extended_Learning'] = 'In School'
    acm_df['Start_Date'] = '09/04/2018'
    acm_df['End_Date'] = '06/07/2019'
    acm_df['Target_Dosage'] = 0

    return acm_df

def MIRI_sections_to_create():
    """
    Produce table of ACM 'Math Inventory' and 'Rreading Inventory' sections to make
    """
    program_df = cysh.get_object_df('Program__c', ['Id', 'Name'], rename_id=True, rename_name=True)

    school_df = cysh.get_object_df('Account', ['Id', 'Name'])
    school_df.rename(columns={'Id':'School__c', 'Name':'School'}, inplace=True)

    staff_df = cysh.get_object_df('Staff__c', ['Id', 'Name'], where="Site__c='Chicago'", rename_name=True)

    section_df = cysh.get_object_df('Section__c', ['Id', 'Name', 'Intervention_Primary_Staff__c', 'School__c', 'Program__c'], rename_id=True, rename_name=True)
    section_df = section_df.merge(school_df, how='left', on='School__c')
    section_df = section_df.merge(program_df, how='left', on='Program__c')
    section_df = section_df.merge(staff_df, how='left', left_on='Intervention_Primary_Staff__c', right_on='Id')

    highschools = [
        'Tilden Career Community Academy High School',
        'Gage Park High School',
        'Collins Academy High School',
        'Schurz High School',
        'Sullivan High School',
        'Chicago Academy High School',
        'Roberto Clemente Community Academy',
        'Wendell Phillips Academy',
    ]

    section_df = section_df.loc[section_df['School'].isin(highschools)]

    miri_section_df = section_df.loc[section_df['Program__c_Name'].str.contains('Inventory')]
    section_df = section_df.loc[section_df['Program__c_Name'].str.contains('Tutoring')]

    section_df['Program__c_Name'] = section_df['Program__c_Name'].map({
        'Tutoring: Literacy':'Reading Inventory', 
        'Tutoring: Math':'Math Inventory'
    })

    for df in [section_df, miri_section_df]:
        df['key'] = df['Staff__c_Name'] + df['Program__c_Name']

    section_df = section_df.loc[~section_df['key'].isin(miri_section_df['key'])]

    section_df.rename(columns={'Staff__c_Name':'ACM', 'Program__c_Name':'SectionName'}, inplace=True)
    section_df['In_School_or_Extended_Learning'] = 'In School'
    section_df['Start_Date'] = '09/04/2018'
    section_df['End_Date'] = '06/07/2019'
    section_df['Target_Dosage'] = 0

    section_df = section_df[['School', 'ACM', 'SectionName', 'In_School_or_Extended_Learning', 'Start_Date', 'End_Date', 'Target_Dosage']]

    return section_df

def deactivate_all_sections(section_type='50 Acts'):
    """
    This is necessary due to a bug in section creation. When section creation fails,
    sometimes a 50 Acts section is made, since it's the default section type selection.
    We don't provide 50 Act programming in Chicago, so we can safely deactivate all.
    """
    # De-activate 50 Acts sections
    section_df = cysh.get_object_df('Section__c', ['Id', 'Name', 'Intervention_Primary_Staff__c', 'School__c', 'Program__c', 'Active__c'], rename_id=True, rename_name=True)
    program_df = cysh.get_object_df('Program__c', ['Id', 'Name'], rename_id=True, rename_name=True)
    
    df = section_df.merge(program_df, how='left', on='Program__c')

    sections_to_delete = df.loc[
        (df['Program__c_Name']==section_type) & 
        (section_df['Active__c']==True), 
        'Section__c'
    ]

    print(f"{len(sections_to_delete)} '50 Acts' sections to de-activate.")

    for section_id in sections_to_delete:
        cysh.sf.Section__c.update(section_id, {'Active__c':False})