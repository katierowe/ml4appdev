# predict.py

# This script should use the model in /tmp/iris_model.csv to predict X-values in /tmp/iris_test.csv

import pandas as pd
import numpy as np

import iris_tools


if __name__ == "__main__":
    # I should get the data I want to predict:
    test_df = pd.read_csv('/tmp/iris_test.csv')
    terms_to_predict = test_df.columns

    for term_predicted in terms_to_predict:
        data_slice = np.array(test_df[[term for term in terms_to_predict if term != term_predicted]])
        model = iris_tools.read_from_pickle('/tmp/' + term_predicted + '_model.pkl')
        predictions = model.predict(data_slice)
        test_df[term_predicted + '_prediction'] = predictions

    test_df.to_csv('/tmp/iris_predictions.csv', index=False)

    print('Predictions were stored here: /tmp/iris_predictions.csv')
