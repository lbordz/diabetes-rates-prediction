# Predicting the County-Level Change in Diabetes Rates Over a 3-Year Period

## Context

Diabetes is a big and growing health problem in the US. About 30% of the US population currently has diabetes or prediabetes ([source](http://www.diabetes.org/assets/pdfs/basics/cdc-statistics-report-2017.pdf)) - a number that has tripled since 1990.



<img src="/images/Diabetes_growth_1958_2015.png" width="600px" align="middle">



The human and economic costs associated with diabetes are high. Some examples:
 - People with diabetes are at higher risk for serious health problems including stroke, blindness, kidney diseases, and others.
 - In 2015, diabetes was the seventh leading cause of death in the U.S.
 - $1 in $7 healthcare dollars in 2018 was spent on diabetes and it’s complications.



Type 2 diabetes, which generally onsets in adulthood, accounts for 95% of all cases. Research indicates that type 2 diabetes is caused by a combination of genetics and lifestyle factors. However, there are many reasons why people do not or cannot maintain lifestyles that optimally promote their health. 

**Government policies are one of the tools we have to enact wide-spread change to curb diabetes. However, what policies should we enact? And what locations should be prioritize?**
 

&nbsp;
&nbsp;

## My Project Goal


**Predict how much the diabetes rate for specific geographic population will change in 3 years.**

Specifically: I will use county-level population data available in 2010 and prior to predict the percent change in the diabetes rate in each county from 2010-2013. 

*Why?*  If we can correctly predict which geographic areas are likely to see the highest growth in diabe tes rates, and understand some of the contributing factors, we can gain insight into what types of government policies we should enact, and where. 



&nbsp;
&nbsp;

## Data

I collected US county-level population statistics from several sources to serve as inputs to my model. 

 - **Sources:** The Center for Disease Control (CDC), the US Census Bureau (2009 & 2010), the Bureau of Labor Statistics (BLA), The Institute for Health Metrics and Evalation (IHME), and the US Department of Agriculture (USDA)

 - **Data Inputs:**
   - Diagnosed diabetes rates (CDC)
   - Obesity prevalence (CDC)
   - Leisure time inactivity prevalence (CDC)
   - Age (Census)
   - Gender  (Census)
   - Race/ethnicity  (Census)
   - Poverty rate (Census)
      - Percent of people living below the poverty threshold
   - Rural land rate (Census)
      - "Urban" land is defined largely by population density and a few owther land-use considerations. "Rural" land was defined as any land not urban.
   - Unemployment rates (BLA)
   - Prevalence of Any Drinking (IHME)
      - Defined as percent of people who have 1+ alcoholic drinks in 30 days
   - Prevalence of Heavy Drinking  (IHME)
      - Defined as percent of people who consume, on average, 1+ drinks per day for women or 2+ drinks/day for men 
   - Fast-food restaurants per capita (USDA)
      - Fast-Food defined as establishments that primarily provide food, where patrons generally order or select items and pay before eating.
    - Low access to a supermarket or large grocery store (USDA)
      - Low access defined as 1+ miles away from a store in urban areas, 10+ miles away in rural areas 



&nbsp;
&nbsp;

## Process Overview

1 - Gather and combine data into one dataframe; Export all data into one master file for exploratory data analysis, and create separate files with training data and test-set for model selection and evaluation. 
 - The input and target data was in 9 different xlsx/csv files. I manipulated all data so it could be merged into one dataframe, with one row per county. The final dataframe had data for all 3,142 unique counties and county-equivalents (parishes, boroughs, census areas, etc) in the 50 states and District of Columbia. 
 - The code for this process appears in `src/import_test_train_split.py`

2 - Exploratory data analysis
(more on this bleow)
 - The code for this process appears in `XXXXX`

3 - Model Selection
(more on this below)
 - The code for this process appears in `XXXXX`

4 - Model Insights
(more on this bleow)
 - The code for this process appears in `XXXXX`



- How did you go about solving your problem? What choices did you make?
(Choices - make missing values average - so few missing)
(Choices - knowing using lasso and looking at feature importance, didnt want highly correlated vaiables. So I noted which ones higly correlated, saw which one performed better, thats it)
(Choices -Lasso--> made some zero, performed better, also at same performance (basically), fewer features with higher coefficients)
*=(Choices - RF -> best of ensemble methods, slightly better)



## ....MORE ABOUT PROCESS (?) 


&nbsp;
&nbsp;

## Evaluation and Results

### Evaluation Metrics

Since I was working with regression across linear and ensemble models, I used the **Mean Squared Error** to evaluate my models.

Specifically, my baseline MSE was my error for the simplest model - always predicting the training average value. I evaluated my subsequent models based on how much the MSE score was reduced compared to the baseline model.


### Results

The best-performing model gave me a 16.5% reduction in the MSE error on my test set. This model was a random forest model. 

However, the best-performing highly-interpretable model, lasso linear regression, was not too far behind with a 15% reduction in the MSE error on my test set. 


### Insights


The graphs below visualize the features that were the best predictors for the change in diabetes rate for each model. 

(For Lasso, the best predictors are features which have the highest impact on the final prediction. For the random forest model, the best predictors are the ones that did the best job of minimizing variance in each split)

<div> 
<img src="/images/lassotop10.png" width="450px" align="left">
<img src="/images/rftop10.png" width="450px" align="right">

 </div>

<img src="/images/lassorelationships.png" width="600px" align="middle">







## Evaluation and Results








