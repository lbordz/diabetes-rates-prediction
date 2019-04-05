import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import string
import requests
from bs4 import BeautifulSoup

'''
Al files:
CDC:
# - Diabetes   'DDP:2010:percent.6', 'DDP:2009-2010:Growth_Rate', *TARGET*
# - obesity    OB:2010:percent', 'OB:2009-2010:Change_rate'
# - inactivity  LI:2010:percent

## Poverty   'Poverty Rate 2010''
## unemployment   '2010:UnemploymentRate'
# foodenvatlas   ''FFRPTH09', PCT_LACCESS_POP10'
rural   Rural_Pct_2010
alcohol   'Alcohol:Any:2010', 'Alcohol:Heavy:2010',
# (fips)  (States?)
census  'pct_male', 'CEN:2010:BAC', 'CEN:2010:IAC',
'CEN:2010:AAC', 'CEN:2010:NAC', 'CEN:2010:H','Age:0-14', 'Age:15-24', 'Age:25-44',
'Age:45+'

'''


#----- SUPPORT FUNCTIONS-----#


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


def _replace_specific_values(df, col, from_to_dict):
    '''
    overwrites very specific values in a dataframe
    (useful for switching out specific county names, etc, to make everything match up)
    '''
    for item in from_to_dict.keys():
        value_index = df[df[col] == item].index
        df.loc[value_index, col] = from_to_dict[item]

def _lower_char_only(x):
    '''
    transformation function: returns string with only lowercase letters (no spaces)
    '''
    chars = string.ascii_lowercase
    return "".join([letter for letter in x.lower() if letter in chars])


def _remove_county_suffix(x):
    '''
    removes words like "county" and "borough" etc from county names. Helpful for aligning
    county names with FIPS codes.
    '''
    if (x.split(" ")[-2].lower() == 'and') and (x.split(" ")[-1].lower() == 'borough'):
        return " ".join(x.split(" ")[:-3])
    elif x.split(" ")[-1].lower() in ['county', 'parish', 'borough', 'municipality']:
        return " ".join(x.split(" ")[:-1])
    elif (x.split(" ")[-2].lower() == 'census') and (x.split(" ")[-1].lower() == 'area'):
        return " ".join(x.split(" ")[:-2])
    else:
        return " ".join(x.split(" "))



#----- IMPORT CENSUS DATA  -----#


def import_census_data(filepath):
    census = pd.read_csv(filepath, encoding = "ISO-8859-1")

    #filter for year = 2010
    census = census[census['YEAR'] == 1]

    #prepare census to merge with fips dataframe to get fips codes
    # --> replace specific county names to make them match fips dataframe
    census_changes = {"Kusilvak Census Area": "Wade Hampton Census Area",
             "District of Columbia" : "Washington County",
             "Doña Ana County" : "Dona Ana County",
            "Oglala Lakota County" : "Shannon County" }
    _replace_specific_values(census, "CTYNAME", census_changes)
    # --> remove "county" suffix and all non-lowercase characters
    census["ctynameshort"] = census["CTYNAME"].apply(_remove_county_suffix)
    census['ctynameshort'] = census['ctynameshort'].apply(_lower_char_only)

    #add fips codes
    fips = import_master_fips_list()
    census = census.merge(fips,  left_on = ["STNAME", "ctynameshort"], right_on = ["StateName","countyshort"], how = "left")

    #change names of ages
    age_changes = {
    0: "AgeTotal",
    1: "AgeGrp01:0-4:2010",
    2: "AgeGrp02:5-9:2010",
    3: "AgeGrp03:10-14:2010",
    4: "AgeGrp04:15-19:2010",
    5: "AgeGrp05:20-24:2010",
    6: "AgeGrp06:25-29:2010",
    7: "AgeGrp07:30-34:2010",
    8: "AgeGrp08:35-39:2010",
    9: "AgeGrp09:40-44:2010",
    10: "AgeGrp10:45-49:2010",
    11: "AgeGrp11:50-54:2010",
    12: "AgeGrp12:55-59:2010",
    13: "AgeGrp13:60-64:2010",
    14: "AgeGrp14:65-69:2010",
    15: "AgeGrp15:70-74:2010",
    16: "AgeGrp16:75-79:2010",
    17: "AgeGrp17:80-84:2010",
    18: "AgeGrp18:85+:2010",
    }
    _replace_specific_values(census, "AGEGRP", age_changes)

    #make a separate dataframe with one column for every age group
    age_df = census[["FIPS", "AGEGRP", "TOT_POP"]]
    age_df = age_df.set_index(['FIPS', 'AGEGRP'])
    age_df = age_df.unstack()
    age_df.columns = age_df.columns.droplevel()
    age_df = age_df.drop("AgeTotal", axis = 1)
    age_df = age_df.reset_index()

    #create a dataframe of just year = 0 as master
    census = census[census['AGEGRP'] == "AgeTotal"]
    census = census.merge(age_df, on = "FIPS", how = 'outer')

    #select only desired columns
    desired_columns = ['STNAME', 'CTYNAME', 'FIPS', 'TOT_POP', 'TOT_MALE', 'WAC_MALE', 'WAC_FEMALE',
       'BAC_MALE', 'BAC_FEMALE', 'IAC_MALE', 'IAC_FEMALE', 'AAC_MALE',
       'AAC_FEMALE', 'NAC_MALE', 'NAC_FEMALE','H_MALE', 'H_FEMALE', 'AgeGrp01:0-4:2010', 'AgeGrp02:5-9:2010',
       'AgeGrp03:10-14:2010', 'AgeGrp04:15-19:2010', 'AgeGrp05:20-24:2010',
       'AgeGrp06:25-29:2010', 'AgeGrp07:30-34:2010', 'AgeGrp08:35-39:2010',
       'AgeGrp09:40-44:2010', 'AgeGrp10:45-49:2010', 'AgeGrp11:50-54:2010',
       'AgeGrp12:55-59:2010', 'AgeGrp13:60-64:2010', 'AgeGrp14:65-69:2010',
       'AgeGrp15:70-74:2010', 'AgeGrp16:75-79:2010', 'AgeGrp17:80-84:2010',
       'AgeGrp18:85+:2010']

    return census[desired_columns]




    census = census.merge(fips[['StateCounty', "fips", "state", "county", 'census_CTYNAME']], on = "StateCounty", how = 'left')

def _match_census_counties():





#----- IMPORT FIPS CODES; NEEDED FOR CENSUS AND ___ DATA -----#



def import_master_fips_list():
    #get fips information from url
    url = 'https://www.nrcs.usda.gov/wps/portal/nrcs/detail/national/home/?cid=nrcs143_013697'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    table = soup.find("div", class_ = "centerColImg")
    #set column names for dataframe
    col_names = [x.text.replace("\r\n\t\t\t\t", "") for x in table.find('tr').find_all('th')]
    col_names[1] = "CountyName"
    #create rows for dataframe
    rows = []
    for tr in table.find_all('tr')[1:]:
        rows.append([x.text.replace("\r\n\t\t\t\t", "") for x in tr.find_all('td')])
    #create fips table
    fips = pd.DataFrame(rows, columns = col_names)
    #custom: add missing fips codes
    additional_fips = pd.DataFrame(
        np.array([["02105", "Hoonah-Angoon", "AK"],
                  ["02195", "Petersburg", "AK"],
                  ["02198", "Prince of Wales-Hyder", "AK"],
                  ["02230", "Skagway", "AK"],
                  ["02275", "Wrangell", "AK"],
                  ["08014", "Broomfield", "CO"],
                  ["12086", "Miami-Dade", "FL"],
                  ["15005", "Kalawao", "HI"]]),
        columns=['FIPS', 'CountyName', 'State'])
    fips = pd.concat([fips,additional_fips ], axis = 0).reset_index(drop = True)
    #custom: change typo
    fips_changes = {"Colonial Heights Cit" : "Colonial Heights City"}
    _replace_specific_values(fips, "CountyName", fips_changes)

    #add state names
    state_names = pd.read_csv('../data/raw_data/state_abbr.csv')
    fips = fips.merge(state_names, left_on = 'State', right_on = "abbr").drop("abbr", axis = 1)

    #add column of just lowercase character-only county names
    fips['countyshort'] = fips['CountyName'].apply(_lower_char_only)

    return fips



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



#----- IMPORT DESIRED FOOD ENVIRONMENT ATLAS RATE DATA FROM FILE-----#



def _food_env_get_sheetnum(filepath, desired_columns):
    '''
    find sheets associated with desired columns(), return a dictionary {column name: sheet number}
    '''
    sheetnums = {}
    found = 0
    for i in range (2, 12):
        sheet = pd.read_excel(filepath, sheet_name = i)
        for col in desired_columns:
            if col in sheet.columns:
                found += 1
                sheetnums[col] = i
                if found == len(desired_columns):
                    return sheetnums
    return sheetnums


def import_food_env_data(filepath, desired_columns):
    '''
    put desired columns from food atlas into one dataframe
    '''
    sheetnums = _food_env_get_sheetnum(filepath, ['PCT_LACCESS_POP10', 'FFRPTH09'])
    #create separate dataframe for each column, prepare to merge on FIPS as index
    dfs = []
    for col in sheetnums.keys():
        df = pd.read_excel(filepath, sheet_name = sheetnums[col])
        df = df[['FIPS', 'State', 'County', col ]]
        df.set_index('FIPS')
        dfs.append(df)
    #merge all dataframes on index (=FIPS)
    final_df = dfs[0]
    for df in dfs[1:]:
        final_df = pd.merge(final_df, df)

    return final_df
