# compare.py

# This script should compare predicted f1 values from observed f1 values in /tmp/iris_test.csv

import pandas as pd
import numpy  as np

# I should get the data I want to compare:
predictions_df = pd.read_csv('/tmp/iris_predictions.csv')
prediction_columns = [c for c in predictions_df if '_prediction' in c and 'iris_type' not in c]

for col in prediction_columns:
    variance = (predictions_df[col[0:2]] - predictions_df[col]) ** 2

    print('The RMSE for ' + col + ' model is:')
    print(np.mean(variance) ** 0.5)
