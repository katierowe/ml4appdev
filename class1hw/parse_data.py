"""
slice_train_test.py

This script slices iris.csv into /tmp/iris_train.csv and /tmp/iris_test.csv
"""

import pandas as pd
import iris_tools

# I should read iris.csv into a DataFrame:

if __name__ == "__main__":
    iris_raw_df = pd.read_csv('iris.csv')
    # Shuffle the original data set so training and test data are chosen at random:
    iris_shuffled_encoded_df = iris_raw_df.sample(frac=1).reset_index(drop=True)
    iris_type_dict = iris_tools.get_iris_type_dict()
    iris_shuffled_encoded_df.loc[:, 'iris_type'] = [iris_type_dict[t] for t in iris_shuffled_encoded_df['iris_type'].values]

    # Get the training data:
    train_df = iris_shuffled_encoded_df[0:140]

    # Get the test data:
    test_df = iris_shuffled_encoded_df[140:150]

    # Write to csv files:
    train_df.to_csv('/tmp/iris_train.csv', index=False)
    test_df.to_csv( '/tmp/iris_test.csv' , index=False)

    print('Train Data is here: /tmp/iris_train.csv')
    print('Test Data is here: /tmp/iris_test.csv' )
