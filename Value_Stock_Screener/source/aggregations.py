#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
filepath = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(filepath)

import pandas as pd
import filters
import data_collector

# Aggregation and Dataset Reduction

def metrics_aggregation(df, timeframe='MRT', eps_type='epsdil', roe_threshold=0.10):
  """Returns dataframe aggregating all of the filtering and price targets.
  """
  ## Add any additional filtering metrics here with any relevant
  # Answers objective: Postiive Year-Over-Year Earnings Per Share (EPS)
  df = filters.pos_yoy_eps(df, timeframe=timeframe, eps_type=eps_type)

  # Answers objective: Return on Equity > 10%
  df = filters.roe(df, threshold=roe_threshold)

  # Answers objective: Return on Assets Increased over Previous Year
  df = filters.pos_yoy_roa(df, timeframe=timeframe)

  # Answers objective: Price Target
  df = filters.pb_price_target(df)

  return df


def most_recent(fund_dict):
  """Returns a dataframe of the most recent valuation data from each ticker in
  the dictionary passed through.
  """

  print("Pulling most recent observations.")

  data = []

  for k in fund_dict:
    fund_dict[k].sort_values('reportperiod',ascending=False,inplace=True)
    row = fund_dict[k].iloc[0]
    data.append(row)

  df = pd.DataFrame(data=data)

  return df


def filter_for_value_stocks(df):
  """ Returns dataframe of all symbols where all filter criteria have been
  determined to be True.
  """
  print("Reducing dataset to available value stocks.")

  cols = [col for col in df.columns if 'filter_' in col]
  df = df[df[cols].all(1)]
  if len(df) > 0:
    return df
  else:
    print("There are no value stocks available at this time.")


def clean_output(df):

  ticker_info = data_collector.sp500_list_retrieval()

  df = pd.merge(df, ticker_info, left_on='ticker', right_on='Symbol', how='left', sort=False)
  df.sort_values(by='pb_pt_pct_below', ascending=False, inplace=True)

  df = df[['Symbol',
           'Security',
           'GICS Sector',
           'Current_Price',
           'pb_pt_pct_below',
           'pb_pt',
           'eps',
           'roa',
           'roe',
           'assetturnover',
           'de',
           'divyield',
           'pe'
           ]]

  df.rename(columns={'Current_Price' : 'Current Price',
                     'pb_pt_pct_below' : '% Below Price Target',
                     'pb_pt' : 'Price Target',
                     'eps' : 'EPS',
                     'roa' : 'ROA',
                     'roe' : 'ROE',
                     'assetturnover' : 'Asset Turnover',
                     'de' : 'Debt-to-Equity',
                     'divyield' : 'Dividend Yield',
                     'pe' : 'P/E'
                     }, inplace=True)

  df['Current Price'] = df['Current Price'].apply(lambda x: ("${:,.2f}").format(x))
  df['Price Target'] = df['Price Target'].apply(lambda x: ("${:,.2f}").format(x))
  df['EPS'] = df['EPS'].apply(lambda x: ("${:,.2f}").format(x))
  df['ROA'] = df['ROA'].apply(lambda x: ("{:,.2f}%").format(x*100))
  df['ROE'] = df['ROE'].apply(lambda x: ("{:,.2f}%").format(x*100))
  df['Asset Turnover'] = df['Asset Turnover'].apply(lambda x: ("{:,.2f}%").format(x*100))
  df['Dividend Yield'] = df['Dividend Yield'].apply(lambda x: ("{:,.2f}%").format(x*100))
  df['% Below Price Target'] = df['% Below Price Target'].apply(lambda x: ("{:,.2f}%").format(x*100))

  return df