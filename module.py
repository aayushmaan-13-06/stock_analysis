import numpy as np
import pandas as pd
from datetime import datetime
from scipy import stats
import statistics
from scipy.stats import skew
np.set_printoptions(threshold=np.inf) #displaying full numpy array without truncation
pd.set_option("display.max_rows", None, "display.max_columns", None) #displaying full pandas dataframe without truncation
import plotly.express as ff
import matplotlib.pyplot as plt
import math
from scipy.stats import norm
import seaborn as sns
import streamlit as st
def plot_histogram(data, col,parameter, title = 'Histogram'):
    """
    This function plots the histogram and prints the necessary details of the given input
    Inputs:
    data = The dataframe on which you would like to plot the histogram
    col = The column of the dataframe on which you would like to plot the histogram on
    parameter = What you would like to be printed while printing the necessary details
    title = The title which you would like to give to your histogram
    Returns:
    Returns a plotly figure
    """
    fig = ff.histogram(data, x=col, title = title)
    st.write(f'The histogram shows that the {parameter} of {col}, oscillate around {stats.mode(data[col])[0][0]}')
    st.write(f'The average {parameter} of this {col} is {np.mean(data[col])}')
    st.write(f'The median {parameter} of this {col} is {np.median(data[col])}')
    if data[col].skew()>0:
        st.write(f'This {col} is positively skewed which indicates that there are more positive returns which is a good sign for the stock')
        st.write('This is supported by the more number of peaks and higher peaks on the positive side of the histogram after the meidan')
    elif data[col].skew()<0:
        st.write(f'This {col} is negatively skewed which indicates that there are more negative returns which is a bad sign for the stock')
        st.write('This is supported by the more number of peaks and higher peaks on the negative side of the histogram before the meidan')
    else:
        st.write(f'The {col} is not skewed which means both the returns are equally likely')
        st.write('Please look out for the outliers also')
    return fig

def plot_boxplot(data, col, parameter, title = 'Boxplot'):
    """
    This function plots the boxplot and prints the necessary details of the given input
    Inputs:
    data = The dataframe on which you would like to plot the boxplot
    col = The column of the dataframe on which you would like to plot the boxplot on
    parameter = What you would like to be printed while printing the necessary details
    title = The title which you would like to give to your boxplot
    Returns:
    Returns a plotly figure
    """
    fig = ff.box(data, y=col, title=title)
    st.write(f'From this boxplot we can see that the median {parameter} of this stock {col} is {np.median(data[col])}')
    if data[col].skew()>0:
        st.write(f'From this boxplot we can see that there are more positive {parameter} in this stock')
        st.write(f'This can be seen in the boxplot as there are more {parameter} above the median i.e there is more data above the median than below the median')
    elif data[col].skew()<0:
        st.write(f'From this boxplot we can see that there are more negative {parameter} in this stock')
        st.write(f'This can be seen in the boxplot as there are more {parameter} below the median i.e there is more data below the median than above the median')
    else:
        st.write(f'The {parameter} are not skewed and the positive returns and the negative returns are equally likely')
    st.write('Please watch out for the outliers')
    return fig

def descriptive_analysis(data):
    """
    This function calculates the descriptive statistics of the given dataframe
    Inputs:
    data = The dataframe on which you would like to calculate descriptive statistics
    Retruns:
    output_df = A dataframe consisting of all the necessary descriptive statistics
    correlation_matrix = A correlation matrix of all the columns in the dataframe
    covariance_matrix = A covariance matrix of all the columns in the dataframe
    """
    mean_list = []
    median_list = []
    mode_list = []
    skewness_list = []
    kurtosis_list = []
    stdev_list = []
    min_list = []
    max_list = []
    for col in data.columns:
        mean_list.append(np.mean(data[col]))
        median_list.append(np.median(data[col]))
        mode_list.append(stats.mode(data[col])[0][0])
        skewness_list.append(data[col].skew())
        kurtosis_list.append(stats.kurtosis(data[col]))
        stdev_list.append(np.std(data[col]))
        min_list.append(np.min(data[col]))
        max_list.append(np.max(data[col]))
    output_df = pd.DataFrame()
    output_df['Mean'] = mean_list
    output_df['Median'] = median_list
    output_df['Mode'] = mode_list
    output_df['Skewness'] = skewness_list
    output_df['Kurtosis'] = kurtosis_list
    output_df['Standard Deviation'] = stdev_list
    output_df['Min'] = min_list
    output_df['Max'] = max_list
    output_df.index = data.columns
    correlation_matrix = data.corr()
    covariance_matrix = pd.DataFrame.cov(data)
    return output_df, correlation_matrix, covariance_matrix

def comparitive(data, parameter):
    """
    Performs comparitive Analysis of the columns of the dataframe passed as a parameter
    Inputs:
    data = the dataframe you would like to perform compartive analysis on (type = pd.DataFrame())
    parameter = The value you would like to be printed in the dataframe
    Returns
    output_df = the dataframe comprising of the output of the comparitive analysis (type = pd.Dataframe())
    """
    mean_list = []
    median_list = []
    mode_list = []
    skewness_list = []
    kurtosis_list = []
    stdev_list = []
    min_list = []
    max_list = []
    stock_list = []
    for column in data.columns:
        stock_list.append(str(column))
    fig, ax = plt.subplots(figsize=(20,10))
    ax.plot(data)
    plt.legend(data.columns, loc='upper right')
    st.pyplot(fig)
    for col in stock_list:
        mean_list.append(np.mean(data[col]))
        median_list.append(np.median(data[col]))
        mode_list.append(stats.mode(data[col])[0][0])
        skewness_list.append(data[col].skew())
        kurtosis_list.append(stats.kurtosis(data[col]))
        stdev_list.append(np.std(data[col]))
        min_list.append(np.min(data[col]))
        max_list.append(np.max(data[col]))
    max = stock_list[mean_list.index(np.max(mean_list))]
    min = stock_list[mean_list.index(np.min(mean_list))]
    most_vol = stock_list[stdev_list.index(np.max(stdev_list))]
    least_vol = stock_list[stdev_list.index(np.min(stdev_list))]
    most_skew = stock_list[skewness_list.index(np.max(skewness_list))]
    least_skew = stock_list[skewness_list.index(np.min(skewness_list))]
    output = [max,min,most_vol, least_vol, most_skew, least_skew]
    column_names = [f'Max avg {parameter}', f'Min avg {parameter}', f'Most Vollatile {parameter}', f'Least Volatile {parameter}', f'Most Skewed {parameter}', f'Least Skewed {parameter}']
    output_df = pd.DataFrame(output)
    output_df.index = column_names
    output_df.columns = ['Stock']
    return output_df

def plot_ts(data, col, parameter, title='Time Series Plot'):
    """
    This function plots the time series of the given dataframe and it's column
    along with printing the index having maximum and minimum index in the column
    of the dataframe
    Inputs:
    data = The dataframe on which you wish to have time series plot on
    col = The column of the dataframe which you wish to have time series plot on
    parameter = The value which you would like to have printed in the output
    title = The title which you would wish to give to your plot
    """
    for col in data.columns:
        fig, ax = plt.subplots(figsize=(20,10))
        ax.plot(data[col])
        ax.set_title(f"Time Series plot of {parameter} for {col}")
        data[col].plot(figsize=(20,10))
        st.write(f'The maximum {parameter} was observed on {data[col].idxmax()}')
        st.write(f'The minimum {parameter} was observed on {data[col].idxmin()}')
        return fig

def hypothesis_testing(data,col,test_value, threshold, n_sample, two_tailed):
    """
    This function validates the hypothesis for a given sample mean, sample standard deviation and
    the threshold to which you want to validate the hypothesis.
    This function can perform both one tailed and two tailed tests
    Inputs:
    data - The dataframe on which you want to validate your hypothsis
    col - The column of the dataframe on which you want to validate your hypothesis
    test_value - The value on which you want to test your hypothesis
    threshold - The alpha value up to which you want to validate your hypothesis
    two_tailed - (Boolean value) whether you want to perform one tailed or two tailed tests
    Returns: None
    """
    mean=np.mean(data[col])
    std=(np.std(data[col]))/math.sqrt(n_sample)
    if threshold>1:
        raise ValueError('The threshold should be between 0 and 1, try dividing the threshold value by 100')

    z_score = abs((test_value-mean)/std)
    if two_tailed:
        threshold = threshold/2
        z_critical = abs(norm.ppf(threshold))
        if z_score>z_critical:
            st.write(f'Hypothesis rejected as the z score is {(test_value-mean)/std} which is more than the z critical {norm.ppf(threshold)}')
        else:
            st.write(f'Hypothesis accpeted as the z score is {(test_value-mean)/std} which is less than the z critical {norm.ppf(threshold)}')
    else:
        z_critical = abs(norm.ppf(threshold))
        if z_score>z_critical:
            st.write(f'Hypothesis rejected as the z score is {(test_value-mean)/std} which is more than the z critical {norm.ppf(threshold)}')
        else:
            st.write(f'Hypothesis accpeted as the z score is {(test_value-mean)/std} which is less than the z critical {norm.ppf(threshold)}')

def visualise_heatmap(data, title='Heatmap for the data', cmap = 'coolwarm'):
    """
    This function plots a heatmap of the data passed in it
    Inputs: 
    data = The dataframe on which you would like to plot a heatmap 
    title = The title you would like to give to your heatmap (default = 'Heatmap for the data')
    cmap = The colormap you would like to use on your heatmap (default = 'coolwarm')
    Returns:
    A seaborn figure
    """
    fig = plt.figure(figsize=(data.shape[1],data.shape[1]))
    sns.heatmap(data, annot=True, fmt ='.3g', cmap=cmap, square=True).set_title(title)
    return fig