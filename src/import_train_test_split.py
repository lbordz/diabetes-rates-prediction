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

X = merged_df.drop(['Diabetes_pct_growth_rate', 'FIPS_master', 'County_master'], axis = 1)
y = merged_df['Diabetes_pct_growth_rate']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=30)

#export all training and test sets. Only training to be used for model selection and fitting.
X_train.to_csv('../data/X_train.csv', index = False)
X_test.to_csv('../data/X_test.csv', index = False)
y_train.to_csv('../data/y_train.csv', index = False, header = ["y_train"])
y_test.to_csv('../data/y_test.csv', index = False, header = ["y_test"])
