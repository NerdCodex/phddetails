import pandas as pd, numpy as np

def write_excel(filename, sheet_name, data):
    df = pd.DataFrame([item.__dict__ for item in data])
    df.drop('_sa_instance_state', axis=1, errors='ignore', inplace=True)
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)


def clean_data(df):
    # Replace NaN with None (compatible with MySQL)
    return df.replace({np.nan: None})