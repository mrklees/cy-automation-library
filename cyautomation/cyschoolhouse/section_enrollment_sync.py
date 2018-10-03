from simple_cysh import *

cysh = init_cysh()

def section_enrollment_sync(source_section, destination_section, enrollment_start_date):
    """ 
    This implementation assumes there is only one destination section per school. In Chicago,
    we use one 'Homework Assistance' and one 'DESSA' section per school (assigned to the TL)
    in order to track enrollment.
    """
    
    program_df = get_cysh_df('Program__c', ['Id', 'Name'], rename_id=True, rename_name=True)

    if type(source_section) == str:
        source_section = [source_section]
    if type(destination_section) == str:
        destination_section = [destination_section]

    for x in source_section + destination_section:
        if x not in program_df['Program__c_Name'].tolist():
            raise ValueError(f'{x} is not a valid section type.')

    student_section_df = get_cysh_df('Student_Section__c', ['Id', 'Student__c', 'Section__c'])
    section_df = get_cysh_df('Section__c', ['Id', 'Name', 'School__c', 'Program__c'], rename_id=True, rename_name=True)
    
    school_df = get_cysh_df('Account', ['Id', 'Name'])
    school_df.rename(columns={'Id':'School__c', 'Name':'School'}, inplace=True)
    
    section_df = section_df.merge(school_df, how='left', on='School__c')
    section_df = section_df.merge(program_df, how='left', on='Program__c')
    
    student_section_df = student_section_df.merge(section_df, how='left', on='Section__c')
    student_section_df['key'] = student_section_df[['Student__c', 'School']].astype(str).sum(axis=1)

    # get unique students enrolled in source sections
    source_enrollment_df = student_section_df.loc[student_section_df['Program__c_Name'].isin(source_section)]
    source_enrollment_df = source_enrollment_df[['key', 'Student__c', 'School']].drop_duplicates()

    # get unique students enrolled in destination sections
    dest_enrollment_df = student_section_df.loc[student_section_df['Program__c_Name'].isin(destination_section)]

    # get students enrolled in source section but not destination section
    to_enroll_df = source_enrollment_df.loc[~source_enrollment_df['key'].isin(dest_enrollment_df['key'])]

    # get set of destination sections
    dest_section_df = section_df.loc[section_df['Program__c_Name'].isin(destination_section)]
    
    results = []
    for index, row in to_enroll_df.iterrows():
        stu_sect_dict = {
            'Student__c':row['Student__c'],
            'Intervention_Enrollment_Start_Date__c':enrollment_start_date,
            'Enrollment_Start_Date__c':enrollment_start_date,
            'Section__c':dest_section_df.loc[dest_section_df['School']==row['School'], 'Section__c'].values[0],
        }
    
        result = cysh.Student_Section__c.create(stu_sect_dict)
        results.append(result)
    
    return results

if __name__ == "__main__":
    results = section_enrollment_sync(
        source_section=['Tutoring: Math', 'Tutoring: Literacy'],
        destination_section='DESSA',
        enrollment_start_date = '2018-09-05',
    )
