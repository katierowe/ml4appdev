# predict.py

# This script should use the model in /tmp/iris_model.csv to predict X-values in /tmp/iris_test.csv

import pandas as pd
import numpy  as np
import pdb

test_df         = pd.read_csv('/tmp/iris_test.csv')
model_sr        = pd.read_csv('/tmp/iris_model.csv')
col1_l          = [1] * len(test_df)
test_df['col1'] = col1_l
test_a          = np.array(test_df[['col1','f0']])
model_a         = np.array(model_sr)

print(model_a)

'bye'

