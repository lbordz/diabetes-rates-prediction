import pandas as pd
import numpy as np


'../data/X_train.csv'



# ----- HELPER FUNCTIONS ----

def _create_df_dummy_states(df, state_col_name):
    return pd.get_dummies(df[state_col_name], prefix='ST:')


def clean_reformat_features(filepath):

    df = ****FILEPATH***

    #state dummies
    states = _create_df_dummy_states(df, "State_master")
    df = df.join(states)

    #reduce ages into fewer Grps(otherwise high correlation)
    df['Age:0-14'] = df['AgeGrp01:0-4:2010'] +  df['AgeGrp02:5-9:2010'] + df['AgeGrp03:10-14:2010']
    df['Age:15-24'] = df['AgeGrp04:15-19:2010'] +  df['AgeGrp05:20-24:2010']
    df['Age:25-44'] = df['AgeGrp06:25-29:2010'] +  df['AgeGrp07:30-34:2010'] + df['AgeGrp08:35-39:2010'] +  df['AgeGrp09:40-44:2010']
    df['Age:45+'] = df['AgeGrp10:45-49:2010'] + df['AgeGrp11:50-54:2010'] + df['AgeGrp12:55-59:2010'] + df['AgeGrp13:60-64:2010'] + df['AgeGrp14:65-69:2010'] + df['AgeGrp15:70-74:2010'] + df['AgeGrp16:75-79:2010'] + df['AgeGrp17:80-84:2010'] + df['AgeGrp18:85+:2010']

    dropped_ages = ['AgeGrp01:0-4:2010', 'AgeGrp02:5-9:2010', 'AgeGrp03:10-14:2010',
       'AgeGrp04:15-19:2010', 'AgeGrp05:20-24:2010',
       'AgeGrp06:25-29:2010', 'AgeGrp07:30-34:2010',
       'AgeGrp08:35-39:2010', 'AgeGrp09:40-44:2010',
       'AgeGrp10:45-49:2010', 'AgeGrp11:50-54:2010',
       'AgeGrp12:55-59:2010', 'AgeGrp13:60-64:2010',
       'AgeGrp14:65-69:2010', 'AgeGrp15:70-74:2010',
       'AgeGrp16:75-79:2010', 'AgeGrp17:80-84:2010', 'AgeGrp18:85+:2010']

    for col in dropped_ages:
        df = df.drop(col, axis = 1)

        #NOPE!! NEXT IS TO MAKE WAC COLUMNS (NOT WAC< CAN LEAVE OFF)
    #remove WAC (high correlation with BAC, BAC performed slightly better)
    df = df.drop('CEN:2010:WAC', axis = 1)

'''

LATER:
#CHANGE DIABETES GROWTH TO --> % POPULATION THAT IS NEW TO DIABETES? (i.e. total diabetes pop #s?)

#new for third pass: adding percent increase 2009-2010
#third_pass['DDP:2009-Growth_Rate'] = (third_pass["DDP:2010:percent.6"] - third_pass["DDP:2009:percent.5"]) / third_pass["DDP:2009:percent.5"]

#ob2['OB:2009-2010:Change_rate'] = ( ob2['OB:2010:percent'] - ob2['OB:2009:percent'] ) / ob2['OB:2009:percent']

#create % male population
#census["Male_pct_2010"] =  (census["TOT_MALE"] / census["TOT_POP"])*100

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


#changed for rural:


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
