from simple_cysh import *

cysh = init_cysh()

def section_enrollment_sync(source_section, destination_section, enrollment_start_date, ACM_to_TL=False):
    """ I'm going to document, I promise.
    """
    
    program_df = get_cysh_df('Program__c', ['Id', 'Name'], rename_id=True, rename_name=True)
    
    if type(source_section) != str or type(destination_section) != str:
        raise ValueError(f'source_section and destination_section must be strings.')
    
    for x in [source_section, destination_section]:
        if x not in program_df['Program__c_Name'].tolist():
            raise ValueError(f'{x} is not a valid section type.')
    
    student_section_df = get_cysh_df('Student_Section__c', ['Id', 'Student__c', 'Section__c'])
    section_df = get_cysh_df('Section__c', ['Id', 'Name', 'School__c', 'Program__c', 'Intervention_Primary_Staff__c'], rename_id=True, rename_name=True)
    
    school_df = get_cysh_df('Account', ['Id', 'Name'])
    school_df = school_df.rename(columns={'Id':'School__c', 'Name':'School'})
    
    section_df = section_df.merge(school_df, how='left', on='School__c')
    section_df = section_df.merge(program_df, how='left', on='Program__c')
    
    student_section_df = student_section_df.merge(section_df, how='left', on='Section__c')
    
    # get students enrolled in source section
    source_enrollment_df = student_section_df.loc[student_section_df['Program__c_Name'] == source_section]
    
    # get students enrolled in destination section
    dest_enrollment_df = student_section_df.loc[student_section_df['Program__c_Name'] == destination_section]
    
    if ACM_to_TL == True:
        source_enrollment_df['key'] = source_enrollment_df[['Student__c', 'School']].astype(str).sum(axis=1)
        source_enrollment_df = source_enrollment_df.drop_duplicates('key')
        dest_enrollment_df['key'] = dest_enrollment_df[['Student__c', 'School']].astype(str).sum(axis=1)
    else:
        source_enrollment_df['key'] = source_enrollment_df[['Student__c', 'Intervention_Primary_Staff__c']].astype(str).sum(axis=1)
        dest_enrollment_df['key'] = dest_enrollment_df[['Student__c', 'Intervention_Primary_Staff__c']].astype(str).sum(axis=1)
    
    # get students enrolled in source section but not destination section
    to_enroll_df = source_enrollment_df.loc[~source_enrollment_df['key'].isin(dest_enrollment_df['key'])]
    
    # get set of destination sections
    dest_section_df = section_df.loc[section_df['Program__c_Name'] == destination_section]
    
    # merge in section ID to enroll in
    if ACM_to_TL == True:
        to_enroll_df = to_enroll_df.merge(dest_section_df[['School__c', 'Section__c']], 
                                          how='left', on='School__c', suffixes=('_from', '_to_Enroll'))
    else:
        to_enroll_df = to_enroll_df.merge(dest_section_df[['Intervention_Primary_Staff__c', 'Section__c']], 
                                          how='left', on='Intervention_Primary_Staff__c', suffixes=('_from', '_to_Enroll'))
    
    to_enroll_df = to_enroll_df.loc[~to_enroll_df['Section__c_to_Enroll'].isnull()]
    
    print(f"Enrolling {len(to_enroll_df)} students to {destination_section} sections.")
    
    results = []
    for index, row in to_enroll_df.iterrows():
        stu_sect_dict = {
            'Student__c':row['Student__c'],
            'Intervention_Enrollment_Start_Date__c':enrollment_start_date,
            'Enrollment_Start_Date__c':enrollment_start_date,
            'Section__c':row['Section__c_to_Enroll'],
        }
    
        result = cysh.Student_Section__c.create(stu_sect_dict)
        results.append(result)
    
    return results
