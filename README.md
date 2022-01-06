A first-year project for the University of Michigan's Master of Applied Data Science program's Milestone I class.

This project seeks to deploy a data pipeline that independently, from start to finish, scrapes S&P 500 names, pulls fundamentals data through Quandl and pricing data from Yahoo!Finance, then, through a series of easily modifiable code, filters for value stocks and returns a dataframe of possible options with relevant investing metrics.


# Value Investing Stock Picks
#### <i>Allie Bergmann and Chris Thorne</i>

### Project Summary
This project will analyze the underlying components of major market indices to identify company stocks that are trading at a discount to their value. We will determine this value using a Price-to-Book (P/B) ratio, and filtering stocks additionally based the following criteria on a yearly reporting basis:

* Earnings Per Share (EPS) Increased over the previous year
    * Indicates a trend of increasing value per share to investors year-over-year.
* Return on Equity (ROE) > 10%
    * Indicates an effective use of investor funds to generate profits.
* Return on Assets (ROA) Increased over the previous year
    * Similar to ROE, but accounts for company debts instead of just equity, and indicates an increase in company profitability relative to its total assets year over-year.


With publicly available data, we will be able to calculate a valuation for each stock, then isolate which are trading below that valuation. Since the metric we will be using to provide a price target does not necessarily account for intangible assets (common in technology companies), we have also added the additional metrics in our filtering process to consider the other factors contributing to a company’s growth and efficiency. These value stocks are often posited in the financial world to have more potential for greater upside, as they are trading below the price that they are deemed to be worth.


The goal and motivation of the project is to efficiently and quickly identify stock picks that may be suitable for a value investing portfolio using data sources. Previously, all of these stocks would have had to have been modeled and analyzed painstakingly by hand or in Excel.


Questions we want to answer include:
* What is an appropriate valuation for the stock price, based on P/B?
* Is the current stock price above or below that valuation?
* Which of the stocks in the popular indexes, like the S&P 500, are trading below our valuation, and thus have the potential for greater returns?

