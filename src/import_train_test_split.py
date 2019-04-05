import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import string
import requests
from bs4 import BeautifulSoup

from sklearn.model_selection import train_test_split
from _import_data import *


# ---- HELPER FUNCTIONS ---------

def _merge_on_fips(big_df, other_df_name, feats_fips_colnames):
    big_df = big_df.merge(feat_dfs[other_df_name], left_on = "FIPS_master", right_on = feats_fips_colnames[other_df_name], how = 'outer' )
    return big_df

#  --- IMPORT ALL DATA  ---

census = import_census_data('../data/raw_data/cc-est2017-alldata.csv')
unemp = import_unemployment_data(filedir = '../data/raw_data/Unemployment/')
diabetes = import_diabetes_data('../data/raw_data/DM_PREV_ALL_STATES.xlsx')
foodenv = import_food_env_data('../Data/raw_data/DataDownload.xls', desired_columns = ['PCT_LACCESS_POP10', 'FFRPTH09'])
poverty = import_poverty_data('../data/raw_data/Poverty-Rates-by-County-1960-2010.xlsm')
inactivity = import_inactivity_data('../data/raw_data/LTPIA_PREV_ALL_STATES.xlsx')
obesity = import_obesity_data('../data/raw_data/OB_PREV_ALL_STATES.xlsx')
rural = import_rural_data('../data/raw_data/County_Rural_Lookup.xlsx')
alcohol = import_alc_data('../data/raw_data/IHME_USA_COUNTY_ALCOHOL_USE_PREVALENCE_2002_2012_NATIONAL_Y2015M04D23.XLSX')

#  --- MERGE ALL DATA  ---

#iterable of all feature dfs
feat_dfs = {
"census": census,
"unemp": unemp,
"foodenv" : foodenv,
"poverty": poverty,
"inactivity" : inactivity,
"obesity" : obesity,
"rural" : rural,
"alcohol" : alcohol
}

# dictionary of the fips column names for each feature dataframe
feats_fips_colnames = {}
for df_name in feat_dfs.keys():
    feats_fips_colnames[df_name] = [col for col in feat_dfs[df_name].columns if col.lower().startswith('fip')][0]
feats_fips_colnames

# merge!
merged_df = diabetes
for df_name in feat_dfs.keys():
    merged_df = _merge_on_fips(merged_df, df_name, feats_fips_colnames)


#  ----- INITAL SCRUBBING  ------

#removing Puerto Rico --> not including in analysis, too many features missing
merged_df = merged_df[merged_df['State_master'] != "Puerto Rico"]

#removing rows without diabetes 2013 info (i.e. missing target information)
merged_df = merged_df[merged_df['DB:2013:percent'].isnull() == False]

#create target
merged_df['Diabetes_pct_growth_rate'] = ((merged_df["DB:2013:percent"] - merged_df["DB:2010:percent"]) *100) / merged_df["DB:2010:percent"]

#removing duplicative columns
#including
desired_merged_columns = ['State_master', 'FIPS_master', 'County_master', 'DB:2009:percent', 'DB:2010:percent', 'TOT_POP',
        'TOT_MALE', 'WAC_MALE', 'WAC_FEMALE', 'BAC_MALE',
       'BAC_FEMALE', 'IAC_MALE', 'IAC_FEMALE', 'AAC_MALE', 'AAC_FEMALE',
       'NAC_MALE', 'NAC_FEMALE', 'H_MALE', 'H_FEMALE', 'AgeGrp01:0-4:2010',
       'AgeGrp02:5-9:2010', 'AgeGrp03:10-14:2010', 'AgeGrp04:15-19:2010',
       'AgeGrp05:20-24:2010', 'AgeGrp06:25-29:2010', 'AgeGrp07:30-34:2010',
       'AgeGrp08:35-39:2010', 'AgeGrp09:40-44:2010', 'AgeGrp10:45-49:2010',
       'AgeGrp11:50-54:2010', 'AgeGrp12:55-59:2010', 'AgeGrp13:60-64:2010',
       'AgeGrp14:65-69:2010', 'AgeGrp15:70-74:2010', 'AgeGrp16:75-79:2010',
       'AgeGrp17:80-84:2010', 'AgeGrp18:85+:2010', 'UnemploymentRate:2010',
       'PCT_LACCESS_POP10', 'FFRPTH09', 'Poverty_Rate_2010',
       'LI:2009:percent', 'LI:2010:percent',  'OB:2009:percent', 'OB:2010:percent',
        'Rural_percent_2010', 'Alcohol:Any:2010', 'Alcohol:Heavy:2010', 'Diabetes_pct_growth_rate']

merged_df = merged_df[desired_merged_columns]

#export all final data (to be used for visualizations, plotting, etc)
merged_df.to_csv('../data/ALL_MERGED_DATA.csv')


#  --- TRAIN TEST  SPLIT  ---

X = merged_df.drop(['Diabetes_pct_growth_rate','State_master', 'FIPS_master', 'County_master'], axis = 1)
y = merged_df['Diabetes_pct_growth_rate']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=30)

#export all training and test sets. Only training to be used for model selection and fitting.
X_train.to_csv('../data/X_train.csv')
X_test.to_csv('../data/X_test.csv')
y_train.to_csv('../data/y_train.csv')
y_test.to_csv('../data/y_test.csv')



'''

LATER:
#CHANGE DIABETES GROWTH TO --> % POPULATION THAT IS NEW TO DIABETES? (i.e. total diabetes pop #s?)

#per second pass, adding Diabetes growth rate TARGET

#new for third pass: adding percent increase 2009-2010
third_pass['DDP:2009-2010:Growth_Rate'] = (third_pass["DDP:2010:percent.6"] - third_pass["DDP:2009:percent.5"]) / third_pass["DDP:2009:percent.5"]

ob2['OB:2009-2010:Change_rate'] = ( ob2['OB:2010:percent'] - ob2['OB:2009:percent'] ) / ob2['OB:2009:percent']

#create % male population
census["Male_pct_2010"] =  (census["TOT_MALE"] / census["TOT_POP"])*100

creating not M/F census_
r_e_df['CEN:2010:WA'] = (r_e_df['WA_MALE'] + r_e_df['WA_FEMALE']) / r_e_df["TOT_POP"]
r_e_df['CEN:2010:BA'] = (r_e_df['BA_MALE'] + r_e_df['BA_FEMALE']) / r_e_df["TOT_POP"]
r_e_df['CEN:2010:IA'] = (r_e_df['IA_MALE'] + r_e_df['IA_FEMALE']) / r_e_df["TOT_POP"]
r_e_df['CEN:2010:AA'] = (r_e_df['AA_MALE'] + r_e_df['AA_FEMALE']) / r_e_df["TOT_POP"]
r_e_df['CEN:2010:NA'] = (r_e_df['NA_MALE'] + r_e_df['NA_FEMALE']) / r_e_df["TOT_POP"]
r_e_df['CEN:2010:WAC'] = (r_e_df['WAC_MALE'] + r_e_df['WAC_FEMALE']) / r_e_df["TOT_POP"]
r_e_df['CEN:2010:BAC'] = (r_e_df['BAC_MALE'] + r_e_df['BAC_FEMALE']) / r_e_df["TOT_POP"]
r_e_df['CEN:2010:IAC'] = (r_e_df['IAC_MALE'] + r_e_df['IAC_FEMALE']) / r_e_df["TOT_POP"]
r_e_df['CEN:2010:AAC'] = (r_e_df['AAC_MALE'] + r_e_df['AAC_FEMALE']) / r_e_df["TOT_POP"]
r_e_df['CEN:2010:NAC'] = (r_e_df['NAC_MALE'] + r_e_df['NAC_FEMALE']) / r_e_df["TOT_POP"]
r_e_df['CEN:2010:H'] = (r_e_df['H_MALE'] + r_e_df['H_FEMALE']) / r_e_df["TOT_POP"]

Age:
Age:0-14', 'Age:15-24', 'Age:25-44',
'Age:45+'


#changed for rural:
#Kusilvak --> 2158 to 2270
#Oglala --> 46102 to 46113



#WILL NEED A PLAN FOR MISSING UNEMPLYOMENT RATE, AND MSSING POVERTY RATE

#5 big_df.loc[[86, 87, 94, 95, 322, 551, 2420]][["FIPS_y", "CountyState", "UnemploymentRate:2010" ]]
#1 big_df.loc[322][["FIPS_y", "State_y", "County_y", "Poverty_Rate_2010"]]

'''

'''
Al files:
CDC:
# - Diabetes   'DDP:2010:percent.6', 'DDP:2009-2010:Growth_Rate', *TARGET*
# - obesity    OB:2010:percent', 'OB:2009-2010:Change_rate'
# - inactivity  LI:2010:percent

## Poverty   'Poverty Rate 2010''
## unemployment   '2010:UnemploymentRate'
# foodenvatlas   ''FFRPTH09', PCT_LACCESS_POP10'
# rural   Rural_Pct_2010
# alcohol   'Alcohol:Any:2010', 'Alcohol:Heavy:2010',
# (fips)  (States?)
# census  'pct_male', 'CEN:2010:BAC', 'CEN:2010:IAC',
'CEN:2010:AAC', 'CEN:2010:NAC', 'CEN:2010:H','Age:0-14', 'Age:15-24', 'Age:25-44',
'Age:45+'

'''
