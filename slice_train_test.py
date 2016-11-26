# slice_train_test.py

# This script should slice iris.csv into /tmp/iris_train.csv and /tmp/iris_test.csv

import pandas as pd
import pdb

# I should read iris.csv into a DataFrame:

iris0_df = pd.read_csv('iris.csv')
iris1_df = iris0_df[['f0','f1']]

# I should get the training data:

train_df = iris1_df[0:140]

# I should get the test data:

test_df = iris1_df[140:150]

# I should write to csv files:

train_df.to_csv('/tmp/iris_train.csv', float_format='%4.2f', index=False)
test_df.to_csv( '/tmp/iris_test.csv' , float_format='%4.2f', index=False)

print('Train Data should be here: /tmp/iris_train.csv')
print('Test  Data should be here: /tmp/iris_test.csv' )

'bye'
