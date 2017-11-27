import datetime
import pandas
import numpy as np

# DATASET = "test"
DATASET = "training"
NUM_SAMPLES = 10000


def get_single_column(file, column, nrows):
    df = pandas.read_csv(file, nrows=nrows)
    return {'dates': df[df.columns[0]],
            'values': df[df.columns[column]]}


def plot_matplot(dataframe):
    '''
    Plots data with matplotlib
    :param dataframe:
    :return:
    '''
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from mpl_toolkits.axes_grid1 import host_subplot
    import mpl_toolkits.axisartist as AA

    minutes = mdates.MinuteLocator("%M")  # every minute
    hours = mdates.HourLocator("%H")  # every month
    hourFmt = mdates.DateFormatter('%H')

    dates = df[df.columns[0]]
    values1 = df[df.columns[1]]
    values2 = df[df.columns[4]]
    values3 = df[df.columns[5]]
    values = [values1, values2]
    # plotting
    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(right=0.75)
    par1 = host.twinx()
    par2 = host.twinx()
    new_fixed_axis = par2.get_grid_helper().new_fixed_axis
    par2.axis["right"] = new_fixed_axis(loc="right",
                                        axes=par2,
                                        offset=(80, 0))
    par2.axis["right"].toggle(all=True)
    new_fixed_axis = par1.get_grid_helper().new_fixed_axis
    par1.axis["right"] = new_fixed_axis(loc="right",
                                        axes=par1,
                                        offset=(30, 0))
    par1.axis["right"].toggle(all=True)
    host.plot(dates, values3)
    par1.plot(values1)
    par2.plot(values2)
    # beautify the x-labels
    host.format_xdata = mdates.DateFormatter(' %Y-%m-%d  %H:%M:%S ')
    host.xaxis.set_major_locator(hours)
    host.xaxis.set_major_formatter(hourFmt)
    host.xaxis.set_minor_locator(minutes)
    #
    host.grid(True)
    plt.draw()
    plt.show()


def get_y_rangename(val):
    y_ranges = ["default", "hundreds", "thousands", "tt"]
    if -20 <= val <= 20: return y_ranges[0]
    if -100 <= val <= 100: return y_ranges[1]
    if -5000 <= val <= 5000:
        return y_ranges[2]
    else:
        return y_ranges[3]


def plot_bokeh(df, labels=None):
    """
    Plots data using bokeh
    :param df: dataframe
    :param labels: labels for dataframe indocating failure
    :return:
    """
    from bokeh.plotting import figure, output_file, save, show
    from bokeh.palettes import Spectral11 as color_palette
    from bokeh.models import LinearAxis, Range1d

    # the number of columns is the number of lines that we will make
    numlines = len(df.columns)
    print(numlines)

    # import color pallet
    mypalette = color_palette[0:numlines]
    print(len(mypalette))
    # make a list of our columns
    col = []
    [col.append(i) for i in df.columns[1:]]
    print(col)
    p = figure(x_axis_type="datetime", title="Sensor values {} data".format(DATASET),
               width=1080, height=720, y_range=(0, 15))
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = "units"
    p.extra_y_ranges = {"hundreds": Range1d(start=-0, end=80),
                        "thousands": Range1d(start=0, end=4000),
                        "tt": Range1d(start=0, end=60000)}
    p.add_layout(LinearAxis(y_range_name="hundreds"), 'left')
    p.add_layout(LinearAxis(y_range_name="thousands"), 'left')
    p.add_layout(LinearAxis(y_range_name="tt"), 'left')

    # loop through our columns and colours
    for (columnnames, colore) in zip(col, mypalette):
        print("Plotting line for {}".format(columnnames))
        p.line(df.datetime, df[columnnames],
               legend=columnnames,
               color=colore,
               y_range_name=get_y_rangename(df[columnnames][1]))

    # # creates an output file
    output_file("{}_data_{}_samples.html".format(DATASET, NUM_SAMPLES))

    # # save the plot
    save(p)
    show(p)


def read_dataframe(filename, nsamples=1000, usecols=None, has_labels = False):
    """

    :param filename: csv file to read, assuming no headers, datetime as first column (index), label as last
    :param nsamples: number of rows to read
    :param usecols: cols to read, if not specified -> all
    :return:    preprocessed dataframe, with columns named datetime, value(n)...
                labels -> from last column of csv
    """
    if usecols is None:
        df = pandas.read_csv(filename, nrows=nsamples, header=None)
    else:
        df = pandas.read_csv(filename, nrows=nsamples, header=None,
                             usecols=usecols)
    if has_labels:
        df.columns = ["datetime"] + ["value{}".format(i) for i in range(len(df.columns) - 2)] + ["labels"]
        labels = df["labels"]
        df = df[df.columns[:-1]]
        anomalies = [(i, l) for (i, l) in zip(df.datetime, labels.values) if l > 0]
        print(len(anomalies))
        print(anomalies)

    else:
        df.columns = ["datetime"] + ["value{}".format(i) for i in range(len(df.columns) - 1)]
        labels = None

    df.datetime = pandas.to_datetime(df.datetime)
    return df, labels

def check_labels(filename):
    labels_df = pandas.read_csv(filename, header=None, usecols=[0, 1, 42])
    # print(labels_df)
    anomalies = [i for (i,l) in zip(labels_df[labels_df.columns[0]], labels_df[labels_df.columns[-1]].values) if l > 0]
    print(len(anomalies))
    print(anomalies)



if __name__ == '__main__':
    # label_col = 42
    # rows_to_read = NUM_SAMPLES
    # cols_to_read = 5
    # used_cols = [i for i in range(cols_to_read + 1)] + [label_col]
    # df, labels = read_dataframe("../data/{}_data.csv".format(DATASET), NUM_SAMPLES)
    # # data
    # # plot_matplot(df)
    # plot_bokeh(df, labels)

    check_labels("../data/{}_data.csv".format(DATASET))
