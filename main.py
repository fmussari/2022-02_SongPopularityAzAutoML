import pickle
import urllib3
import cryptography

print(f"urllib3.__version__ : {urllib3.__version__}")
print(f"cryptography.__version__ : {cryptography.__version__}")


with open('StackEnsembleModel/model.pkl', 'rb') as f : 
   #song_popularity_model = pickle.load(f, encoding='latin1')
   song_popularity_model = pickle.load(f)

print('*'*10)
print('*'*10)
print(type(song_popularity_model))
print(song_popularity_model.__dict__)


