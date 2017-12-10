# predict.py

# This script should use the model in /tmp/iris_model.csv to predict X-values in /tmp/iris_test.csv

import pandas as pd
import numpy  as np
import cPickle as pickle

def read_from_pickle(file_path):
    with open(file_path, 'rb') as pickle_input:
        return pickle.load(pickle_input)

# I should get the data I want to predict:
test_df = pd.read_csv('/tmp/iris_test.csv')
terms_to_predict = test_df.columns
# I should get the model I created earlier:
#model_df = pd.read_csv('/tmp/iris_model.csv', index_col='model_term')
#model_terms = model_df.index.values
#print model_df

# Setting up the intercept column and filling with ones.
#test_df['intercept'] = np.ones(len(test_df))
#data_slice = np.array(test_df[model_terms])

for term_predicted in terms_to_predict:
    data_slice = np.array(test_df[[term for term in terms_to_predict if term != term_predicted]])
    model = read_from_pickle('/tmp/' + term_predicted + '_model.pkl')
    predictions = model.predict(data_slice)
    test_df[term_predicted + '_prediction'] = predictions
    '''if term_predicted != 'iris_type':
        # To use Linear Algebra to generate predictions from model and test-data, I matrix-multiply:
        weight_array = np.array(model_df.loc[:, term_predicted])

        predictions_a = np.matmul(data_slice, weight_array)

        # I should write the predictions to CSV in a way which helps me compare then to observations:
        test_df[term_predicted + '_prediction'] = predictions_a

    else:
        model_slice = model_df[[c for c in model_df.columns if 'iris_type' in c]]
        for i in range(0, 3):
            print test_df['iris_type']
            print np.matmul(test_df[model_terms], model_slice)'''

print test_df
test_df.to_csv('/tmp/iris_predictions.csv', float_format='%4.2f', index=False)

print('Predictions should be here: /tmp/iris_predictions.csv')
'bye'
