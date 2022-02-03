## Downloaded from Microsoft

import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

##############
## Added by FM
import pandas as pd

# In this script None must be set in dictionary for null/empty values

test_df = pd.read_csv("../kaggle_competition_data/test.csv")

#data_to_send = test_df.head(2)
#data_to_send = test_df[30:50]
data_to_send = test_df

idxs = list(data_to_send.id)

data_to_send = data_to_send.drop(['id'], axis='columns').fillna(-500)

keys_lst = data_to_send.columns
jsonlines = list()

for row in data_to_send.iterrows():
    values_lst = list(row[1])
    values_lst = [None if value==-500 else str(value) for value in values_lst]
    datapoint = {i: j for i, j in zip(keys_lst, values_lst)}
    jsonlines.append(datapoint)


"""for each in jsonlines:
    print(each)"""

## End added
##############

data = {
    "Inputs": {
        "data": jsonlines,
    },
    "GlobalParameters": {
        'method': "predict",
    }
}


body = str.encode(json.dumps(data))

url = 'http://7ac06799-508e-414b-b8ec-47fe5a5d4226.centralus.azurecontainer.io/score'
api_key = '' # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(json.loads(error.read().decode("utf8", 'ignore')))


######
## FM
result = result.decode()
print(f"result.decode(): {result}")
result_lst = json.loads(result)['Results']
print(f"result_lst: {result_lst}")

result_df = pd.DataFrame({
        "id": idxs,
        "song_popularity": result_lst
})

print(result_df)

result_df.to_csv("result.csv", index=False)
