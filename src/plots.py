import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import _data_cleaning as dc
import model as m

import seaborn as sns



# ------- Functions for plotting top features ----- #


def _weights_coefs_df(weights, column_names, label_dict,
                     color_above_0 = "tomato",
                     color_below_0 = "salmon", ):
    df = pd.DataFrame.from_dict({"features" : column_names,
                             "weights" : weights })
    df = df.reindex(df["weights"].abs().sort_values().index)[::-1]
    df["color"] = df["weights"].apply(lambda x: color_above_0 if  x > 0 else color_below_0)
    df["labels"] = df["features"].apply(lambda x: label_dict[x] if x in label_dict.keys() else x)
    return df


def _plot_save_top_features(weights, labels, colors,
                           top_num = 20,
                           save_filepath = None,
                           figsize = (7, 10),
                           xlabel = None,
                           title = None):
    plt.figure(figsize = figsize)
    plt.barh(labels.iloc[:top_num], height = .85, width = weights.iloc[:top_num],
            color = colors, align='center')
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    if xlabel:
        plt.xlabel(xlabel, fontsize=20)
    if title:
        plt.title(title, fontsize=25, pad = 40)
    plt.gca().invert_yaxis()

    if save_filepath:
        plt.savefig(save_filepath, bbox_inches="tight")

def plot_top_features(weights, column_names, label_dict,
                      color_above_0,
                      top_num = 20,
                      save_filepath = None,
                      figsize = (7, 10),
                      xlabel = None,
                      title = None,
                     ):
    #1 create sorted dataframe
    df = _weights_coefs_df(weights, column_names, label_dict, color_above_0)
    #2 plot
    _plot_save_top_features(df['weights'], df['labels'], df['color'],
                           top_num = top_num, save_filepath = save_filepath,
                           figsize = figsize, xlabel = xlabel, title = title)




if __name__ == '__main__':
    sns.set()

    #import training dataset
    filepath_X = '../data/X_train.csv'
    X_train = dc.clean_reformat_features(filepath_X)
    filepath_y = '../data/y_train.csv'
    y_train = pd.read_csv(filepath_y)

    #creat and fit models
    model = m.Diabetes_Rate_Model()
    model.fit_linear(X_train, y_train)
    model.fit_ensemble(X_train, y_train.values)

    #readable column names (so feature names on plots look nice)
    cols_readable = { "DB:2010:percent":"Diabetes Rate in 2010",
                 "DB:2009-2010:Rate_Change":"Change in Diabetes Rate 2009-2010",
                 "OB:2009-2010:Rate_Change" : "Change in Obesity Rate 2009-2010",
                 "UnemploymentRate:2010": "Unemployment Rate 2010",
                 "LI:2010:percent":"Leisure Inactivity Rate 2010",
                 "LI:2009-2010:Rate_Change":"Change in Leisure Inactivity Rate 2009-2010",
                 "OB:2010:percent" : "Obesity Prevalance 2010",
                 "ST:_Texas":"Texas",
                 "ST:_Iowa":"Iowa",
                 "ST:_Idaho":"Idaho",
                 "ST:_Ohio":"Ohio",
                 "ST:_Virginia":"Virginia",
                 "ST:_Colorado":"Colorado",
                 "ST:_Iowa":"Iowa",
                 "ST:_Alaska":"Alaska",
                 "ST:_Indiana":"Indiana",
                 "ST:_South Carolina":"South Carolina",
                 "ST:_Wyoming":"Wyoming",
                 "CEN:2010:H":"Percent Hispanic 2010",
                 "Alcohol:Any:2010":"Any Alcohol Use 2010",
                 "Alcohol:Heavy:2010":"Heavy Alcohol Use 2010",
                 "ST:_Tennessee": "Tennesse",
                 "PCT_LACCESS_POP10" : "Low Access to groceries (%) 2010",
                 "FFRPTH09" :    "Fast Food per capita (2009)"  ,
                 "Poverty_Rate_2010"    :    "Poverty Rate 2010" ,
                 "Male_pct_2010" : "Male (%) 2010"  ,
                 "CEN:2010:H" : "Hispanic (%) 2010",
                 "Rural_percent_2010" : "Rural (%) 2010" ,
                 "ST:_Alabama" : "Alabama",
                 "CEN:2010:NAC" : "Native Hawaiian / Pactific Islander (%) 2010"
             }

    # Plot and save Top Lasso Coefficients
    plot_top_features(model.modellinear.coef_, X_train.columns, cols_readable,
                      color_above_0 = "tomato",
                      top_num = 15,   #20 for presentation, 15 for readme
                      figsize = (7, 9),    #used (7, 10) for presentation, (7, 9) for readme
                      xlabel = "Coefficient",
                      title ="Best Predictors of Diabetes Rate Change \n Lasso Regression Model" ,
                      save_filepath = '../images/top_lasso_pred.png'
                    )
    #Plot and save top Random Forest features per feature importance
    plot_top_features(model.modelensemble.feature_importances_, X_train.columns, cols_readable,
                      color_above_0 = "teal",
                      top_num = 5,
                      figsize = (7, 3),   #used (7, 4) for presentation, (7, 3) for readme
                      xlabel = "Feature Importance",
                      title ="Best Predictors of Diabetes Rate Change \n Random Forest Model",
                      save_filepath = '../images/top_rf_pred.png'  #../images/lassotop20.png
                    )
