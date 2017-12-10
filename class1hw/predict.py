# predict.py

# This script should use the model in /tmp/iris_model.csv to predict X-values in /tmp/iris_test.csv

import pandas as pd
import numpy  as np
import pdb

# I should get the data I want to predict:
test_df         = pd.read_csv('/tmp/iris_test.csv')
terms_to_predict = test_df.columns
# I should get the model I created earlier:
model_sr        = pd.read_csv('/tmp/iris_model.csv', index_col='model_term')
model_terms = model_sr.index.values
print terms_to_predict

intercept_col = [1] * len(test_df)
test_df['intercept'] = intercept_col

for term_predicted in terms_to_predict:
    if term_predicted != 'iris_type':
        # To use Linear Algebra to generate predictions from model and test-data, I need a column of ones:
        x_a             = np.array(test_df[model_terms])

        # To use Linear Algebra to generate predictions from model and test-data, I matrix-multiply:
        w_a             = np.array(model_sr.loc[:, term_predicted])
        predictions_a   = np.matmul(x_a,w_a)
        print predictions_a

        # I should write the predictions to CSV in a way which helps me compare then to observations:
        test_df[term_predicted + '_prediction'] = predictions_a

print test_df
test_df.to_csv('/tmp/iris_predicitons.csv', float_format='%4.2f', index=False)

print('Predictions should be here: /tmp/iris_predicitons.csv')
'bye'

