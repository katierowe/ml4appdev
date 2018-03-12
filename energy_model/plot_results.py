import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

def individual_plot(df, x_col, y_cols, ax, fig):
    for prediction in y_cols:
        percent_error = (df[prediction] - df['demand']) / df['demand']
        ax.plot(df[x_col], percent_error,
                'o', label=prediction)
    if 'TIMESTAMP' in x_col:
        fig.autofmt_xdate()


def plot_predictions(prediction_df):
    columns_to_plot = ['demand_forecast', 'demand_predictions']
    #columns_to_plot = ['demand_forecast']
    fig, ax = plt.subplots()
    individual_plot(prediction_df, 'LOCAL_TIMESTAMP',
                    columns_to_plot, ax, fig)
    ax.legend(loc='best')

    plt.savefig('prediction error.jpg')
    plt.close()

    font_p = FontProperties()
    font_p.set_size(6)
    fig = plt.figure(figsize=(10, 7))
    numrows = 3
    numcols = 4
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
              'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
              'Nov', 'Dec']
    for i, month in enumerate(months):
        ax = plt.subplot(numrows, numcols, i + 1)
        prediction_month = prediction_df[prediction_df.month == i + 1]
        individual_plot(prediction_month, 'hour_of_day',
                        columns_to_plot, ax, fig)
        ax.set_title(month)
        ax.set_ylim([-0.2, 0.2])
    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,
                        wspace=0.35)
    plt.savefig('prediction error by month.jpg')
