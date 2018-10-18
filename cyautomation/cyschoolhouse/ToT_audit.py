import os
from simple_cysh import *
from StyleFrame import StyleFrame, Styler, utils

def fix_t1t2_entries():
    """ Standardize common spellings of "T1" and "T2"
    """
    
    t1t2_fixes = {
        't1': 'T1',
        'Tier 1': 'T1', 'Tier1': 'T1', 'tier 1': 'T1', 'tier1': 'T1',
        'Teir 1': 'T1', 'Teir1': 'T1', 'teir 1': 'T1', 'teir1': 'T1',
        't2': 'T2',
        'Tier 2': 'T2', 'Tier2': 'T2', 'tier 2': 'T2', 'tier2': 'T2',
        'Teir 2': 'T2', 'Teir2': 'T2', 'teir 2': 'T2', 'teir2': 'T2',
    }
    
    df = get_cysh_df('Intervention_Session__c', ['Id', 'Comments__c'], rename_id=True)
    
    df = df.loc[(df['Comments__c'].str.contains('|'.join(list(t1t2_fixes.keys())))==True)]
    
    df['Comments__c'].replace(t1t2_fixes, inplace=True, regex=True)
    
    print(f"Found {len(df)} T1/T2 labels that can be fixed")
    
    results = []
    for index, row in df.iterrows():
        result = cysh.Intervention_Session__c.update(row['Intervention_Session__c'], {'Comments__c':row['Comments__c']})
        results.append(results)
    
    return results

def get_ToT_error_table():
    ISR_df = get_cysh_df('Intervention_Session_Result__c', ['Amount_of_Time__c', 'IsDeleted', 'Intervention_Session_Date__c', 'Related_Student_s_Name__c', 'Intervention_Session__c'])
    IS_df = get_cysh_df('Intervention_Session__c', ['Id', 'Name', 'Comments__c', 'Section__c'], rename_id=True, rename_name=True)
    section_df = get_cysh_df('Section__c', ['Id', 'School__c', 'Intervention_Primary_Staff__c', 'Program__c'], rename_id=True)

    school_df = get_cysh_df('Account', ['Id', 'Name'])
    school_df.rename(columns={'Id':'School__c', 'Name':'School_Name__c'}, inplace=True)

    staff_df = get_cysh_df('Staff__c', ['Id', 'Name'], where="Site__c = 'Chicago'", rename_id=True, rename_name=True)

    program_df = get_cysh_df('Program__c', ['Id', 'Name'], rename_id=True, rename_name=True)

    df = ISR_df.merge(IS_df, how='left', on='Intervention_Session__c'); del df['Intervention_Session__c']
    df = df.merge(section_df, how='left', on='Section__c'); del df['Section__c']
    df = df.merge(school_df, how='left', on='School__c'); del df['School__c']
    df = df.merge(staff_df, how='left', left_on='Intervention_Primary_Staff__c', right_on='Staff__c'); del df['Intervention_Primary_Staff__c'], df['Staff__c']
    df = df.merge(program_df, how='left', on='Program__c'); del df['Program__c']

    df.loc[df['Program__c_Name'].str.contains('Tutoring')
           & (df['Comments__c'].str.contains('T1|T2') != True), 'Missing T1/T2 Code'] = 'Missing T1/T2 Code'

    df.loc[df['Program__c_Name'].str.contains('Tutoring|SEL')
           & (df['Amount_of_Time__c'] < 10), '<10 Minutes'] = '<10 Minutes'

    df.loc[df['Program__c_Name'].str.contains('Tutoring')
           & (df['Amount_of_Time__c'] > 120), '>120 Minutes'] = '>120 Minutes'

    df['Comments__c'].fillna('', inplace=True)
    
    df['Error'] = df[['Missing T1/T2 Code', '<10 Minutes', '>120 Minutes']].apply(lambda x: x.str.cat(sep=' & '), axis=1)

    df = df.loc[df['Error'] != '']
    
    col_friendly_names = {
        'School_Name__c':'School',
        'Staff__c_Name':'ACM',
        'Intervention_Session__c_Name':'Session ID',
        'Related_Student_s_Name__c':'Student',
        'Intervention_Session_Date__c':'Date',
        'Amount_of_Time__c':'ToT',
        #'Comments__c':'Comment',
        'Error':'Error',
    }
    
    df = df.rename(columns=col_friendly_names)
    df = df.sort_values(list(col_friendly_names.values()))
    df = df[list(col_friendly_names.values())]
    
    return df

def write_tot_error_tables_to_cyconnect(df):
    sch_ref_df = pd.read_excel(r'Z:\ChiPrivate\Chicago Data and Evaluation\SY19\SY19 School Reference.xlsx')

    for index, row in sch_ref_df.iterrows():
        print(row['School'])
        school_error_df = df.loc[df['School']==row['School']].copy()
        del school_error_df['School']

        write_path = f"Z:\\{row['Informal Name']} Team Documents\\SY19 ToT Audit Errors - {row['Informal Name']}.xlsx"
        
        if os.path.exists(write_path):
            os.remove(write_path)
        
        excel_writer = StyleFrame.ExcelWriter(write_path)
        sf = StyleFrame(school_error_df)
        sf.apply_column_style(
            cols_to_style=list(school_error_df), 
            styler_obj=Styler(
                horizontal_alignment=utils.horizontal_alignments.left,
                #vertical_alignment=utils.vertical_alignments.top
            ),
            width=25,
            style_header=False,
        )
        
        if len(school_error_df) > 0:
            freeze = 'A2'
        else:
            freeze = 'A1'
            
        sf.to_excel(
            excel_writer=excel_writer, 
            row_to_add_filters=0,
            columns_and_rows_to_freeze=freeze,
        )
        excel_writer.save()