import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
from matplotlib import cm
from pathlib import Path
import math
from pandas.plotting import scatter_matrix
import seaborn as sns
import matplotlib.gridspec as gs
import matplotlib.dates as mpldates


# GRAPHS THE COMBINATION FORMULA
def graph_combination_formula(n):

    numerator = np.math.factorial(n)
    results = [numerator / (np.math.factorial(k) * np.math.factorial(n - k)) for k in range(0, n + 1)]
    # PLOT RESULTS
    plt.plot(results)
    plt.ylabel('No. of combinations')
    plt.xlabel('Value of k')
    plt.show()


# returns best fit projected Y-value given input x-value based on bestfit line inputs (x_data, y_data, degree)
def getbestfitformula(x_data, y_data, degree):
    x = np.array(x_data)
    y = np.array(y_data)
    z = np.polyfit(x, y, degree)
    p = np.poly1d(z)
    return p


# returns projected y-value given x-input value and bestfit formula
def getprojectedyval(x_input, x_data, y_data, degree):
    p = getbestfitformula(x_data, y_data, degree)
    return p(x_input)


# graphs best fit formula given range of x vals and bestfit data and degree
def graphbestfitformula(xstart, xend, step, x_data, y_data, degree):
    # get bestfitformula
    p = getbestfitformula(x_data, y_data, degree)
    # get x array
    xarr = np.arange(xstart, xend, step)
    graphdf = pd.DataFrame(data={'xvals': xarr})
    graphdf['POLYN'] = p(graphdf['xvals'])
    # get df of original data
    origdf = pd.DataFrame(data={'xvals': x_data, 'origdata': y_data})
    graphdf.set_index(['xvals'], inplace=True)
    origdf.set_index(['xvals'], inplace=True)
    sns.lineplot(data=graphdf[['POLYN']])
    sns.scatterplot(data=origdf[['origdata']])
    plt.show()


# plot bar graph
def graphdataframe_bar(dataframe):
    sns.countplot(data=dataframe)
    plt.show()


# plot graph as choose col that would serve as x axis
def graphdataframe_line(xaxiscol, dataframe):
    # set date col as index for graphing purposes
    dataframe.set_index(xaxiscol, inplace=True)
    # graph
    sns.lineplot(data=dataframe)
    plt.show()


# SCATTER PLOT OF VARIABLE CORRELATIONS OF A DATAFRAME
def scattermatrix(dataframe):
    scatter_matrix(dataframe)
    plt.show()


# graph 3d surfaces
def graph3dsurface():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    X = np.arange(1, 22, 1)
    Y = np.arange(1, 13, 1)
    X, Y = np.meshgrid(X, Y)
    Z = Y - X
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    plt.show()


# graph 3d line
def graph3dline():
    fig = plt.figure()
    ax = plt.axes(projection="3d")
    z_line = np.linspace(0, 15, 1000)
    x_line = np.cos(z_line)
    y_line = np.sin(z_line)
    ax.plot3D(x_line, y_line, z_line, 'gray')


# graph 3d scatter surface
def graph3dscatter():
    fig = plt.figure()
    ax = plt.axes(projection="3d")
    x_points = np.arange(1, 22, 1)
    y_points = np.arange(1, 13, 1)
    z_points = resultdf.iat[math.floor(x_points), math.floor(y_points)]
    ax.scatter3D(x_points, y_points, z_points, c=z_points, cmap='hsv')
    plt.show()


# graph dataframe into surface
def graphdfsurface(my_dataframe):
    Y = np.arange(0, 21, 1)
    X = np.arange(0, 13, 1)
    Z = my_dataframe.values
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.contour3D(X, Y, Z)


# graphs two graphs side by side; sharing same x axis
def graphsidebyside_samexaxis(datadf, graph1col1, graph1col2, graph2col1):
    ax1 = plt.subplot(1, 2, 1)
    sns.lineplot(datadf[[graph1col1, graph1col2]])
    plt.subplot(1, 2, 2, sharex=ax1)
    sns.lineplot(datadf[[graph2col1]])
    plt.show()


# graphs two graphs side by side
def graphsidebyside(graph1df, graph2df, graph1cols, graph2cols):
    plt.subplot(121)
    sns.lineplot(data=graph1df[graph1cols])
    plt.subplot(122)
    sns.lineplot(data=graph2df[graph2cols])
    plt.show()


# graphs two graphs one of top with twice height as below with benchcompare group
def graphtopbottombenchcompare(graph1df, graph2df, graph1axis, graph2axis, graph1cols, graph1benchcols, graph2cols, heightratio, gridtop, gridbottom):
    spec2 = gs.GridSpec(nrows=2, ncols=1, height_ratios=heightratio)
    ax1 = plt.subplot(spec2[0, 0])
    copygraph1 = graph1df.copy()
    copygraph1.set_index([graph1axis], inplace=True)
    sns.lineplot(data=copygraph1[graph1cols])
    ax2 = plt.twinx()
    pal = sns.dark_palette('purple', 2)
    sns.lineplot(data=copygraph1[graph1benchcols], palette=pal)
    ax2.legend(loc=1)
    plt.grid(gridtop)
    plt.subplot(spec2[1, 0], sharex=ax1)
    copygraph2 = graph2df.copy()
    copygraph2.set_index([graph2axis], inplace=True)
    sns.lineplot(data=copygraph2[graph2cols])
    plt.grid(gridbottom)
    plt.show()


# graphs two graphs one of top with twice height as below
def graphtopbottom(graph1df, graph2df, graph1axis, graph2axis, graph1cols, graph2cols, heightratio, gridtop, gridbottom):
    spec2 = gs.GridSpec(nrows=2, ncols=1, height_ratios=heightratio)
    ax1 = plt.subplot(spec2[0, 0])
    copygraph1 = graph1df.copy()
    copygraph1.set_index([graph1axis], inplace=True)
    sns.lineplot(data=copygraph1[graph1cols])
    plt.grid(gridtop)
    plt.subplot(spec2[1, 0], sharex=ax1)
    copygraph2 = graph2df.copy()
    copygraph2.set_index([graph2axis], inplace=True)
    sns.lineplot(data=copygraph2[graph2cols])
    plt.grid(gridbottom)
    plt.show()


# HEATMAP THE DATAFRAME
def heatmap(heatmapsettings):
    sns.heatmap(heatmapsettings['heatmapregion'],
                xticklabels=heatmapsettings['xticklabels'],
                yticklabels=heatmapsettings['yticklabels'],
                annot=heatmapsettings['showcellvalues'],
                cmap=sns.color_palette(
                    heatmapsettings['colorpalette'],
                    as_cmap=True),
                cbar=heatmapsettings['colorbar'],
                center=heatmapsettings['centerval'],
                robust=True
                )
    plt.xlabel(heatmapsettings['xlabel'])
    plt.ylabel(heatmapsettings['ylabel'])
    plt.show()
