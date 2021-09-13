2020-09-24

Authors:
Chris Thorne, ctmads
Allie Bergmann, arbergm

# Value Investing
Value Investing project files and notebooks for SIADS 591/592 Milestone I project.

# Data_Collector.py
List of stocks from web scraping and corresponding data from APIs
* Scrape list of S&P500 stocks from Wikipedia
* Get fundamentals data for corresponding stocks from Quandl
* Get pricing data for corresponding stocks from finance

# Filters.py
Create filtering and eligibility criteria for each company in terms of various return rates and pricing targets, given the value investing methodology
* Have track records of positive year over year EPS
* Have reasonable efficiency (ROE > 10%)
* Have recurring efficiency (ROA positive year over year)
* Price target above current price

# Aggregations.py
Aggregate data and apply filters, clean and reduce the outputs for easier readability.
* Aggregate metrics for filtering, apply filters
* Return most recent observations for most up-to-date data
* Filter for only observations that meet all filtering criteria
* Clean output to only relevant data points
	* Symbol
	* Security (Company Name)
	* GICS Sector
	* Current Price
	* % Below Price Target
	* Price Target
	* Most Recent EPS
	* Most Recent ROA
	* Most Recent ROE
	* Asset Turnover
	* Debt-to-Equity Ratio
	* Dividend Yield
	* P/E Ratio

# Value_screener.py
Aggregate all previous functions and run through all steps in order.
* Run the value screener, return a data frame of the final value stocks
