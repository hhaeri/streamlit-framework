# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 12:39:06 2022

@author: hhaeri
"""

import csv
import requests
import pandas as pd
import streamlit as st
from bokeh.plotting import figure
# importing range1d from
# bokeh.models in order to change
# the X-Axis and Y-Axis ranges
from bokeh.models import Range1d, HoverTool
import yfinance as yf

my_apikey = '8G2941CYJGUYUU6A'
url = 'https://www.alphavantage.co/query'
function='LISTING_STATUS'
parameters1 = {'function':function,'apikey':my_apikey}


#This API returns a list of active or delisted US stocks and ETFs, either as of the latest trading day or at a specific time
# in history. The endpoint is positioned to facilitate equity research on asset lifecycle and survivorship.


with requests.Session() as s:
    download = s.get(url,params = parameters1)
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
#    for row in my_list:
#        print(row)

api_list = pd.DataFrame(my_list).iloc[1::,0].tolist()

##################################
# Create Select Widgets using Streamlit

#Select Widget for Ticker
selected_ticker = st.selectbox(
     'Select Ticker Symbol',
     api_list)

#Select Widget for Period
selected_period = st.selectbox(
     'Select - Retrieve Past Data Timeframe',
     ["1d","1mo","3mo","6mo","1y","5y","10y","ytd","max"])

#Select Widget for Interval
selected_interval = st.selectbox(
     'Select - Retrieve Interval',
     ["30m","1h","1d","5d","1wk","1mo","3mo"])




# data = yf.download("SPY AAPL", start="2017-01-01", end="2017-04-30")

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


x = data.index.tolist()
y = data['Close'].tolist()
z = data['Volume'].tolist()

p = figure(
      title=f'Price History of {selected_ticker} to date\n  {selected_period} Period, {selected_interval} Interval',
      x_axis_label='Date',
      y_axis_label='Closing Price in USD $', 
      x_axis_type="datetime",
      background_fill_color="#f5f5f5",
      plot_width=1000,
      plot_height=600)

p.grid.grid_line_color="white"

# With the help of x_range and
# y_range functions I am setting
# up the range of both the axis

#p.x_range = Range1d(20, 25)
# miny = min(float(x) for x in y)
miny = 0
if len(x)>0:
    maxy = max(float(x) for x in y)*1.2
else:
    maxy = 2000
    
p.y_range = Range1d(miny, maxy)


# Add the HoverTool to the figure
# Format the tooltip
p.add_tools(HoverTool(
    tooltips=[
        ( 'date',   '@x{%F}'            ),
        ( 'close',  '$@y{%0.2f}' ), # use @{ } for field names with spaces
        ( "volume", "@z{0.00 a}"      ),
    ],

    formatters={
        '@x'        : 'datetime', # use 'datetime' formatter for '@date' field
        '@y' : 'printf',   # use 'printf' formatter for '@y' field
                                     # use default 'numeral' formatter for other fields
    },

    # display a tooltip whenever the cursor is vertically in line with a glyph
    mode='vline'
))
#simple tooltip
# tooltips = [
#             ('Date','@x{%F}'),
#             ('Closing price', '@y'),
#            ]
# Add the HoverTool to the figure
# p.add_tools(HoverTool(tooltips=tooltips,formatters={'@x': 'datetime'}))

p.line(x, y)
# show(p)
st.bokeh_chart(p)

