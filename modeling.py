import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

from sklearn.preprocessing import MinMaxScaler, QuantileTransformer



def scaler(scaler, X, y):
    '''
    function accepts a scaler, and train/validate/test dataframes and 
    performs min_max scaling on the sq_ft and tax_amount columns
    returns the train, validate, and test dataframes with the additional 
    scaled columns
    '''
    scaled = scaler.fit_transform(X, y)

    return scaled