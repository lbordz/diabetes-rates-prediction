'''
Final running of model against test set
'''

if __name__ == '__main__':
    import pandas as pd
    import numpy as np

    from _data_cleaning import *
    from model import Diabetes_Rate_Model

    #import and transform data
    X_train = clean_reformat_features('../data/X_train.csv')
    y_train = pd.read_csv('../data/y_train.csv')["y_train"]
    X_test = clean_reformat_features('../data/X_test.csv')
    y_test = pd.read_csv('../data/y_test.csv')["y_test"]

    #fit model on training
    model = Diabetes_Rate_Model()
    model.fit_linear(X_train, y_train)
    model.fit_ensemble(X_train, y_train)


    #output predictions with county and state names
    pred_linear = model.predict_linear(X_test)
    pred_ensemble = model.predict_ensemble(X_test)


    #print scores

    linear_rmse = model.rmse(y_test, pred_linear)
    ensemble_rmse = model.rmse(y_test, pred_ensemble)
    print (f"RMSE of baseline (guess average): {model.rmse_avg}")
    print (f"Linear RMSE on test set: {linear_rmse}, {model.rmse_pct_improvement(y_test,pred_linear )} change from baseline")
    print (f"Ensemble RMSE on test set: {ensemble_rmse}, {model.rmse_pct_improvement(y_test,pred_ensemble )} change from baseline")



    # #table of predictions vs actual values by state and county
    # fips = pd.read_csv('../data/county_fips_mapping.csv')
    #
    # X_test_county_name_merge = X_test.merge(fips, left_on = 'FIPS_master', right_on = "fips", how = "left")#   ('state', 'county')
    # X_test_pred = pd.DataFrame({'state': X_test_county_name_merge['state'],
    #                         'county': X_test_county_name_merge['county'],
    #                         'pred_linear': pred_linear,
    #                         'pred_ensemble': pred_ensemble,
    #                         'actual': y_test})
    #
    #
    # X_test_pred['pred_linear_rank'] = X_test_pred.shape[0] + 1  - X_test_pred["pred_linear"].rank()
    # X_test_pred['pred_ensemble_rank'] = X_test_pred.shape[0] + 1  - X_test_pred["pred_ensemble"].rank()
    # X_test_pred['actual_rank'] = X_test_pred.shape[0] + 1  - X_test_pred["actual"].rank()
    #
    # print (X_test_pred.sort_values(by = "actual", ascending = False))
