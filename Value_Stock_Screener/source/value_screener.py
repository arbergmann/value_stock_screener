#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
filepath = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(filepath)
#sys.path.append('/Users/Allie/Desktop/Value_Stock_Screener')

import data_collector
import aggregations

def run_value_screener(dimension='', start_yr='2015', end_date=None, eps_type='epsdil', roe_threshold=0.10):

  # Retrieve list of S&P 500 stocks
  df = data_collector.sp500_list_retrieval()
  stock_list = list(df['Symbol'].unique())
  print("S&P 500 Ticker Count:  " + str(len(stock_list)))

  # Retrieve fundamentals data for all S&P 500 stocks
  stock_dict = data_collector.fundamentals_data_pull(timeframe=dimension, ticker=stock_list, start_yr=start_yr, end_date=None)

  # Merge pricing data for all stocks
  stock_dict = data_collector.pricing_data(stock_dict)

  # Add on filters and price targets
  print("Calculating filters and metrics.")
  for k in stock_dict:
    aggregations.metrics_aggregation(stock_dict[k], timeframe=dimension, eps_type=eps_type, roe_threshold=0.10)

  # Reduce dataset to those that meet criteria
  stock_df = aggregations.most_recent(stock_dict)
  stock_df = aggregations.filter_for_value_stocks(stock_df)
  stock_df = aggregations.clean_output(stock_df)

  print("Analysis Complete.")
  return stock_df


#if __name__ == "__main__":

# Run Screener
#df = run_value_screener(dimension='MRT', start_yr='2015', end_date=None, eps_type='epsdil', roe_threshold=0.10)