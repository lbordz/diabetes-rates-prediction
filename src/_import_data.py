import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join


'''
Al files:
CDC:
# - Diabetes   'DDP:2010:percent.6', 'DDP:2009-2010:Growth_Rate', *TARGET*
# - obesity    OB:2010:percent', 'OB:2009-2010:Change_rate'
# - inactivity  LI:2010:percent

# Poverty   'Poverty Rate 2010''
# unemployment   '2010:UnemploymentRate'
foodenvatlas   ''FFRPTH09', PCT_LACCESS_POP10'
rural   Rural_Pct_2010
alcohol   'Alcohol:Any:2010', 'Alcohol:Heavy:2010',
(fips)  (States?)
census  'pct_male', 'CEN:2010:BAC', 'CEN:2010:IAC',
'CEN:2010:AAC', 'CEN:2010:NAC', 'CEN:2010:H','Age:0-14', 'Age:15-24', 'Age:25-44',
'Age:45+'

'''

#Function to import diabetes, leisure inactiity, and obesity data

def _import_CDC_data(filepath, abbr):

    '''
    filepath: string, path to raw data file
    abbr: string, 2-3 letters to use to abbreviate data type
    cols: list of all columns needed for model and/or to create new features
    '''

    #import data
    data_df = pd.read_excel(filepath, skiprows=1)

    #rename features with corresponding years
    prefix = abbr + ':YEAR:'
    new_col_names_prefix = ['', '', '']
    for year in range (2004, 2014):
        year_specific_prefixs = [prefix.replace('YEAR', str(year))] * 7
        new_col_names_prefix = new_col_names_prefix + year_specific_prefixs
    new_col_names = np.array(new_col_names_prefix + data_df.columns)
    for i in range(10, len(new_col_names)):
        new_col_names[i] = new_col_names[i][:-2]  #removing the numbers at the end of column names
    data_df.columns = new_col_names
    return data_df



#----- IMPORT DESIRED INACTIVITY DATA FROM FILE-----#


def import_inactivity_data(filepath):
    #read file, rename columns
    li_data = _import_CDC_data(filepath, 'LI')

    li_data = li_data[['State', 'FIPS Codes', 'County', 'LI:2009:percent', 'LI:2010:percent']]

    #select desired columns only, change "No Data" to nulls
    for col in li_data.columns[3:]:
        li_data[col] = pd.to_numeric(li_data[col], errors = 'coerce')

    return li_data
    #missing step --> ob2 = ob2[ob2.isnull().sum(axis = 1) == 0]





#----- IMPORT DESIRED OBESITY DATA FROM FILE-----#


def import_obesity_data(filepath):
    #read file, rename columns
    ob_data = _import_CDC_data(filepath, 'OB')

    ob_data = ob_data[['State', 'FIPS Codes', 'County', 'OB:2009:percent', 'OB:2010:percent']]

    #select desired columns only, change "No Data" to nulls
    for col in ob_data.columns[3:]:
        ob_data[col] = pd.to_numeric(ob_data[col], errors = 'coerce')

    return ob_data
    #missing step --> ob2 = ob2[ob2.isnull().sum(axis = 1) == 0]



#----- IMPORT DESIRED DIABETES DATA FROM FILE-----#

def import_diabetes_data(filepath):
    #read file, rename columns
    diab_data = _import_CDC_data(filepath, 'DB')

    #select desired columns only, change "No Data" to nulls
    diab_data = diab_data[["State", "FIPS Codes", "County", "DB:2009:percent", "DB:2010:percent", "DB:2013:percent"]]
    for col in diab_data.columns[3:]:
        diab_data[col] = pd.to_numeric(diab_data[col], errors = 'coerce')

    return diab_data




#----- IMPORT DESIRED POVERTY DATA FROM FILE-----#

def import_poverty_data(filepath):
    pov_data = pd.read_excel(filepath, sheet_name = 'Data', skiprows = 1)

    #remove rows now with county-level data
    pov_data = pov_data[(pov_data["County"] != "Total") & (pov_data["County"] != "State Total")]

    #remove rows with notes, not data
    pov_data = pov_data[pov_data["FIPS"].isnull() == False]  #remove

    #change fips to be integer, to match other datasets
    pov_data['FIPS'] = pov_data["FIPS"].astype(int)

    #choose and rename needed columns
    pov_data = pov_data[["FIPS", "State", "County", "Poverty Rate 2010"]]
    pov_data.columns = ["FIPS", "State", "County", "Poverty_Rate_2010"]

    return pov_data


#----- IMPORT DESIRED UNEMPLOYMENT RATE DATA FROM FILE-----#

def import_unemployment_data(filedir):

    #get list of files from directory (one file per state)
    filenames = [f for f in listdir(filedir)]
    filenames.remove('.DS_Store')

    #create a dataframe for each state
    alldfs = []
    for filename in filenames:
        df = pd.read_excel(filedir + filename, skiprows = 1)

        #rename and reorganize columns
        first = ["FIPS"]
        second = [df.columns[1]]
        middle = list(df.columns[2:12].astype(str) + [":UnemploymentRate"])
        end = [df.columns[12]]
        endend = [df.columns[-1] + " (2017)"]
        df.columns = first + second + middle + end + endend

        #drop extra columns that mean nothing
        df.drop("None:UnemploymentRate", axis = 1, inplace = True)

        #drop first row, which is always the total for the STATE
        df.drop(index = 0, inplace = True)
        #add state df to the list of all dataframes
        alldfs.append(df)

    #create one master dataframe with all data
    master_df = pd.DataFrame(columns = alldfs[0].columns)
    for df in alldfs:
        master_df = master_df.append(df)

    #removing notes not associated with any county
    master_df = master_df[master_df['Name'].isnull() == False]

    #select columns
    master_df = master_df[["FIPS", "Name", "2010:UnemploymentRate"]]
    master_df.columns = ["FIPS", "CountyState", "UnemploymentRate:2010"]

    return master_df
