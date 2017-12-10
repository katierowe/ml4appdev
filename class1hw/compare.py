# compare.py

# This script should compare predicted f1 values from observed f1 values in /tmp/iris_test.csv

import pandas as pd
import numpy  as np

# I should get the data I want to compare:
predictions_df = pd.read_csv('/tmp/iris_predictions.csv')

predictions_df['difference'] = predictions_df.f1 - predictions_df.f1_prediction

predictions_df['diff_squared'] = predictions_df.difference ** 2

print('A comparison of observed values (f1) and predictions:')
print(predictions_df)

print('The square-root of the mean of differences-squared:')
print(np.mean(predictions_df.diff_squared) ** 0.5)
print('Acronym for above calculation is "RMSE".')
print('For me, RMSE is a good way to compare observed values and predictions.')
print('If RMSE is zero, the predictions are probably accurate.')

'bye'
