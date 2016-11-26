# compare.py

# This script should compare predicted f1 values from observed f1 values in /tmp/iris_test.csv

import pandas as pd
import numpy  as np
import pdb

# I should get the data I want to compare:
predicitons_df         = pd.read_csv('/tmp/iris_predicitons.csv')

predicitons_df['difference'] = predicitons_df.f1 - predicitons_df.prediction

predicitons_df['diff_squared'] = predicitons_df.difference ** 2

print('A comparison of observed values (f1) and predicitons:')
print(predicitons_df)

print('The square-root of the mean of differences-squared:')
print(np.mean(predicitons_df.diff_squared) ** 0.5)
print('Acronym for above calculation is "RMSE".')
print('For me, RMSE is a good way to compare observed values and predicitons.')
print('If RMSE is zero, the predictions are probably accurate.')

'bye'
