"""
learn.py

This script learns from /tmp/iris_train.csv. Based on the y_variable name it will
determine whether a regression or classification model should be used.
"""

import pandas as pd
import numpy as np
from sklearn import linear_model
import warnings

import iris_tools

# Filter warning deemed harmless: https://github.com/scipy/scipy/issues/5998
warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")


if __name__ == '__main__':
    train_df = pd.read_csv('/tmp/iris_train.csv')

    for y_var in train_df.columns:
        coeff_list = [col for col in train_df.columns if col != y_var]
        # I should collect independent variables in a nested list:
        X = np.array(train_df[coeff_list])

        if y_var == 'iris_type':
            model = linear_model.LogisticRegression()
        else:
            model = linear_model.LinearRegression()

            # I should call fit() to create the model:
        model.fit(X, train_df[y_var])
        iris_tools.dump_to_pickle(model, '/tmp/' + y_var + '_model.pkl')
    print "Models have been trained and stored."
