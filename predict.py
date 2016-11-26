# predict.py

# This script should use the model in /tmp/iris_model.csv to predict X-values in /tmp/iris_test.csv

import pandas as pd
import numpy  as np
import pdb

# I should get the data I want to predict:
test_df         = pd.read_csv('/tmp/iris_test.csv')
# I should get the model I created earlier:
model_sr        = pd.read_csv('/tmp/iris_model.csv')
# To use Linear Algebra to generate predictions from model and test-data, I need a column of ones:
col1_l          = [1] * len(test_df)
test_df['col1'] = col1_l
x_a             = np.array(test_df[['col1','f0']])

# To use Linear Algebra to generate predictions from model and test-data, I matrix-multiply:
w_a             = np.array(model_sr)
predictions_a   = np.matmul(x_a,w_a)

# I should write the predictions to CSV in a way which helps me compare then to observations:
test_df['prediction'] = [prediction[0] for prediction in predictions_a]
test_df[['f0','f1','prediction']].to_csv('/tmp/iris_predicitons.csv', float_format='%4.2f', index=False)

print('Predictions should be here: /tmp/iris_predicitons.csv')
'bye'

