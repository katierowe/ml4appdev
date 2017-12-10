# learn.py

import pandas as pd
import numpy as np
from sklearn import linear_model
import cPickle as pickle

# This script should learn from /tmp/iris_train.csv
# I should assume that f1 column depends on f0 column.

def dump_to_pickle(model, file_path):
    with open(file_path, 'wb') as output:
        pickler = pickle.Pickler(output, -1)
        pickler.dump(model)


train_df = pd.read_csv('/tmp/iris_train.csv')
index = list(['intercept']) + list(train_df.columns)
columns = list(['intercept', 'f0', 'f1', 'f2', 'f3',
              'iris_type_0', 'iris_type_1','iris_type_2'])

model_df = pd.DataFrame(index=index,
                        columns=columns)

for var in train_df.columns:
    coeff_list = [col for col in train_df.columns if col != var]
    # I should collect independent variables in a nested list:
    x_l = np.array(train_df[coeff_list])

    if var == 'iris_type':
        model = linear_model.SGDClassifier()
        model.fit(x_l, train_df[var])
        dump_to_pickle(model, '/tmp/' + var + '_model.pkl')
        #for i in range(0,3):
        #    model_df.loc[['f0','f1','f2','f3'], 'iris_type_{:.0f}'.format(i)] = model.coef_[i]
        #    model_df.loc['intercept', 'iris_type_{:.0f}'.format(i)] = model.intercept_[i]
    else:
        # I should import linear_model:
        model = linear_model.LinearRegression()


        # I should call fit() to create the model:
        model.fit(x_l, train_df[var])
        dump_to_pickle(model, '/tmp/' + var + '_model.pkl')
        # I should save the model:
        #w0_f = model.intercept_
        ##w_l  = model.coef_
        #m_l  = [w0_f] + w_l.tolist()
        #m_sr = pd.Series(index=list(['intercept']) + coeff_list, data=m_l)
        #model_df[var] = m_sr
'''
model_df = model_df.fillna(0)
model_df.index.name = 'model_term'
model_filepath  = '/tmp/iris_model.csv'
model_df.to_csv(model_filepath, index_label='model_term')
print('Model saved to: '+ '/tmp/iris_model.csv')

'''