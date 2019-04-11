# Predicting the 3-Year Change in Diabetes Rates at the County Level

## Context

Diabetes is a big and growing health problem in the US. About 30% of the US population currently has diabetes or prediabetes ([source](http://www.diabetes.org/assets/pdfs/basics/cdc-statistics-report-2017.pdf)) - a number that has tripled since 1990.



<img src="/images/Diabetes_growth_1958_2015.png" width="600px" align="middle">



The human and economic costs associated with diabetes are high. Some examples:
 - People with diabetes are at higher risk for serious health problems including stroke, blindness, kidney diseases, and others.
 - In 2015, diabetes was the seventh leading cause of death in the U.S.
 - $1 in $7 healthcare dollars in 2018 was spent on diabetes and it’s complications.



Type 2 diabetes, which generally onsets in adulthood, accounts for 95% of all cases. Research indicates that type 2 diabetes is caused by a combination of genetics and lifestyle factors. However, there are many reasons why people do not or cannot maintain lifestyles that optimally promote their health. 

**Government policies are one of the tools we have to enact wide-spread change to curb diabetes. However, where should we focus on enacting these polcies?**
 

&nbsp;
&nbsp;

## My Project Goal


**Predict how much the diabetes rates for specific geographic populations will change in 3 years.**

Specifically: I will use county-level population data available in 2010 to predict the how much the diabetes rate increased or decresed by 2013. 

*Why?*  If we can correctly predict which geographic areas are likely to see the highest growth in diabetes rates, we can gain insight into where we should focus on enacting government policies. 


&nbsp;
&nbsp;

## Overview: My Process & Git Repository

 - **Step 1:** 
Gather data from 9 difference sources for all 3,142 unique counties and county-equivalents (parishes, boroughs, census areas, etc) in the 50 U.S. states; clean and format for consistency
   - The code for this process appears in `src/_import_data.py` ([view](https://github.com/lbordz/diabetes-rates-prediction/blob/master/src/_import_data.py))


 - **Step 2:**
Merge all data into one dataframe, 
combine into one dataframe, create target colum, create separate training and test set files. 
   - The code for this process appears in `src/import_test_train_split.py` ([view](https://github.com/lbordz/diabetes-rates-prediction/blob/master/src/import_train_test_split.py))
&nbsp;


 - **Step 3:**
Exploratory data analysis: explore initial feature trends, investigate outliers, clean data, remove highly correlated features, and added featurization. 
   - The code for final data cleaning and featurization appears in `src/_data_cleaning.py` ([view](https://github.com/lbordz/diabetes-rates-prediction/blob/master/src/_data_cleaning.py))
&nbsp;


 - **Step 4:**
Model Selection: Explore both interpretable and less interpretable models (Goal of that: to get insights on predictive features, but not sarifice performance). Find model(s) that best improve prediction error compared to baseline; model tuning.
   - The code for my final model in `src/model.py` ([view](https://github.com/lbordz/diabetes-rates-prediction/blob/master/src/model.py))
&nbsp;


 - **Step 5:** 
Explore top predictors of my model(s), visualized to understand relationships. 
   - The code for all my graphs in `<to be added>` ([view]())



&nbsp;
&nbsp;


## Data (Input)

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

## Results (Output)





### Evaluation Metrics

Since I was working with regression across linear and ensemble models, I used the **Mean Squared Error** to evaluate my models.

Specifically, my baseline RMSE was my error for the simplest model - always predicting the training average value. I evaluated my subsequent models based on how much the RMSE score was reduced compared to the baseline model.

The RMSE of my baseline was 12.1 PP (Percentage Points).


### Results

My best-performing model gave me an MSE of 11.1 PP - an 8.6% reduction in the baseline RMSE. This model was a random forest model, with additional parameters set to prune the trees to prevent overfitting.

However, the best-performing highly-interpretable model, lasso linear regression, was not too far behind with a 11.2 PP RMSE, which translates to a 7.8% reduction in the RMSE of my baseline model.

I leveraged both models to find insights. 


### Insights


The graphs below visualize the features that were the best predictors for the change in diabetes rate for each model. 

 - For Lasso, the best predictors are the features which have the highest weight on the final prediction.
 - For the random forest model, the best predictors are the ones that most often did the best job of minimizing variance in each split. (Note: only the top 5 important features in the random forest model ranked better than random noise)


<div> 
<img src="/images/top_lasso_pred.png" width="415px" align="left">
<img src="/images/top_rf_pred.png" width="415px" align="right">
</div>

The top four features in BOTH models were:
 - Change in Diabetes Rates 2009-2010
 - Diabetes Rate in 2010
 - Unemployment Rate 2010
 - Leisure Inactivity 2010


Here are partial dependency plots for these top 4 features, showing for both models, the general relationship between the feature values and the predicted diabetes change rate:


<img src="/images/top4_relationships.png" align="center">


Possible explanation / Interpretations:



Possible I


In addition, Any Alcohol Use and % Hispanic showed up in the top 10 of both. 






Possible Explanations:

 - The change in diabetes Rate (2009-2010) and the Diabetes rate in 2010 are likely regression towards the mean. 
 - Feature importancee for randomf forest: We expect numeric coumsn to come up more often than classification ones






<img src="/images/lassorelationships.png" width="600px" align="middle">


Coefficient:

Holding all other features constant:

Each beta representes the increase in the predicted value of Y for a one-unit increase in the feature *after scaling*

Example:

2010 DB coeff = -3.64

Represents a 3.64 unit DECREASE in predicted value of Y for a one-unit increase in 2010 DB *after scaling*

Represents a 3.64 unit DECREASE in predicted value of Y for a 13-unit increase in
2010 DB (before scaling).




## The Future



Future: Explore more faetures
(Example, Educational e






