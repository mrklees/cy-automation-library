import pandas as pd
from simple_salesforce import Salesforce

def init_cysh():
    with open('C:\\Users\\City_Year\\Desktop\\salesforce_credentials.txt', 'r') as f:
        read_data = f.read()
        sf_creds = eval(read_data)
        
    cysh = Salesforce(instance_url=sf_creds['instance_url'],
                      password=sf_creds['password'],
                      username=sf_creds['username'],
                      security_token=sf_creds['security_token'])
    
    return cysh

def get_cysh_df(sf_object, sf_fields, where=None, rename_id=False, rename_name=False):
    if type(sf_fields) == str and sf_fields.lower() == 'all':
        sf_fields = get_cysh_fields(sf_object)
    else:
        sf_fields_str = ", ".join(sf_fields)
    if where==None:
        querystring = (f"SELECT {sf_fields_str} FROM {sf_object}")
    else:
        querystring = (f"SELECT {sf_fields_str} FROM {sf_object} WHERE {where}")
        
    query_return = cysh.query_all(querystring)
    query_list = []
    for row in query_return['records']:
        record = []
        for column in sf_fields:
            col_data = row[column]
            record.append(col_data)
        query_list.append(record)
    
    df = pd.DataFrame(query_list, columns=sf_fields)
    
    if rename_id==True:
        df.rename(columns={'Id':sf_object}, inplace=True)
    if rename_name==True:
        df.rename(columns={'Name':(sf_object+'_Name')}, inplace=True)
    
    return df

def get_cysh_fields(sf_object):
    one_id = cysh.query(f"SELECT Id FROM {sf_object} LIMIT 1")['records'][0]['Id']
    response = getattr(cysh, sf_object).get(one_id)
    fields = sorted(list(response.keys()))
    fields.remove('attributes')
    
    return fields

cysh = init_cysh()