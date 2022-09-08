import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler, QuantileTransformer
from IPython.display import display_html 
from sklearn.linear_model import LinearRegression, LassoLars, TweedieRegressor



def scaler(scaler, X, y):
    '''
    function accepts a scaler, and train/validate/test dataframes and 
    performs min_max scaling on the sq_ft and tax_amount columns
    returns the train, validate, and test dataframes with the additional 
    scaled columns
    '''
    scaled = scaler.fit_transform(X, y)

    return scaled

def predict_baseline(train, validate):

        
    # create y_train and y_validate
    y_train = train['tax_value']
    y_validate = validate['tax_value']
        
    y_train = pd.DataFrame(y_train)
    y_validate = pd.DataFrame(y_validate)
    
    value_pred_mean = y_train['tax_value'].mean()
    y_train['value_pred_mean'] = value_pred_mean
    y_validate['value_pred_mean'] = value_pred_mean

    # 2. compute value_pred_median
    value_pred_median = y_train['tax_value'].median()
    y_train['value_pred_median'] = value_pred_median
    y_validate['value_pred_median'] = value_pred_median

    # 3. RMSE of value_pred_mean
    rmse_train = mean_squared_error(y_train.tax_value, y_train.value_pred_mean)**(1/2)
    rmse_validate = mean_squared_error(y_validate.tax_value, y_validate.value_pred_mean)**(1/2)

    results = pd.DataFrame(columns = ['model', 'RMSE_train', 'RMSE_validate', 'R2'])
    newresult = ['Mean','${:,.2f}'.format(rmse_train),'', 'N/A']
    results.loc[len(results)] = newresult

    # 4. RMSE of value_pred_median
    rmse_train = mean_squared_error(y_train.tax_value, y_train.value_pred_median)**(1/2)
    rmse_validate = mean_squared_error(y_validate.tax_value, y_validate.value_pred_median)**(1/2)

    newresult = ['Median','${:,.2f}'.format(rmse_train),'', 'N/A']
    results.loc[len(results)] = newresult

    df_style = results.style.set_table_attributes("style='display:inline; margin-right:100px;'").set_caption("RESULTS")
    display_html(df_style._repr_html_(), raw=True)

    return results


def LRmodel(model, train, validate, features):
    # create X and y
    X_train = train[features]
    y_train = train['tax_value']

    X_validate = validate[features]
    y_validate = validate['tax_value']

    # create MinMaxScaler and fit to train
    scaler = MinMaxScaler()
    X_train[features] = scaler.fit_transform(X_train[features])
    X_validate[features] = scaler.transform(X_validate[features])


    # fit the model object
    model.fit(X_train, y_train)

    # predict train
    yhat_train = model.predict(X_train)

    # evaluate: rmse
    rmse_train = mean_squared_error(y_train, yhat_train)**(1/2)

    # predict validate
    yhat_validate = model.predict(X_validate)

    # evaluate: rmse
    rmse_validate = mean_squared_error(y_validate, yhat_validate)**(1/2)

    newresult = [model,'${:,.2f}'.format(rmse_train),'${:,.2f}'.format(rmse_validate), r2_score(y_validate, yhat_validate)]

    return newresult