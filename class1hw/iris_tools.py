import cPickle as pickle

def get_iris_type_dict():
    return {'setosa':0, 'virginica':1, 'versicolor':2}


def read_from_pickle(file_path):
    with open(file_path, 'rb') as pickle_input:
        return pickle.load(pickle_input)

def dump_to_pickle(model, file_path):
    with open(file_path, 'wb') as output:
        pickler = pickle.Pickler(output, -1)
        pickler.dump(model)
