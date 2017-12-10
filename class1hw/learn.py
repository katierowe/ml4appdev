"""
learn.py

This script learns from /tmp/iris_train.csv. Based on the y_variable name it will
determine whether a regression or classification model should be used.
"""

import pandas as pd
import numpy as np
from sklearn import linear_model
import cPickle as pickle


def dump_to_pickle(model, file_path):
    with open(file_path, 'wb') as output:
        pickler = pickle.Pickler(output, -1)
        pickler.dump(model)


if __name__ == '__main__':
    train_df = pd.read_csv('/tmp/iris_train.csv')

    for y_var in train_df.columns:
        coeff_list = [col for col in train_df.columns if col != y_var]
        # I should collect independent variables in a nested list:
        X = np.array(train_df[coeff_list])

        if y_var == 'iris_type':
            model = linear_model.SGDClassifier()
        else:
            model = linear_model.LinearRegression()

            # I should call fit() to create the model:
        model.fit(X, train_df[y_var])
        dump_to_pickle(model, '/tmp/' + y_var + '_model.pkl')
