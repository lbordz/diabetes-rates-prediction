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

Specifically: I will use county-level population data available in 2010 and prior to predict how much the diabetes rate in each county will have changed in 2013.

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
