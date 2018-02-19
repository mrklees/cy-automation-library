import pandas as pd
from simple_salesforce import Salesforce

with open('C:\\Users\\CLuedtke\\Desktop\\sf_credentials.txt', 'r') as f:
    read_data = f.read()
    sf_creds = eval(read_data)

sf = Salesforce(instance_url=sf_creds['instance_url'],
                password=sf_creds['password'],
                username=sf_creds['username'],
                security_token=sf_creds['security_token'])

def get_sf_df(sf_object, sf_fields):
    sf_fields_str = ", ".join(sf_fields)
    querystring = (f"SELECT {sf_fields_str} FROM {sf_object}")

    query_return = sf.query_all(querystring)

    query_list = []
    for row in query_return['records']:
        record = []
        for column in sf_fields:
            col_data = row[column]
            record.append(col_data)
        query_list.append(record)

    return pd.DataFrame(query_list, columns=sf_fields)
