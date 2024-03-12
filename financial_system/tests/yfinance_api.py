import yfinance as yf
import pandas as pd
from IPython.core.display_functions import display

tickers = yf.Tickers('msft aapl goog')

tickers_dic = tickers.tickers
print(tickers_dic['MSFT'].actions)
print(tickers.tickers['AAPL'].history(period="1mo"))
print(tickers.tickers['GOOG'].actions)

print('*'*30)


def display_dictionary(dictionary):
    df = pd.DataFrame(dictionary)
    display(df)


msft = yf.Ticker("MSFT")

# get all stock info
print(msft.info)

# get historical market data
display_dictionary(msft.history(period="1mo"))

# show meta information about the history (requires history() to be called first)
print("History Metadata" + "+"*30)
print(msft.history_metadata)

# show actions (dividends, splits, capital gains)
print("Actions (dividends, splits, capital gains)" + "+"*30)
display_dictionary(msft.actions)
print(msft.dividends)
print(msft.splits)
print(msft.capital_gains)  # only for mutual funds & etfs

# show share count
print("Share Count" + "+"*30)
print(msft.get_shares_full(start="2022-01-01", end=None))

# show financials:
print("Financials" + "+"*30)
# - income statement
print("Income statement")
print(msft.income_stmt)
print(msft.quarterly_income_stmt)
# - balance sheet
print("Balance sheet")
print(msft.balance_sheet)
print(msft.quarterly_balance_sheet)
# - cash flow statement
print("Csh flow statement")
print(msft.cashflow)
print(msft.quarterly_cashflow)
# see `Ticker.get_income_stmt()` for more options

# show holders
print("Holders")
print(msft.major_holders)
print(msft.institutional_holders)
print(msft.mutualfund_holders)
print(msft.insider_transactions)
print(msft.insider_purchases)
print(msft.insider_roster_holders)

# show recommendations
print("Recommendations" + '+'*30)
print(msft.recommendations)
print(msft.recommendations_summary)
print(msft.upgrades_downgrades)

# Show future and historic earnings dates, returns at most next 4 quarters and last 8 quarters by default.
# Note: If more are needed use msft.get_earnings_dates(limit=XX) with increased limit argument.
print("Future and historic earnings dates" + '+'*30)
print(msft.earnings_dates)

# show ISIN code - *experimental*
# ISIN = International Securities Identification Number
print("ISIN code" + '+'*30)
print(msft.isin)

# show options expirations
print("Options Expirations" + '+'*30)
print(msft.options)

# show news
print("\n\nNews " + '+'*30)
print(msft.news)

# get option chain for specific expiration
# opt = msft.option_chain('YYYY-MM-DD')
# data available via: opt.calls, opt.puts