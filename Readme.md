# Doing Inference from Azure AutoML Model (Song Popularity Prediction)
  
[Song Popularity Prediction](https://www.kaggle.com/c/song-popularity-prediction) competition data was used to train a classification model with Azure AutoML services.  
  
The files from trained model and conda environment were downloaded in the folder [AutoMachineLearningSongContestModel](./AutoMachineLearningSongContestModel).  
  
## Creating conda environment from `conda_env_v_1_0_0.yml`
Using anaconda prompt:  
```
.\2022-02_SongPopularityAzAutoML> conda env create -f .\AutoMachineLearningSongContestModel\conda_env_v_1_0_0.yml  
.\2022-02_SongPopularityAzAutoML> conda activate song-popularity-az-model
```  
  
Then, when executing `main.py` the following error was generated:  
```  
.\2022-02_SongPopularityAzAutoML> python main.py

(...) Requirement.parse('cryptography!=1.9,!=2.0.*,!=2.1.*,!=2.2.*,<4.0.0')  
(...) Requirement.parse('urllib3<=1.26.7,>=1.23')
``` 
  
The urlib3 library installed was 1.26.8 and cryptography 36.0.1.  
The following libraries were installed:
```  
.\2022-02_SongPopularityAzAutoML> pip install azureml-automl-runtime
.\2022-02_SongPopularityAzAutoML> pip install urllib3==1.26.7

``` 

`.\2022-02_SongPopularityAzAutoML> pip install azureml-automl-runtime`  
  
## Before continuing
In order to compare the model running locally, the same model was first deployed at Azure:
[Use automated machine learning in Azure Machine Learning](https://docs.microsoft.com/en-us/learn/modules/use-automated-machine-learning/7-deploy-model)  
```   
{
  "Inputs": {
    "data": [
      {
        "song_duration_ms": 0,
        "acousticness": 0,
        "danceability": 0,
        "energy": 0,
        "instrumentalness": 0,
        "key": 0,
        "liveness": 0,
        "loudness": 0,
        "audio_mode": 0,
        "speechiness": 0,
        "tempo": 0,
        "time_signature": 0,
        "audio_valence": 0
      }
    ]
  },
  "GlobalParameters": {
    "method": "predict"
  }
}
``` 
1. Didn't know how to set null/empty values for testing at Azure ML portal to work. 
2. Tested endpoint running `endpoint_script.py` with 5 first test values, returning predictions: [0, 0, 0, 0, 0,]
3. All tests I did returned `song_prediction` equals to 0 ...
4. Example inferences from deployed API: [`rows30-50-result.csv`](rows30-50-result.csv) & [`sample20-result.csv`](sample20-result.csv)
5. I send all the [test dataset](./kaggle_competition_data/test.csv) and returned al only fourty something one from 10,0...
6. Looked at the best submission to the competition and the biggest values was `0.4894715` for id `254`. So maybe Azure Classification. See [`result.csv`](result.csv) is going to return zeroes for all values?

## Started to train anothe model using Regression
- Loaded train.csv
- 5 folds for k-fold cross validation
- Median imputation for all numerical and `key`
- By selecting regression, Azure didn't allow to use *AUC* as metric, *Normalized root mean squared error* was set.
- The best algorithm (0.47759 error) was a *StackEnsemble* with the following details:
  - Data transformation:
  ```  
  {
    "class_name": "StandardScaler",
    "module": "sklearn.preprocessing",
    "param_args": [],
    "param_kwargs": {
        "with_mean": false,
        "with_std": true
    },
    "prepared_kwargs": {},
    "spec_class": "preproc"
  }
  ```
    - Training algorithm:
  ```
  {
    "class_name": "LightGBMRegressor",
    "module": "automl.client.core.common.model_wrappers",
    "param_args": [],
    "param_kwargs": {
        "boosting_type": "gbdt",
        "colsample_bytree": 0.8,
        "learning_rate": 0.02106157894736842,
        "max_bin": 255,
        "max_depth": 7,
        "min_data_in_leaf": 0.008804237587752594,
        "min_split_gain": 0.5263157894736842,
        "n_estimators": 100,
        "num_leaves": 15,
        "reg_alpha": 0,
        "reg_lambda": 0,
        "subsample": 0.3,
        "subsample_freq": 7
    },
    "prepared_kwargs": {},
    "spec_class": "sklearn"
  }
  ```  
    
The file [`scoring_file_v_1_0_0.py`](scoring_file_v_1_0_0.py) seems to be designed for the deploying the model onto Azure. When loading `model.pkl`, its type is `<class 'sklearn.pipeline.Pipeline'>`.  It seems that you cannot download the model and deploy where you want.  
  
### Deploying the new model and generating a submission
1. At the portal, going to *Microsoft Azure Machine Learning Studio \> Automated ML* and selecting *song-popularity-autoML-regressor* experiment.
2. Then, at *Best model summary*, select the algorithm and press *Deploy > Deploy to web service* to deploy it.
3. Then at the *Endpoints* section you can get the code to consume it.

The endpoint (deployed twice) is giving some `timeout_exception.TimeoutException`... boh. It works when using it in *Test*, but not remote *Consume*. Consume script was tested using local brach and Colab.  
  
Then I tried to debug according to this reference [Troubleshooting remote model deployment](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-troubleshoot-deployment):  
```  
az extension add --name ml  
az ml service list  --workspace-name machine-learning-ws  


No me funcionaron:  
az ml dataset list --workspace-name machine-learning-ws --resource-group machine-learning-rg


az ml service get-logs --verbose --workspace-name <my workspace name> --name <service name>  
``` 


## References
- [Deploy models trained with Azure Machine Learning on your local machines](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-deploy-local#download-and-run-your-model-directly)  
- [How to use a model trained by Azure AutoML](https://docs.microsoft.com/en-us/answers/questions/297882/how-to-use-a-model-trained-by-azure-automl.html)  
- [Use automated machine learning in Azure Machine Learning](https://docs.microsoft.com/en-us/learn/modules/use-automated-machine-learning/7-deploy-model)  
