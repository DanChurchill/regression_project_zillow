import os
import pandas as pd
import numpy as np
import env
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
                       fullbathcnt, garagecarcnt, garagetotalsqft as garagesqft, hashottuborspa, lotsizesquarefeet, poolcnt, rawcensustractandblock,
                       roomcnt, unitcnt, yearbuilt, structuretaxvaluedollarcnt as structure_tax_value, taxvaluedollarcnt as tax_value, 
                       landtaxvaluedollarcnt as land_tax_value,
                       taxdelinquencyflag, taxdelinquencyyear, logerror, transactiondate, propertylandusedesc
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
    df['county_name'] = df.county.map({6037 : 'Los Angelos', 6059 : 'Orange', 6111 : 'Ventura'})

    # convert poolcnt nulls to 0's
    df.poolcnt = df.poolcnt.fillna(0)

    # convert fireplace count nulls to 0
    df.fireplacecnt = df.fireplacecnt.fillna(0)

    # garage null values to 0
    df.garagecarcnt = df.garagecarcnt.fillna(0)
    df.garagesqft = df.garagesqft.fillna(0)   

    # hottub/spa nulls to 0
    df.hashottuborspa = df.hashottuborspa.fillna(0)

    # has pool nulls to 0
    df.poolcnt = df.poolcnt.fillna(0)

    # drop rows where unit count is 2 or 3 (incorrectly coded as single family) then drop column
    df = df[(df.unitcnt != 2) & (df.unitcnt != 3)]
    df.drop(columns='unitcnt', inplace=True)

    # drop rows where tax delinquency exists as these will have values that don't fit the model, then delete columns
    df = df[df.taxdelinquencyflag != 'Y']
    df.drop(columns=['taxdelinquencyflag', 'taxdelinquencyyear'], inplace=True)

    # drop remaining rows with null values 
    df = df.dropna()

    return df