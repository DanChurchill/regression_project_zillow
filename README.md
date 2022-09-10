# 2017 ZILLOW CLASSIFICATION PROJECT <a name="top"></a>
![]()

by: Dan Churchill

<p>
  <a href="https://github.com/DanChurchill" target="_blank">
    <img alt="Dan" src="https://img.shields.io/github/followers/DanChurchill?label=Follow_Dan&style=social" />
  </a>
</p>


***
[[Project Description](#project_description)]
[[Project Planning](#planning)]
[[Data Dictionary](#dictionary)]
[[Data Acquire and Prep](#wrangle)]
[[Data Exploration](#explore)]
[[Modeling](#model)]
[[Conclusion](#conclusion)]
[[Steps to Reproduce](#reproduce)]
___



## <a name="project_description"></a>Project Description:
The purpose of this project is to create a Regression Model that predicts property tax assessed values of Single Family Properties that were sold in 2017 from a database of Zillow data  
    
  Goal 1: Create a model that can predict the tax value better than the baseline rate<br>
  Goal 2: Find the key drivers of tax value for single family properties<br>
  Goal 3: Identify where the properties are located


[[Back to top](#top)]

***
## <a name="planning"></a>Project Planning: 


### Project Outline:
- Acquire, clean, and prepare data from the Codeup Database using a function saved in a wrangle.py file to import into the Final Report Notebook.
- Perform initial data exploration to determine what features will be usefull for modeling
- Establish a baseline RMSE
- Train three different linear regression models and evaluate on train and validate datasets
- Choose the model with that performs the best and evaluate that single model on the test dataset
- Document conclusions, takeaways, and next steps in the Final Report Notebook.

[[Back to top](#top)]
***

## <a name="dictionary"></a>Data Dictionary  

| Target Attribute | Definition | Data Type |
| ----- | ----- | ----- |
| tax_value | the 2017 assessed tax value of the property | float |


---
| Feature | Definition | Data Type |
| ----- | ----- | ----- |
| parcelid | Unique id for each property| int |
| bathrooms| The number of bathrooms on the property | float |
| bedrooms | The number of bedrooms on the property | float |
| county| The County the property is located in | string |
| fireplacecnt | The number of fireplaces on the property | float|
| garagecarcnt | The number of cars that can be held in the garage on the property | float |
| lotsize | the square footage of the land | float |
| poolcnt | the number of pools on the property | float |
| lat | The geographical latitude of the property | float |
| long | The geographical longitude of the property | float |
| logerror | the logerror of zillows model, retained for possible future use, but not used in this project | float |
| tract | the census tract of the property, with the FIPS and decimal portions removed | float |
| Los Angeles | 1 if the property is in LA County | int |
| Orange | 1 if the property is in Orange County | int |
| Ventura | 1 if the property is in Ventura County | int |
| 1.0 | 1 if the property has one bedroom | int |
| 2.0 | 1 if the property has two bedrooms | int |
| 3.0 | 1 if the property has three bedrooms | int |
| 4.0 | 1 if the property has four bedrooms | int |
| 5.0 | 1 if the property has five bedrooms | int |
| 6.0 | 1 if the property has six bedrooms | int |
| 7.0 | 1 if the property has seven bedrooms | int |
| 8.0 | 1 if the property has eight bedrooms | int |
| 9.0 | 1 if the property has nine bedrooms | int |
| 10.0 | 1 if the property has ten bedrooms | int |
| 11.0 | 1 if the property has eleven bedrooms | int |
| age | the age of the property in years | float
| 4plusBath | 1 if the property has more than three bathrooms | int
| 3to5garage | 1 if the property's garage has the capacity for 3 to 5 cars | int

[[Back to top](#top)]

***

## <a name="wrangle"></a>Data Acquisition and Preparation

Data is acquired from the Codeup Database server using an SQL query within the modular function get_telco_data located in the acquire.py file.  This returns a dataframe containing 7043 rows and 23 columns of data

Preparation is performed using the modular function prep_telco located in the prepare.py file.  This function performs the following on the data:

- Deletes the id columns that contained redundent information
- Converted total_charges from a string to a float
    * NOTE: There were 11 entries of 0 for total_charges, but in each case the tenure was also 0 indicating they were new customers; no values were imputed because this was a logical value
- Encoded categorical and binary columns using 1-hot encoding
- Renamed some columns for brevity
- Created 'addon_count' column, a count of how many internet add-ons each customer has
- Split Data into 80% Train, 20% Validate, and 20% Test using 'Churn' as stratification



[[Back to top](#top)]

![]()


*********************

## <a name="explore"></a>Data Exploration:

### Correlation Testing
The first step was to explore each variable's linear correlation using a custom modular function correlation_report located in the explore.py file.  This function accepts a dataframe (in this case our training dataset) and a target column (in this case our target variable 'churn'),  The function performs a correlation test on each column, sorts the absolute values, and returns two tables with the 11 strongest correlations, and the 11 weakest correlations.

Correlation test takeaways:
 - Contract types, internet, payment by check, and not having internet add-ons showed higher correlation to churn
 - Phone service, gender, and multiple lines showed lower correlation to churn

### Exploring Internet Service
The training data was split into subsets of those that did and did not have internet service to see which was more likely to churn. 

- **Hypothesis**
- $H_0$: There is no difference in churn between those with and without internet service
- $H_a$: There is a significant difference in churn between those with and without internet service

We failed to confirm the null hypothesis and confirmed via visualization that customers without internet service were more likely to churn

### Exploring Number of Internet Service Add-Ons
To explore why internet users were more likely to churn we then utilized the add-on_count column by using a $Chi^2$ test

- **Hypothesis**
- $H_0$: 'Churn is independent of the number of add-on services'
- $H_a$: 'Churn is dependent on the number of add-on services'

We failed to confirm the null hypothesis and confirmed via visualization that customers with fewer add-on services were more likely to churn

### Exploring Monthly Charges and Internet Service Add-Ons
We saw that monthly charges correlated to churn, and that more add-ons meant higher churn.  Looking at the breakdown visually we were able to see that customers that paid more for the same number of add-ons churned at a higher rate.


### Takeaways from exploration:
- We've identified that internet customers churn at a higher rate
- Internet customers with fewer add-on services, and those that pay more for internet services, churn more
- Gender, phone service, and multiple lines are our least significant indicators of churn
- During modeling we'll begin with the features we determined to be most important

[[Back to top](#top)]

***

## <a name="model"></a>Modeling:

#### Training Dataset
| Model | Accuracy | f1 score |
| ---- | ---- | ---- |
| Baseline | 0.74| N/A |
| K-Nearest Neighbor | 0.80 | 0.53 |  
| Random Forest | 0.81 | 0.58 |  
| Logistic Regression | 0.80 | 0.60 |  

#### Validation Dataset
| Model | Accuracy | f1 score |
| ---- | ---- | ---- |
| Baseline | 0.74| N/A |
| K-Nearest Neighbor | 0.78 | 0.47 |  
| Random Forest | 0.79 | 0.53 |  
| Logistic Regression | 0.78 | 0.56 |  


- The Logistic Regression model performed the best


## Testing the Model

- Logistic Regression Results on Test Data

#### Testing Dataset
             precision    recall  f1-score   support

           0       0.85      0.90      0.87      1035
           1       0.66      0.56      0.61       374

    accuracy                           0.81      1409
    macro avg      0.76      0.73      0.74      1409
    weighted avg   0.80      0.81      0.80      1409

[[Back to top](#top)]

***

## <a name="conclusion"></a>Conclusion and Next Steps:

- We created a churn classification model that beat the baseline prediction by more than 7%

- The customers that our model predicted as more likely-churned, but who haven't churned yet, should be incentivized to remain customers 

- Customers with Internet Service (particularly those that do not have add-ons) are more likely to churn, especially if their bills are higher.  Making the add-ons less expensive could help retain customers longer.

- Shorter contract types showed higher correlation to churn, and given more time I would have explored that further to determine what other factors drove those customers to churn

[[Back to top](#top)]

*** 

## <a name="reproduce"></a>Steps to Reproduce:

You will need your own env.py file with database credentials then follow the steps below:

  - Download the acquire.py, prepare.py, explore.py, and final_report.ipynb files
  - Add your own env.py file to the directory (user, host, password)
  - Run the final_repot.ipynb notebook

[[Back to top](#top)]
