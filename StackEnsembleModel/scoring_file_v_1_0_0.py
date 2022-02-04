# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
import logging
import os
import pickle
import numpy as np
import pandas as pd
import joblib

import azureml.automl.core
from azureml.automl.core.shared import logging_utilities, log_server
from azureml.telemetry import INSTRUMENTATION_KEY

from inference_schema.schema_decorators import input_schema, output_schema
from inference_schema.parameter_types.numpy_parameter_type import NumpyParameterType
from inference_schema.parameter_types.pandas_parameter_type import PandasParameterType


#0,308523.0,0.019845340510348215,,0.9089387810684176,0.0014384979828828493,,0.11283225018899048,
#-8.890171605720209,0,0.08271435018066495,126.12930376264788,4,0.39962045149647313
input_sample = pd.DataFrame(
    {
        "song_duration_ms": pd.Series([0,308523.0], dtype="float64"), 
        "acousticness": pd.Series([0.019845340510348215], dtype="float64"), 
        "danceability": pd.Series([None], dtype="float64"), 
        "energy": pd.Series([0.9089387810684176], dtype="float64"), 
        "instrumentalness": pd.Series([0.0014384979828828493], dtype="float64"), 
        "key": pd.Series([None], dtype="float64"), 
        "liveness": pd.Series([0.11283225018899048], dtype="float64"), 
        "loudness": pd.Series([-8.890171605720209], dtype="float64"), 
        "audio_mode": pd.Series([0], dtype="int64"), 
        "speechiness": pd.Series([0.08271435018066495], dtype="float64"), 
        "tempo": pd.Series([126.12930376264788], dtype="float64"), 
        "time_signature": pd.Series([4], dtype="int64"), 
        "audio_valence": pd.Series([0.39962045149647313], dtype="float64")
    }
)
output_sample = np.array([0])

try:
    log_server.enable_telemetry(INSTRUMENTATION_KEY)
    log_server.set_verbosity('INFO')
    logger = logging.getLogger('azureml.automl.core.scoring_script')
except:
    pass


def init():
    global model
    # This name is model.id of model that we want to deploy deserialize the model file back
    # into a sklearn model
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'model.pkl')
    model_path = os.path.join('', 'model.pkl')
    path = os.path.normpath(model_path)
    path_split = path.split(os.sep)
    log_server.update_custom_dimensions({'model_name': path_split[-3], 'model_version': path_split[-2]})
    try:
        logger.info("Loading model from path.")
        model = joblib.load(model_path)
        logger.info("Loading successful.")
    except Exception as e:
        logging_utilities.log_traceback(e, logger)
        raise


@input_schema('data', PandasParameterType(input_sample))
@output_schema(NumpyParameterType(output_sample))
def run(data):
    print("run")
    try:
        result = model.predict(data)
        print(f"result: {result}")
        return json.dumps({"result": result.tolist()})
    except Exception as e:
        result = str(e)
        return json.dumps({"error": result})

print("algo")
init()
run(input_sample)
