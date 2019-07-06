import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


class Diabetes_Rate_Model():

    def __init__(self):
        self.scalar = StandardScaler()
        self.modellinear =  Lasso(alpha =  .5, max_iter = 1000)
        self.modelensemble = RandomForestRegressor(max_depth = 20, min_samples_leaf = 5, n_estimators = 1000)
        self.rmse_avg = None

    def fit_linear(self, X_train, y_train):
        try:
            self.X_train = X_train.drop("FIPS_master", axis = 1)
        except:
            self.X_train = X_train
        self.y_train = y_train
        #print (self.X_train.shape)
        self.scalar.fit(self.X_train)
        self.X_train_scaled = self.scalar.transform(self.X_train)
        self.modellinear.fit(self.X_train_scaled, self.y_train)
        if not self.rmse_avg:
             yavg = self.y_train.mean()
             y_pred_avg = np.array([yavg] * self.X_train.shape[0])
             self.rmse_avg = self.rmse(y_train, y_pred_avg)


    def predict_linear(self, X):
        try:
            X = X.drop("FIPS_master", axis = 1)
        except:
            pass
        X_scaled = self.scalar.transform(X)
        return self.modellinear.predict(X_scaled)


    def fit_ensemble(self, X_train, y_train):
        try:
            self.X_train = X_train.drop("FIPS_master", axis = 1)
        except:
            self.X_train = X_train
        self.y_train = y_train
        self.modelensemble.fit(self.X_train, self.y_train)
        if not self.rmse_avg:
            yavg = self.y_train.mean()
            y_pred_avg = np.array([yavg] * self.X_train.shape[0])
            self.rmse_avg = self.rmse(y_train, y_pred_avg)

    def predict_ensemble(self, X):
        try:
            X = X.drop("FIPS_master", axis = 1)
        except:
            pass
        return self.modelensemble.predict(X)

    def rmse(self, y_true, y_pred):
        return (mean_squared_error(y_true, y_pred)) ** (1/2)

    def rmse_pct_improvement(self, y_true, y_pred):
        rmse = (mean_squared_error(y_true, y_pred)) ** (1/2)
        return (rmse - self.rmse_avg) / self.rmse_avg
