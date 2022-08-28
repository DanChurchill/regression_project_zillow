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
The purpose of this project is to aquire customer data for the Telco Company from a database, create a model to predict customer churn, and utilize that model to make predictions from a group of customers

Goal 1: Create a model that can predict churn with greater accuracy than baseline

Goal 2: Find drivers for customer churn at Telco and make recommendations to improve retention


[[Back to top](#top)]

***
## <a name="planning"></a>Project Planning: 


### Project Outline:
- Acquire data from the Codeup Database using a function saved in an acquire.py file to import into the Final Report Notebook.
- Perform initial data exploration to determine what preparations the data needs to undergo.
- Clean and prepare data utilizing a function saved in a prepare.py, and prepare data in Final Report Notebook by importing and using the funtion.
- Clearly define two hypotheses, set an alpha, run statistical tests needed to reject or fail to reject the Null Hypothesis, and document findings and takeaways.
- Establish a baseline accuracy.
- Train three different classification models.
- Evaluate models on train and validate datasets.
- Choose the model with that performs the best and evaluate that single model on the test dataset.
- Create csv file with the customer id, the probability that the customer has churned, and the model's prediction for each observation in my test dataset.
- Document conclusions, takeaways, and next steps in the Final Report Notebook.

[[Back to top](#top)]
***

## <a name="dictionary"></a>Data Dictionary  

| Target Attribute | Definition | Data Type |
| ----- | ----- | ----- |
| churn | 1 if the customer has churned | int |


---
| Feature | Definition | Data Type |
| ----- | ----- | ----- |
| customer_id | Unique id for each customer| string |
| senior_citizen| 1 if customer is a senior citizen | int |
| tenure | Months of tenure as a customer| int |
| monthly_charges| The customer's monthly bill| float |
| total_charges| The customer's total bills since they have been a customer| float|
| male | 1 if the customer is male | int |
| partner | 1 if the customer has a partner  | int |
| dependents | 1 if the customer has dependents | int |
| phone | 1 if the customer has phone service | int |
| paperless_billing | 1 if the customer has paperliess billing | int |
| multiple_lines_yes | 1 if the customer has multiple phone lines | int |
| online_security_no | 1 if the customer has internet but no online security | int |
| online_security_yes | 1 if the customer has online security add-on | int |
| online_backup_no | 1 if the customer has internet but no online backup | int |
| online_backup_yes | 1 if the customer has online backup | int |
| device_protection_no | 1 if the customer has internet but no device protection | int |
| device_protection_yes | 1 if the customer has device protection | int |
| tech_support_no | 1 if the customer has internet but no tech support | int |
| tech_support_yes | 1 if the customer has tech_support | int |
| streaming_tv_no | 1 if the customer has internet but no streaming tv | int |
| streaming_tv_yes | 1 if the customer has streaming tv | int |
| streaming_movies_no | 1 if the customer has internet but no streaming movies | int |
| streaming_movies_yes | 1 if the customer has streaming movies | int |
| contract_type_month-to-month | 1 if the customer has a month-to-month contract | int |
| contract_type_one_year | 1 if the customer has a one year contract  | int |
| contract_type_two_year | 1 if the customer has a two year contract | int |
| payment_type_bank_transfer_auto | 1 if the customer pays by automatic bank transfer | int
| payment_type_credit_card_auto | 1 if the customer pays automatically by credit card | int
| payment_type_electronic_check | 1 if the customer pays manually by electronic check | int
| payment_type_mailed_check | 1 if the customer pays manually by mailed check | int
| internet_type_dsl  | 1 if the customer has DSL internet service |  int
| internet_type_fiber_optic | 1 if the customer has fiber optic internet service | int
| internet_type_none | 1 if the customer has no internet | int
| addon_count | sum of how many internet service add-ons the customer has | int

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
