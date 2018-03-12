import pandas as pd
from sklearn import linear_model, neural_network, svm, gaussian_process
import numpy as np
import cPickle as pickle
import plot_results


def read_from_pickle(file_path):
    with open(file_path, 'rb') as pickle_input:
        return pickle.load(pickle_input)

def dump_to_pickle(model, file_path):
    with open(file_path, 'wb') as output:
        pickler = pickle.Pickler(output, -1)
        pickler.dump(model)


def separate_train_test_data():
    raw_data = pd.read_csv('CISO_data.csv')
    raw_data = raw_data[pd.notnull(raw_data['demand'])]
    raw_data_shuffled = raw_data.sample(frac=1).reset_index(drop=True)

    train_len = int(0.8 * len(raw_data.index))
    train_data = raw_data_shuffled[:train_len]
    test_data = raw_data_shuffled[train_len:]
    train_data.to_csv('/tmp/CISO_train.csv')
    test_data.to_csv('/tmp/CISO_test.csv')

    return train_data, test_data

def retrieve_train_test_data():
    train_data = pd.read_csv('/tmp/CISO_train.csv')
    test_data = pd.read_csv('/tmp/CISO_test.csv')
    return train_data, test_data

def create_new_model(train_data):
    y = train_data['demand'].values
    x = train_data[features].values
    model = linear_model.LinearRegression()
    model.fit(x, y)

    #model = neural_network.MLPRegressor(hidden_layer_sizes=(1000))
    #model.fit(x, y)

    #model = gaussian_process.GaussianProcessRegressor()
    #model.fit(x, y)

    #dump_to_pickle(model, '/tmp/demand_model.pkl')
    print "Models have been trained and stored."
    return model

if __name__ == "__main__":

    # Step 1: organize training and test data sets.
    # train_data, test_data = separate_train_test_data()
    #features = ['day_of_week', 'month', 'day_of_month', 'hour_of_day', 'year',
    #            'previous_day_demand', 'SF temp', 'LA temp']
    features = ['day_of_week_sin', 'day_of_week_cos', 'weekday',
                'month_sin', 'month_cos', 'previous_week_demand',
                'day_of_month', 'hour_sin', 'hour_cos', 'year',
                'previous_day_demand', 'SF temp', 'LA temp',
                'SP15 EZ Gen DA LMP Peak wtd avg',
                'SP15 EZ Gen DA LMP Peak change',
                'NP15 EZ Gen DA LMP Peak wtd avg',
                'NP15 EZ Gen DA LMP Peak change'
                ]
    train_data, test_data = retrieve_train_test_data()
    model = create_new_model(train_data)

    # Test out the model:
    #model = read_from_pickle('/tmp/demand_model.pkl')
    x_test = test_data[features]
    predictions = model.predict(x_test)
    test_data['demand_predictions'] = predictions

    x_train = train_data[features]
    predictions = model.predict(x_train)
    RMSE_train = (np.sum((train_data['demand'] - predictions)**2 /
                          len(train_data.index))**0.5)
    print 'Training data prediction RMSE: {:.2f}'.format(RMSE_train)
    test_data['LOCAL_TIMESTAMP'] = pd.to_datetime(test_data['LOCAL_TIMESTAMP'])
    for pred in ['demand_forecast', 'demand_predictions']:
        RMSE_forecast = (np.sum((test_data['demand'] - test_data[pred])**2 /
                          len(test_data.index))**0.5)
        print pred + ' RMSE: {:.2f}'.format(RMSE_forecast)
        print 'pre-Oct 2016: '
        test_data_slice = test_data[test_data['LOCAL_TIMESTAMP'] < pd.Timestamp('1 October 2016')]
        RMSE_forecast = (np.sum((test_data_slice['demand'] - test_data_slice[pred]) ** 2 /
                            len(test_data_slice.index)) ** 0.5)
        print pred + ' RMSE: {:.2f}'.format(RMSE_forecast)
    #print test_data[['demand', 'demand_forecast', 'demand_predictions']]
    plot_results.plot_predictions(test_data)