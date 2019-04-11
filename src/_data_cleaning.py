import pandas as pd
import numpy as np




# ----- HELPER FUNCTIONS ----

def _create_df_dummy_states(df, state_col_name):
    return pd.get_dummies(df[state_col_name], prefix='ST:')

def _drop_cols(df, col_names):
    for col in col_names:
        df = df.drop(col, axis = 1)
    return df


## ------ CLEANING FEATURES ----- #

def clean_reformat_features(filepath):

    df = pd.read_csv(filepath)

    #state dummies
    states = _create_df_dummy_states(df, "State_master")
    #if state dummies missing a state, add the column with all zeros
    all_states = ['ST:_Alabama', 'ST:_Alaska', 'ST:_Arizona', 'ST:_Arkansas',
       'ST:_California', 'ST:_Colorado', 'ST:_Connecticut', 'ST:_Delaware',
       'ST:_District of Columbia', 'ST:_Florida', 'ST:_Georgia', 'ST:_Idaho',
       'ST:_Illinois', 'ST:_Indiana', 'ST:_Iowa', 'ST:_Kansas', 'ST:_Kentucky',
       'ST:_Louisiana', 'ST:_Maine', 'ST:_Maryland', 'ST:_Massachusetts',
       'ST:_Michigan', 'ST:_Minnesota', 'ST:_Mississippi', 'ST:_Missouri',
       'ST:_Montana', 'ST:_Nebraska', 'ST:_Nevada', 'ST:_New Hampshire',
       'ST:_New Jersey', 'ST:_New Mexico', 'ST:_New York',
       'ST:_North Carolina', 'ST:_North Dakota', 'ST:_Ohio', 'ST:_Oklahoma',
       'ST:_Oregon', 'ST:_Pennsylvania', 'ST:_Rhode Island',
       'ST:_South Carolina', 'ST:_South Dakota', 'ST:_Tennessee', 'ST:_Texas',
       'ST:_Utah', 'ST:_Vermont', 'ST:_Virginia', 'ST:_Washington',
       'ST:_West Virginia', 'ST:_Wisconsin', 'ST:_Wyoming', 'ST:_Hawaii']
    for state_col in all_states:
         if state_col not in states.columns:
             states[state_col] = [0] * states.shape[0]

    df = df.join(states)
    df = _drop_cols(df, ['State_master', 'ST:_Hawaii'])



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

    df = _drop_cols(df, dropped_ages)

    #add % male feature
    df["Male_pct_2010"] =  (df["TOT_MALE"] / df["TOT_POP"])*100
    df = _drop_cols(df, ['TOT_MALE'])

    #create rate change features for diabetes and obesity, remove non-needed
    df['DB:2009-2010:Rate_Change'] = (df["DB:2010:percent"] - df['DB:2009:percent']) / df['DB:2009:percent']
    df['OB:2009-2010:Rate_Change'] = (df["OB:2010:percent"] - df['OB:2009:percent']) / df['OB:2009:percent']
    df['LI:2009-2010:Rate_Change'] = (df["LI:2010:percent"] - df['LI:2009:percent']) / df['LI:2009:percent']

    df = _drop_cols(df, ['DB:2009:percent', 'OB:2009:percent', 'LI:2009:percent'])

    #reformat census columns
    # --> combine male.female into one
    census_col_prefixes = ['BAC', 'IAC', 'AAC', 'NAC', 'H']
    for race in census_col_prefixes:
        df['CEN:2010:' + race] = (df[race + '_MALE'] + df[race + '_FEMALE']) / df["TOT_POP"]
        df = _drop_cols(df, [race + '_MALE', race + '_FEMALE'])
    # --> remove columns no longer needed (WAC was heavily correlated with BAC, BAC performed better)
    df = _drop_cols(df, ['TOT_POP', 'WAC_MALE', 'WAC_FEMALE'])

    #fill in missing values *only 5 in training and test set, across differnet rows
    df.fillna(df.mean(), inplace = True)

    return df



if __name__ == '__main__':
    filepath_X = '../data/X_train.csv'
    X_train = clean_reformat_features(filepath_X)
    filepath_y = '../data/y_train.csv'
    y_train = pd.read_csv(filepath_y)

'''



def scale_data()
scalar = StandardScaler()


#SCALE!

FOR MODEL FIT / TRNAFORMS --> MUST SCALE DATA THERE!!!!! (BC MUST BE FIT TO TRIAN)

'''
