import matplotlib.pyplot as plt
import pandas as pd

import parse_data
import predict

iris_raw_df = pd.read_csv('iris.csv')
iris_type_dict = parse_data.get_iris_type_dict()
feature_columns = [col for col in iris_raw_df.columns if col != 'iris_type']
iris_raw_df.loc[:, 'iris_code'] = [iris_type_dict[t] for t in iris_raw_df['iris_type'].values]

model = predict.read_from_pickle('/tmp/iris_type_model.pkl')
iris_raw_df.loc[:, 'predicted_iris_code'] = model.predict(iris_raw_df[feature_columns])

correct_iris_df = iris_raw_df[iris_raw_df['iris_code']==iris_raw_df['predicted_iris_code']]
incorrect_iris_df = iris_raw_df[iris_raw_df['iris_code']!=iris_raw_df['predicted_iris_code']]

fig, axes = plt.subplots(3, 3)
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
                ax.set_xlabel('f{:.0f}'.format(x))
                if x == 0:
                    ax.set_ylabel('f{:.0f}'.format(y))
axes[1, 1].legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 10})
fig.delaxes(axes[1, 2])
fig.delaxes(axes[0, 2])
fig.delaxes(axes[0, 1])
fig.suptitle('Iris type predictions')
fig.savefig('iris_colors.pdf')