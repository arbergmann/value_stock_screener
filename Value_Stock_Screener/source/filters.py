#!/usr/bin/env python3

import numpy as np


# Filtering Metrics

# If you would like to add additional calculations and criteria to your strategy,
# here is where you would add it.

# Make sure any filtering columns are boolean values (True/False) and are labeled
# with "filter_" for later dynamic dataframe filtering.

def pos_yoy_eps(df,timeframe='MRT',eps_type='epsdil'):
  """Adds a column with a boolean value indicating if yoy eps is positive.

  Keyword Arguments:
  df
  timeframe -- str, dimension being used throughout
  eps_type -- str, 'eps' (basic) or 'epsdil' (diluted)

  Returns:
  df -- dataframe with added boolean column for positive year-over-year eps.
  """

  if timeframe in ['MRT', 'ART']:
    df.sort_values('reportperiod',ascending=False,inplace=True)
    df['filter_pos_yoy_eps'] = np.where(df[eps_type] > df[eps_type].shift(-4), True, False)

  elif timeframe in ['ARY', 'MRY']:
      df.sort_values('reportperiod',ascending=False,inplace=True)
      df['filter_pos_yoy_eps'] = np.where(df[eps_type] > df[eps_type].shift(-1), True, False)

  return df


def roe(df, threshold=0.00):
  """
  Returns ROE as a calculated column (Net Income / Shareholder Equity [Avg])

  Keyword Arguments:
  df
  threshold -- float, percent ROE as decimal threshold (above=True, below=False)

  Returns:
  df -- dataframe with added 'roe_calc' float column and 'roe_thresh' boolean column
  """

  df['roe_calc'] = df['netinccmnusd'] / df['equityavg']
  df['filter_roe_thresh'] = np.where(df['roe_calc'] >= threshold, True, False)

  return df


def pos_yoy_roa(df,timeframe='MRT'):
  """Adds a column with a boolean value indicating if yoy roa is positive.

  Keyword Arguments:
  df
  timeframe -- str, dimension being used throughout

  Returns:
  df -- dataframe with added boolean column for positive year-over-year roa.
  """

  df['roa_calc'] = df['netinccmnusd'] / df['assetsavg']

  if timeframe in ['MRT', 'ART']:
    df.sort_values('reportperiod',ascending=False,inplace=True)
    df['filter_pos_yoy_roa'] = np.where(df['roa_calc'] > df['roa_calc'].shift(-4), True, False)

  elif timeframe in ['ARY', 'MRY']:
      df.sort_values('reportperiod',ascending=False,inplace=True)
      df['filter_pos_yoy_roa'] = np.where(df['roa_calc'] > df['roa_calc'].shift(-1), True, False)

  del df['roa_calc']

  return df


# Price Target Metrics
def pb_price_target(df):
  """ Returns columns for book value per share (price-to-book price target, pb_pt),
  boolean value for whether price to book (pb) is less than 1 (pb_value), and
  the percentage below price-to-book.
  """

  df['pb_pt'] = df['bvps']
  df['filter_pb_value'] = np.where((df['pb'] < 1) & (df['pb'] > 0), True, False)
  df['filter_pb_price_target'] = np.where((df['pb_pt'] > df['Current_Price']), True, False)
  df['pb_pt_pct_below'] = np.where(df['filter_pb_value'] == True, 1 - (df['Current_Price'] / df['pb_pt']), 0)

  return df
