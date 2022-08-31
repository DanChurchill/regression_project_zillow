import pandas as pd
import numpy as np

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
    df.garagetotalsqft = df.garagetotalsqft.fillna(0)   

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