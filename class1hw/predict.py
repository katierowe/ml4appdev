# predict.py

# This script should use the model in /tmp/iris_model.csv to predict X-values in /tmp/iris_test.csv

import pandas as pd
import numpy as np
import cPickle as pickle

def read_from_pickle(file_path):
    with open(file_path, 'rb') as pickle_input:
        return pickle.load(pickle_input)

if __name__ == "__main__":
    # I should get the data I want to predict:
    test_df = pd.read_csv('/tmp/iris_test.csv')
    terms_to_predict = test_df.columns

    for term_predicted in terms_to_predict:
        data_slice = np.array(test_df[[term for term in terms_to_predict if term != term_predicted]])
        model = read_from_pickle('/tmp/' + term_predicted + '_model.pkl')
        predictions = model.predict(data_slice)
        test_df[term_predicted + '_prediction'] = predictions

    print test_df
    test_df.to_csv('/tmp/iris_predictions.csv', index=False)

    print('Predictions should be here: /tmp/iris_predictions.csv')
