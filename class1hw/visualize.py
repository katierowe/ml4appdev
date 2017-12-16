import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import pandas as pd

import iris_tools

def get_and_sort_data():
    iris_raw_df = pd.read_csv('iris.csv')
    iris_type_dict = iris_tools.get_iris_type_dict()
    feature_columns = [col for col in iris_raw_df.columns if col != 'iris_type']
    iris_raw_df.loc[:, 'iris_code'] = [iris_type_dict[t] for t in iris_raw_df['iris_type'].values]

    model = iris_tools.read_from_pickle('/tmp/iris_type_model.pkl')
    iris_raw_df.loc[:, 'predicted_iris_code'] = model.predict(iris_raw_df[feature_columns])

    correct_iris_df = iris_raw_df[iris_raw_df['iris_code']==iris_raw_df['predicted_iris_code']]
    incorrect_iris_df = iris_raw_df[iris_raw_df['iris_code']!=iris_raw_df['predicted_iris_code']]

    return correct_iris_df, incorrect_iris_df

def plot_iris_data(correct_iris_df, incorrect_iris_df):
    iris_type_dict = iris_tools.get_iris_type_dict()
    fig, axes = plt.subplots(3, 3)
    loc = plticker.MultipleLocator(base=1.0) # this locator puts ticks at regular intervals
    colors = ['g', 'r', 'b']
    for i, key in enumerate(iris_type_dict.keys()):
        correct_iris_slice = correct_iris_df[correct_iris_df['iris_type']==key]
        incorrect_iris_slice = incorrect_iris_df[incorrect_iris_df['iris_type']==key]
        for x in range(0, 4):
            for y in range(0, 4):
                if x < y:
                    ax = axes[y-1, x]
                    ax.plot(correct_iris_slice['f{:.0f}'.format(x)],
                            correct_iris_slice['f{:.0f}'.format(y)], colors[i] + 'o',
                            label=key)
                    if len(incorrect_iris_slice.index) > 0:
                        ax.plot(incorrect_iris_slice['f{:.0f}'.format(x)],
                                incorrect_iris_slice['f{:.0f}'.format(y)], colors[i] + 'x',
                                label=key + ' misidentified')
                    if y - 1 == 2:
                        ax.set_xlabel('f{:.0f}'.format(x))
                    if x == 0:
                        ax.set_ylabel('f{:.0f}'.format(y))
                    ax.xaxis.set_major_locator(loc)
                    ax.tick_params(axis='both', which='major', labelsize=10)
    axes[1, 1].legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 10})
    fig.delaxes(axes[1, 2])
    fig.delaxes(axes[0, 2])
    fig.delaxes(axes[0, 1])
    fig.suptitle('Iris type predictions')
    fig.savefig('iris_colors.pdf')

if __name__ == "__main__":
    correct, incorrect = get_and_sort_data()
    plot_iris_data(correct, incorrect)
