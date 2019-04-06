import pandas as pd
import numpy as np

from _data_cleaning import *


filepath_X = '../data/X_train.csv'
X_train = clean_reformat_features(filepath_X)
filepath_y = '../data/y_train.csv'
y_train = pd.read_csv(filepath_y)


from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge

from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor

from sklearn.model_selection import GridSearchCV

from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error

import statsmodels.api as sm
#import statsmodels.stats.api as sms
#from statsmodels.compat import lzip
from statsmodels.regression.linear_model import OLS #.fit_regularized


class Diabetes_Rate_Model():

    def __init__(self):
        self.scalar = StandardScaler()
        self.model =  Ridge(alpha = 10)

    def fit(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train

        self.scalar.fit(X_train)
        self.X_train_scaled = self.scalar.transform(X_train)
        self.model.fit(self.X_train_scaled, self.y_train)

    def predict(self, X):
        X_scaled = self.scalar.transform(X)
        return self.model.predict(X_scaled)

#    mse(y_true, y_pred):
#        return mean_squared_error(y_true,
