import pandas as pd

# In this script None must be set in dictionary for null/empty values

def create_json_input(csv_path:str, id:str="id", remove:list=None, fill:str="-500"):
    # Format a test csv from Kaggle to create an input for a model deployed at Azure
    
    #test_df = pd.read_csv("../kaggle_competition_data/test.csv")
    test_df = pd.read_csv(csv_path)

    data_to_send = test_df
    """if top:
        data_to_send = test_df.head(top)"""

    idxs = list(data_to_send[id])

    if remove:
        data_to_send = data_to_send.drop(remove, axis='columns')
        
    if fill:
        data_to_send = data_to_send.fillna(fill)

    keys_lst = data_to_send.columns
    jsonlines = list()

    for row in data_to_send.iterrows():
        values_lst = list(row[1])
        values_lst = [None if value==fill else str(value) for value in values_lst]
        datapoint = {i: j for i, j in zip(keys_lst, values_lst)}
        jsonlines.append(datapoint)

    return idxs, jsonlines
