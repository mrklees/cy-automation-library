from . import simple_cysh as cysh

## Demo of how to pull student object
#school_df = cysh.get_object_df('Account', ['Id', 'Name'])
#student_df = cysh.get_object_df('Student__c', ['Id', 'Name', 'Local_Student_ID__c', 'School__c', 'External_Id__c'], where=f"School__c IN ({str(school_df['Id'].tolist())[1:-1]})")
#
#df = cysh.get_object_df('Student_Program__c')

def enrollment_sync(source_section, destination_section, enrollment_start_date, ACM_to_TL=False):
    """ Syncs student enrollment across different section types

    In Chicago, we use this to ensure students enrolled in 'Tutoring: Math' or 'Tutoring: Literacy' are also enrolled in 'DESSA'
    """

    if type(source_section) != str or type(destination_section) != str:
        raise ValueError(f'source_section and destination_section must be strings.')

    program_df = cysh.get_object_df('Program__c', ['Id', 'Name'], rename_id=True, rename_name=True)

    for x in [source_section, destination_section]:
        if x not in program_df['Program__c_Name'].tolist():
            raise ValueError(f'{x} is not a valid section type.')

    student_section_df = cysh.get_object_df('Student_Section__c', ['Id', 'Student__c', 'Section__c'])
    section_df = cysh.get_object_df('Section__c', ['Id', 'Name', 'School__c', 'Program__c', 'Intervention_Primary_Staff__c'], rename_id=True, rename_name=True)

    school_df = cysh.get_object_df('Account', ['Id', 'Name'])
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
        result = create_one(student__c = row['Student__c'], section__c = row['Section__c_to_Enroll'],
                            enrollment_start_date = enrollment_start_date)
        results.append(result)

    return results


def create_one(student__c, section__c, enrollment_start_date, sf=cysh.sf):
    stu_sect_dict = {
        'Student__c':student__c,
        'Intervention_Enrollment_Start_Date__c':enrollment_start_date,
        'Enrollment_Start_Date__c':enrollment_start_date,
        'Section__c':section__c,
    }

    result = sf.Student_Section__c.create(stu_sect_dict)

    return result

def exit_one(student_section_id, exit_date, exit_reason, sf=cysh.sf):
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

def undo_exit_one(student_section_id, sf=cysh.sf):
    result = {}
    result['student_section_id'] = student_section_id
    result['Active__c'] = sf.Student_Section__c.update(student_section_id, {'Active__c':True})
    result['Enrollment_End_Date__c'] = sf.Student_Section__c.update(student_section_id, {'Enrollment_End_Date__c':None})
    result['Section_Exit_Reason__c'] = sf.Student_Section__c.update(student_section_id, {'Section_Exit_Reason__c':None})

    return result

def exit_all(exit_date, exit_reason, sf=cysh.sf):
    """
    exit_date in the format YYYY-MM-DD
    exit_reason used: 'School Year ended'
    """
    # load student/sections object from salesforce
    student_sections_df = cysh.get_object_df(
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

        result = exit_one(student_section_id=row['Id'],
                          exit_date=exit_date,
                          exit_reason=exit_reason)

        results.append(result)

    return results
