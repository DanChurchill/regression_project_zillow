
SELECT parcelid, bathroomcnt, bedroomcnt, calculatedfinishedsquarefeet as sqft, fips as county, fireplacecnt,
	   fullbathcnt, garagecarcnt, garagetotalsqft, hashottuborspa, lotsizesquarefeet, poolcnt, rawcensustractandblock,
       roomcnt, unitcnt, yearbuilt, structuretaxvaluedollarcnt, taxvaluedollarcnt, landtaxvaluedollarcnt,
       taxamount, taxdelinquencyflag, taxdelinquencyyear, censustractandblock, logerror, transactiondate, propertylandusedesc
FROM properties_2017
JOIN predictions_2017
USING (parcelid)
JOIN propertylandusetype
USING (propertylandusetypeid)
HAVING propertylandusedesc = 'Single Family Residential'