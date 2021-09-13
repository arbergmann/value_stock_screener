#!/usr/bin/env python3

# Import libraries
import pandas as pd
import sys, os

#!pip install quandl
import quandl

#!pip install yfinance
import yfinance as yf

# API Credentials
quandl.ApiConfig.api_key = 'Xgwh__VbLXMscAH-oiFi'


#%%

# S&P 500 Scraper

def sp500_list_retrieval():
  """
  Retrieve the S&P 500 list from the corresponding Wikipedia page.

  Returns a dataframe of all tickers and corresponding industry information.
  """
  print("Acquiring S&P500 Tickers list.")

  table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

  df = table[0]
  df.columns = ['Symbol',
                'Security',
                'SEC filings',
                'GICS Sector',
                'GICS Sub Industry',
                'Headquarters Location',
                'Date First Added',
                'CIK',
                'Founded'
                ]
  df.drop(labels=['SEC filings',
                  'Headquarters Location',
                  'Date First Added',
                  'CIK'
                  ],
          axis=1,
          inplace=True
          )

  return df

#%%

from datetime import date

# Fundamental Data Pull from Quandl
def fundamentals_data_pull(timeframe='MRT', ticker=[], start_yr='2015', end_date=None):
  """Pull the fundamentals data for each ticker passed through. If no timeframe
  is selected, all timeframes (dimensions) will be pulled. Otherwise, timeframes
  may be selected from one of the following:

  Select One:
  - AR (As Reported)
  - MR (Most-Recent Reported)

  + One of the Following
  - Y (Annual)
  - T (Trailing Twelve Months)
  - Q (Quarterly)
  (i.e. MRY = Most-Recent Reported Annual Data)

  Keyword Arguments:
  timeframe -- one of the above (default 'MRT')
  ticker -- list of stock tickers (default empty list)

  Returns:
  dict -- keys are tickers, values are dataframe of all Quandl fundamentals data for designated timeframe
  """

  print("Acquiring fundamentals data for tickers.")

  # Reduce dataset only to years requested
  cutoff_date = str(start_yr + "-01-01")
  #cutoff_date = pd.to_datetime(start_yr + "-01-01")
  #df = df[df['reportperiod'] > cutoff_date]

  if timeframe == None:
    timeframe = input("Please select a timeframe from 'MRT', 'ART','ARY', or 'MRY':  ")
    #df = quandl.get_table('SHARADAR/SF1', ticker=ticker)
    # Removing to eliminate confusion with Quarterly results and potential incompatibility down the line -- AB 9/14

  elif timeframe in ['MRT', 'ART','ARY', 'MRY']:
    if end_date == None:
      end_date = str(date.today())
      df = quandl.get_table('SHARADAR/SF1', dimension=timeframe, calendardate={'gte': cutoff_date, 'lte' : end_date}, ticker=ticker, paginate=True)
    else:
      df = quandl.get_table('SHARADAR/SF1', dimension=timeframe, calendardate={'gte': cutoff_date, 'lte' : end_date}, ticker=ticker, paginate=True)

  elif timeframe in ['MRQ', 'ARQ']:
    raise ValueError("Quarterly data is not compatible with this analysis. Please select a timeframe from 'MRT', 'ART','ARY', or 'MRY'")

  else:
    timeframe = input("Please select a timeframe from 'MRT', 'ART','ARY', or 'MRY':  ")


  # Create a dictionary where keys are tickers and values are dataframes of fundamentals
  fund_dict = {}
  for x in ticker:
    df0 = df.copy()
    df0 = df0[df0['ticker'] == x.upper()]
    if len(df0) == 0:
      print("No data provided for symbol '" + x.upper() + "'")
      pass
    else:
      fund_dict[x.upper()] = df0

  return fund_dict


#%%

# Pricing Data Pull from yfinance
def pricing_data(fund_dict):
  """Pull the pricing data for each ticker.

  Keyword Arguments:
  fund_dict -- dict, dictionary where k,v pairs are ticker,fundamental_data pairs

  Returns:
  dict -- keys are tickers
  """

  class HiddenPrints():
    def __enter__(self):
      self._original_stdout = sys.stdout
      sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
      sys.stdout.close()
      sys.stdout = self._original_stdout

  print("Acquiring pricing data for tickers.")

  #current_price = {}
  to_del = []
  # Iterate through dictionary pulling data for that symbol, joining to
  # corresponding fundamentals dataframe.
  for k in fund_dict:
    start_date = min(fund_dict[k]['reportperiod'])
    #end_date = max(fund_dict[k]['reportperiod'])
    end_date = date.today()

    with HiddenPrints():
      data = yf.download(k, start=start_date, end=end_date)

    if len(data) > 0:
      current_price = data['Close'].iloc[-1]
      data.reset_index(inplace=True)
      data.rename(columns={"Date" : "reportperiod"}, inplace=True)

      # Sometimes quarter end/reporting period end is not on trading day, will take most recent closing price.
      # To do this, we will do an outer join of all data, sort by date, backfill data, then eliminate
      # all rows that did not have corresponding reporting data to restore original set + pricing.
      fund_dict[k] = pd.merge(fund_dict[k], data, left_on='reportperiod', right_on='reportperiod', how='outer', sort=False)
      fund_dict[k].sort_values('reportperiod',ascending=False,inplace=True)
      fund_dict[k][['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']] = fund_dict[k][['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']].bfill()
      fund_dict[k].dropna(axis=0, subset=['ticker'], inplace=True)
      fund_dict[k]['Current_Price'] = current_price

    elif len(data) == 0:
      to_del.append(k)
      pass

  print("Deleting tickers " + str(to_del) + " from dataset due to insufficient pricing data.")
  for k in to_del:
    del fund_dict[k]

  print("S&P Ticker Count after Data Acquisition:  " + str(len(fund_dict.keys())))

  return fund_dict
