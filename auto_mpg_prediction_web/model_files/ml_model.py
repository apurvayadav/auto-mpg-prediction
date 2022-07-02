import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

# Functions

# preprocessing origin column
def preprocessing_org_column(df):
    df['Origin'] = df['Origin'].map({1 : 'India', 2 : 'USA', 3 : 'Germany'})
    return df

# Creating Custom Attribute adder
acc_ix, hpower_ix, cyl_ix = 4, 2, 0

class CustomAttrAdder(BaseEstimator, TransformerMixin):
    def __init__(self, acc_on_power = True):
        self.acc_on_power = acc_on_power
    def fit(self, X, y= None):
        return self
    def transform(self, X):
        acc_on_cyl = X[:, acc_ix] / X[:, cyl_ix]
        if self.acc_on_power:
            acc_on_power = X[:, acc_ix] / X[:, hpower_ix]
            return np.c_[X, acc_on_power, acc_on_cyl]

# pipelines
def num_pipeline_transformer(data):
    numerics = ['float64', 'int64']
    num_attrs = data.select_dtypes(include= numerics)
    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy= 'median')),
        ('attr_adder', CustomAttrAdder()),
        ('std_scaler', StandardScaler())
    ])
    return num_attrs, num_pipeline

def pipeline_transformer(data):
    cat_attrs = ['Origin']
    num_attrs, num_pipeline = num_pipeline_transformer(data)
    full_pipeline = ColumnTransformer([
        ('num', num_pipeline, list(num_attrs)),
        ('cat', OneHotEncoder(), cat_attrs)
    ])
    prepared_data = full_pipeline.fit_transform(data)
    return prepared_data

def predict_mpg(config, model):

    if type(config) == dict:
        df = pd.DataFrame(config)
    else:
        df = config

    preproc_df = preprocessing_org_column(df)
    prepared_df = pipeline_transformer(preproc_df)
    y_pred = model.predict(prepared_df)
    return y_pred