# learn.py

import pandas as pd
import pdb
# This script should learn from /tmp/iris_train.csv

train_df = pd.read_csv('/tmp/iris_train.csv')

# I should collect independent variables in a list:
x_l = [[x_f] for x_f in train_df.f0]
print(x_l[:9])

# I should import linear_model
from sklearn import linear_model
linr_model = linear_model.LinearRegression()
linr_model.fit(x_l, train_df.f1)
# That was easy. I needed only 3 lines of syntax.

print('scikit-learn calculates W to be:')
print(linr_model.coef_[0])
print('scikit-learn calculates b to be:')
print(linr_model.intercept_)

'bye'

