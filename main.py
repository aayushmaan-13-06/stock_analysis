import numpy as np
import pandas as pd
import re
import seaborn as sns
from pandas_datareader import data
from pandas_datareader.data import DataReader
from datetime import datetime
from scipy import stats
import statistics
import matplotlib.pyplot as plt
from scipy.stats import skew
import streamlit as st
import plotly.express as ff
from module import *
st.write("""

## Prepared by:
## Aayushmaan Jain
""")
st.write("""
This is a web app intended to help you with basic stock analysis along with the visulalizations with a statistical perspective.

Precautions and advices

1) This notebook uses Yahoo Finance as its source of financial data by default

2) The case in which you enter the stock does not matter as the stock name will be converted to upper case

3) The separator you use while entering the dates does not matter as the date accepts both separators like / and - but please enter the date in YYYY/MM/DD format

Please note that this web app only helps you to analyse the stocks and take informed decisions. This app does not give any financial advice. Please invest carefully.
""")

np.set_printoptions(threshold=np.inf) #displaying full numpy array without truncation
pd.set_option("display.max_rows", None, "display.max_columns", None) #displaying full pandas dataframe without truncation

st.write('# User Inputs')
st.write('### Enter quit to stop')
stock_list = list()
num_stocks = st.number_input('Enter the number of stocks in your portfolio')
key = 1
for i in range(int(num_stocks)):
    stock_inp = st.text_input('Enter a stock name according to yahoo finance search: ', key = str(key))
    stock_list.append(stock_inp.upper())
    key += 1
from_date = st.text_input('Enter the from date in yyyy/mm/dd format ')
from_date = re.split('-|/', from_date)
to_date = st.text_input('Enter the to date in yyyy/mm/dd format ')
to_date = re.split('-|/', to_date)
try:
    for i in range(len(from_date)):
      from_date[i] = int(from_date[i])
    for j in range(len(to_date)):
      to_date[j] = int(to_date[j])
except:
    pass

column_name = st.text_input('Enter the column you would like to consider for analysis (case sensitive): ')
final_dataframe = pd.DataFrame()
try:
  for stock in stock_list:
    historical_data = DataReader(stock,  "yahoo", datetime(int(from_date[0]), int(from_date[1]), int(from_date[2])), datetime(int(to_date[0]), int(to_date[1]), int(to_date[2])))
    final_dataframe[stock] = historical_data[column_name]
except:
  st.write('Please enter a valid input')
final_dataframe = final_dataframe.dropna()

return_dataframe = final_dataframe.pct_change()
return_dataframe = return_dataframe.dropna()
try:
    return_dataframe.columns = stock_list
except:
    pass

st.write("""
This web app can analyse the stocks on the basis of following plots

1) Histogram

2) Boxplots

3) Time Series

4) Comparitive Analysis
""")
choice_hist = st.text_input('Would you like to analyse based on Histograms? ')
choice_box = st.text_input('Would you like to analyse based on Boxplots? ')
choice_ts = st.text_input('Would you like to analyse based on Time Series? ')
choice_comparitive = st.text_input('Would you like to do a comparitive analysis? ')
choice_col = st.text_input(f'Would you like to analyse returns or {column_name} or both? ')
try:
    if choice_hist.upper().startswith('Y') or choice_hist.upper().startswith('B'):
        if choice_col.upper().startswith('R') or choice_col.upper().startswith('B'):
            st.write('Histograms for returns')
            for stock in stock_list:
              fig = plot_histogram(data = return_dataframe, col=stock, parameter="return", title=f"Histogram for returns of {stock}")
              st.plotly_chart(fig)
        if choice_col.upper().startswith(column_name.upper()) or choice_col.upper().startswith('B'):
            st.write('Histograms for {col}'.format(col=column_name))
            for stock in stock_list:
              fig = plot_histogram(data=final_dataframe, col=stock, parameter={column_name}, title=f"Histogram for {column_name} of {stock}")
              st.plotly_chart(fig)
    if choice_box.upper().startswith('Y') or choice_box.upper().startswith('B'):
        if choice_col.upper().startswith('R') or choice_col.upper().startswith('B'):
            st.write('Boxplots for retuns')
            for stock in stock_list:
              fig = plot_boxplot(data=return_dataframe, col=stock, parameter="return", title=f"Boxplot for returns of {stock}")
              st.plotly_chart(fig)
        if choice_col.upper().startswith(column_name.upper()) or choice_col.upper().startswith('B'):
            st.write('Boxplot for {col}'.format(col = column_name))
            for stock in stock_list:
              fig = plot_boxplot(data=final_dataframe, col=stock, parameter=column_name, title=f"Boxplot for {column_name} of {stock}")
              st.plotly_chart(fig)

    if choice_ts.upper().startswith('Y') or choice_ts.upper().startswith('B'):
        if choice_col.upper().startswith('R') or choice_col.upper().startswith('B'):
            st.write('Time Series plot for returns')
            fig = plot_ts(data=return_dataframe, col=stock, parameter="return", title=f"Time series plot for returns of {stock}")
            st.pyplot(fig)
        if choice_col.upper().startswith(column_name.upper()) or choice_col.upper().startswith('B'):
            st.write('Time Series plots for {col}'.format(col = column_name))
            for stock in stock_list:
              fig = plot_ts(data=final_dataframe, col=stock, parameter=column_name, title=f"Time series plot for {column_name} of {stock}")
              st.pyplot(fig)

    """Descriptive Statistics"""

    
    if choice_col.upper().startswith(column_name.upper()) or choice_col.upper().startswith('B'):
        st.write('Descriptive Statistics Table for', column_name)
        output_df_return, correlation_matrix_return, covariance_matrix_return = descriptive_analysis(data=return_dataframe)
        st.write(output_df_return)
        st.write(correlation_matrix_return)
        st.write(covariance_matrix_return)

    if choice_col.upper().startswith('R') or choice_col.upper().startswith('B'):
        st.write('Descriptive Statistics Table for returns')
        output_df_col, correlation_matrix_col, covariance_matrix_col = descriptive_analysis(data=return_dataframe)
        st.write(output_df_col)
        st.write(correlation_matrix_col)
        st.write(covariance_matrix_col)

    st.write('Visualizing correlation martrix')
    if choice_col.upper().startswith('R') or choice_col.upper().startswith('B'):
        st.write("Correlation matrix for Returns")
        figure = visualise_heatmap(data=correlation_matrix_return,title=f"Correlation matrix for returns")
        st.pyplot(figure)

    if choice_col.upper().startswith(column_name.upper()) or choice_col.upper().startswith('B'):
        st.write(f"Correlation matrix for {column_name}")
        figure_col = visualise_heatmap(data=correlation_matrix_col,title=f"Correlation matrix for {column_name}")
        st.pyplot(figure_col)

    if choice_col.upper().startswith('R') or choice_col.upper().startswith('B'):
        st.write('Covariance Matrix for Returns')
        cov_fig = visualise_heatmap(data=covariance_matrix_return, title="Covariance matrix for Returns")
        st.pyplot(cov_fig)

    if choice_col.upper().startswith(column_name.upper()) or choice_col.upper().startswith('B'):
        st.write(f'Covariance Matrix for {column_name}')
        cov_fig_col = visualise_heatmap(data=covariance_matrix_col, title="Covariance matrix for Returns")
        st.pyplot(cov_fig_col)

    if choice_comparitive.upper().startswith('Y'):
        st.write('Comparitive Analysis')
        if choice_col.upper().startswith('R') or choice_col.upper().startswith('B'):
            output_df = comparitive(data=return_dataframe, parameter="Returns")
            st.write(output_df)
        if choice_col.upper().startswith(column_name.upper()) or choice_col.upper().startswith('B'):
            output_df = comparitive(data=final_dataframe, parameter=column_name)
            st.write(output_df)
except:
    pass
st.write("""
Thank you for using this web app, please leave a feedback. This motivates me to make more web apps like this.

Regards,

Aayushmaan Jain
""")
