from doctest import OutputChecker
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler, QuantileTransformer
from IPython.display import display_html 
from sklearn.linear_model import LinearRegression, LassoLars, TweedieRegressor


def predict_baseline(train):
    '''
    Function to calculate the RMSE for the mean and median tax value of zillow properties
    accepts train dataframe, displays a table of formatted results, and returns a results table
    '''

    # create y_train and y_validate
    y_train = train['tax_value']
        
    y_train = pd.DataFrame(y_train)
    
    value_pred_mean = y_train['tax_value'].mean()
    y_train['value_pred_mean'] = value_pred_mean

    # compute value_pred_median
    value_pred_median = y_train['tax_value'].median()
    y_train['value_pred_median'] = value_pred_median

    # RMSE of value_pred_mean
    rmse_train = mean_squared_error(y_train.tax_value, y_train.value_pred_mean)**(1/2)

    results = pd.DataFrame(columns = ['model', 'RMSE_train', 'RMSE_validate', 'R2'])
    newresult = ['Mean','${:,.2f}'.format(rmse_train),'N/A', 'N/A']
    results.loc[len(results)] = newresult

    # RMSE of value_pred_median
    rmse_train = mean_squared_error(y_train.tax_value, y_train.value_pred_median)**(1/2)

    # create and display tabular formatted data
    newresult = ['Median','${:,.2f}'.format(rmse_train),'N/A', 'N/A']
    results.loc[len(results)] = newresult

    df_style = results.style.set_table_attributes("style='display:inline; margin-right:100px;'").set_caption("RESULTS")
    display_html(df_style._repr_html_(), raw=True)

    return results


def LRmodel(model, X_train, y_train, X_2, y_2):
    '''
    Function to fit a model, make predictions on two sets of data, and return a 
    row of evaluation data
    Accepts: a model (not fit)
             a dataframe of X_train data that will be used to fit the model
             a dataframe of y_train data that will be used to fit the model
             a second dataframe of X data (can be validate or test) to make predictions
             a second dataframe of y data (can be validate or test) to evaluate predictions
    Returns: a list containing the model, the RMSE for train data, the RMSE of the second dataset,
             and the R2 score of the second dataset
    '''
    # fit the model object
    model.fit(X_train, y_train)

    # predict train
    yhat_train = model.predict(X_train)
    yhat_2 = model.predict(X_2)

    # evaluate: rmse for train
    rmse_train = mean_squared_error(y_train, yhat_train)**(1/2)

    # evaluate: rmse for validate (or test if that is what is sent to the function)
    rmse_2 = mean_squared_error(y_2, yhat_2)**(1/2)

    # format results and save as a list that will be returned
    newresult = [model,'${:,.2f}'.format(rmse_train),'${:,.2f}'.format(rmse_2), round(r2_score(y_2, yhat_2),4)]

    return newresult