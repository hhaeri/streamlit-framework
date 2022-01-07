# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 12:39:06 2022
@author: hhaeri

This is a simple app created by Hanieh Haeri for The Data Incubator milestone project using streamlit. 
It uses Python Requests libaray along with YFinance Data and plots historical prices for a selected stock to date.

"""

import csv
import requests
import pandas as pd
import streamlit as st
from bokeh.plotting import figure
# importing range1d from
# bokeh.models in order to change
# the X-Axis and Y-Axis ranges
from bokeh.models import Range1d, HoverTool, ColumnDataSource
import yfinance as yf

#############################################################################
st.set_page_config(
      page_title="hhaeri_milestone_app",
      page_icon=":)",
      layout="wide",
      initial_sidebar_state="expanded",
      menu_items={
          'Get Help': 'https://app.thedataincubator.com/12day.html',
          'About': "# Welcome to my first app!"
      }
  )

st.markdown("""
<style>
.big-font {
    font-size:30px !important;
.medium-font {
    font-size:20px !important;
.small-font {
    font-size:20px !important;
}
</style>
""", unsafe_allow_html=True)


#############################################################################
#This API returns a list of active or delisted US stocks and ETFs, either as of the latest trading day or at a 
#specific time in history. The endpoint is positioned to facilitate equity research on asset lifecycle and survivorship.

my_apikey = '8G2941CYJGUYUU6A'
url = 'https://www.alphavantage.co/query'
function='LISTING_STATUS'
parameters1 = {'function':function,'apikey':my_apikey}
with requests.Session() as s:
    download = s.get(url,params = parameters1)
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
#    for row in my_list:
#        print(row)

api_list = pd.DataFrame(my_list).iloc[1::,0].tolist()
#############################################################################
#Configuring the title and sidebar for the app created by streamlit

st.title("The Data Incubator Milestone Project")
st.markdown('<p class="big-font">Hanieh Haeri </p>', unsafe_allow_html=True)

st.sidebar.markdown('<p class="medium-font">The Data Incubator Milestone Project</p> Hanieh Haeri </p>', unsafe_allow_html=True)


st.sidebar.markdown('<p class="small-font">This is a simple app created by streamlit. It uses Python Requests libarary\
                    along with YFinance Data and plots historical prices for a selected stock to date</p> \
                        Comments? <p>Email: hhaeri0911@gmail.com</p>', unsafe_allow_html=True)

#############################################################################
# Creating Select Widgets using Streamlit

#Select Widget for Ticker
selected_ticker = st.sidebar.selectbox(
     'Select Ticker Symbol',
     api_list)

#Select Widget for Period
selected_period = st.sidebar.selectbox(
     'Select - Retrieve Past Data Timeframe',
     ["1d","1mo","3mo","6mo","1y","5y","10y","ytd","max"])

#Select Widget for Interval
selected_interval = st.sidebar.selectbox(
     'Select - Retrieve Interval',
     ["30m","1h","1d","5d","1wk","1mo","3mo"])

#############################################################################
#Fetching the stock data from yfinance
###
#Use the following format to fetch a specific period between two dates
# data = yf.download("SPY AAPL", start="2017-01-01", end="2017-04-30")
###
data = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers = selected_ticker,

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period = selected_period,

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval = selected_interval,

        # group by ticker (to access via data['SPY'])
        # (optional, default is 'column')
        group_by = 'ticker',

        # adjust all OHLC automatically
        # (optional, default is False)
        auto_adjust = True,

        # download pre/post regular market hours data
        # (optional, default is False)
        prepost = True,

        # use threads for mass downloading? (True/False/Integer)
        # (optional, default is True)
        threads = True,

        # proxy URL scheme use use when downloading?
        # (optional, default is None)
        proxy = None
    )
#############################################################################
#Creating the chart using bokeh

data2 = data.reset_index()

source = ColumnDataSource(data={
    'date'      : data2.iloc[:,0],
    'adj close' : data2.iloc[:,4],
    'volume'    : data2.iloc[:,5],
})


p = figure(
      title=f'Price History of {selected_ticker} to date\n  {selected_period} Period, {selected_interval} Interval',
      x_axis_label='Date',
      y_axis_label='Closing Price in USD $', 
      x_axis_type="datetime",
      plot_width=1000,
      plot_height=600)
p.line(x='date', y='adj close', line_width=2, color='#ebbd5b', source=source)

p.add_tools(HoverTool(
    tooltips=[
        ( 'date',   '@date{%F}'            ),
        ( 'close',  '$@{adj close}{0.2f}' ), # use @{ } for field names with spaces
        ( 'volume', '@volume{0.00 a}'      ),
    ],

    formatters={
        '@date'      : 'datetime', # use 'datetime' formatter for 'date' field
        'adj close' : 'printf',   # use 'printf' formatter for 'adj close' field
                                  # use default 'numeral' formatter for other fields
    },

    # display a tooltip whenever the cursor is vertically in line with a glyph
    mode='vline'
))

st.bokeh_chart(p)

