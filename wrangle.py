import os
import pandas as pd
import numpy as np
import env
from sklearn.model_selection import train_test_split
from datetime import datetime

def get_connection(db, user=env.user, host=env.host, password=env.password):
    '''
    function to generate a url for querying the codeup database
    accepts a database name (string) and requires an env.py file with 
    username, host, and password.

    Returns an url as a string  
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'


def get_zillow():
    """
    Retrieve locally cached data .csv file for the zillow dataset
    If no locally cached file is present retrieve the data from the codeup database server
    Keyword arguments:
    none
    Returns:
    DataFrame
    """
    
    filename = "zillow.csv"

    # if file is available locally, read it
    if os.path.isfile(filename):
        return pd.read_csv(filename)
    
    else:
    # if file not available locally, acquire data from SQL database
    # and write it as csv locally for future use 
        df = pd.read_sql('''
                SELECT parcelid, bathroomcnt, bedroomcnt, calculatedfinishedsquarefeet as sqft, fips as county, fireplacecnt,
                       garagecarcnt, hashottuborspa, lotsizesquarefeet, unitcnt, yearbuilt, taxdelinquencyflag, 
                       logerror, transactiondate, propertylandusedesc, taxvaluedollarcnt as tax_value
                FROM properties_2017
                JOIN predictions_2017
                USING (parcelid)
                JOIN propertylandusetype
                USING (propertylandusetypeid)
                HAVING propertylandusedesc = 'Single Family Residential'
                    ''', get_connection('zillow'))

    # Write that dataframe to disk for later. This cached file will prevent repeated large queries to the database server.
        df.to_csv(filename, index=False)
    return df

def prep_zillow(df):
    '''
    function accepts a dataframe of zillow data and prepares it for use in 
    modelling
    
    returns a transformed dataframe
    '''

    # convert transaction column from a string to a date
    df.transactiondate = pd.to_datetime(df.transactiondate, infer_datetime_format=True) 

    # remove one transaction where date is in 2018
    df = df[df.transactiondate < '2018-01-01']

    # create column with fips value converted from an integer to the county name string
    df['county'] = df.county.map({6037 : 'Los Angelos', 6059 : 'Orange', 6111 : 'Ventura'})

    # convert poolcnt nulls to 0's
    df.poolcnt = df.poolcnt.fillna(0)

    # convert fireplace count nulls to 0
    df.fireplacecnt = df.fireplacecnt.fillna(0)

    # garage null values to 0
    df.garagecarcnt = df.garagecarcnt.fillna(0)

    # has pool nulls to 0
    df.poolcnt = df.poolcnt.fillna(0)

    # drop rows where unit count is 2 or 3 (incorrectly coded as single family) then drop column
    df = df[(df.unitcnt != 2) & (df.unitcnt != 3)]
    df.drop(columns='unitcnt', inplace=True)

    # drop rows where tax delinquency exists as these will have values that don't fit the model, then delete columns
    df = df[df.taxdelinquencyflag != 'Y']
    df.drop(columns=['taxdelinquencyflag'], inplace=True)

    df.drop(columns=['propertylandusedesc', 'transactiondate'], inplace=True)

   

    return df

def remove_outliers(df, k, col_list):
    ''' remove outliers from a list of columns in a dataframe 
        and return that dataframe
    '''
    
    for col in col_list:

        q1, q3 = df[col].quantile([.17, .83]) # get range
        
        iqr = q3 - q1   # calculate interquartile range
        
        upper_bound = q3 + k * iqr   # get upper bound
        lower_bound = q1 - k * iqr   # get lower bound

        # drop remaining rows with null values 
        df = df.dropna()
        
        # return dataframe without outliers
        
        df = df[(df[col] > lower_bound) & (df[col] < upper_bound)]
        
    return df

def my_split(df):
       '''
       Separates a dataframe into train, validate, and test datasets

       Keyword arguments:
       df: a dataframe containing multiple rows
       

       Returns:
       three dataframes who's length is 60%, 20%, and 20% of the length of the original dataframe       
       '''

       # separate into 80% train/validate and test data
       train_validate, test = train_test_split(df, test_size=.2, random_state=333)

       # further separate the train/validate data into train and validate
       train, validate = train_test_split(train_validate, 
                                          test_size=.25, 
                                          random_state=333)

       return train, validate, test