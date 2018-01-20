from learn import retrieve_train_test_data, read_from_pickle
import pandas as pd

if __name__ == "__main__":
    train_data, test_data = retrieve_train_test_data()
    model = read_from_pickle('/tmp/demand_model.pkl')

