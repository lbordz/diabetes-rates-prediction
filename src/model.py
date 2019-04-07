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
        self.mse_avg = None

    def fit_linear(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train

        self.scalar.fit(X_train)
        self.X_train_scaled = self.scalar.transform(X_train)
        self.modellinear.fit(self.X_train_scaled, self.y_train)
        if not self.mse_avg:
            yavg = self.y_train.mean()
            y_pred_avg = np.array([yavg] * self.X_train.shape[0])
            self.mse_avg = mean_squared_error(y_train, y_pred_avg)


    def predict_linear(self, X):
        X_scaled = self.scalar.transform(X)
        return self.modellinear.predict(X_scaled)


    def fit_ensemble(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train
        self.modelensemble.fit(self.X_train, self.y_train)
        if not self.mse_avg:
            yavg = self.y_train.mean()
            y_pred_avg = np.array([yavg] * self.X_train.shape[0])
            self.mse_avg = mean_squared_error(y_train, y_pred_avg)

    def predict_ensemble(self, X):
        return self.modelensemble.predict(X)

    def mse(self, y_true, y_pred):
        return mean_squared_error(y_true, y_pred)

    def mse_pct_improvement(self, y_true, y_pred):
        mse = mean_squared_error(y_true, y_pred)
        return (mse - self.mse_avg) / self.mse_avg
