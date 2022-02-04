
import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here
data = {
    "Inputs": {
        "data":
        [
            {
                'song_duration_ms': "0",
                'acousticness': "0",
                'danceability': "0",
                'energy': "0",
                'instrumentalness': "0",
                'key': "0",
                'liveness': "0",
                'loudness': "0",
                'audio_mode': "0",
                'speechiness': "0",
                'tempo': "0",
                'time_signature': "0",
                'audio_valence': "0",
            },
        ],
    },
    "GlobalParameters": {
    }
}


####################################################
# Added to original downloaded file
####################################################
from csv_to_json import *

idxs, input_data = create_json_input(
    csv_path="../kaggle_competition_data/test.csv", 
    id="id", 
    remove=["id"], 
    fill=-750, 
)
print(f"input_data[:1]: {input_data[1:2]}")
print(f"idxs[:1]: {idxs[1:2]}")

data = {
    "Inputs": {
        "data": input_data[1:2],
    },
    "GlobalParameters": {
    }
}

####################################################
# End 
####################################################


body = str.encode(json.dumps(data))

url = 'http://1b2c9d0e-9342-4735-ba70-7408415dac7f.centralus.azurecontainer.io/score'
api_key = '' # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers)



#try:
response = urllib.request.urlopen(req)

result = response.read()
print(result)
"""except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(json.loads(error.read().decode("utf8", 'ignore')))"""



def export_prediction_csv(result, idxs:list, csv_file:str="test_predictions.cvs"):
    result = result.decode()
    result_lst = json.loads(result)['Results']
    result_df = pd.DataFrame({
        "id": idxs,
        "song_popularity": result_lst
    })

    result_df.to_csv(csv_file, index=False)



####################################################
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

result_df.to_csv("test_predictions.csv", index=False)