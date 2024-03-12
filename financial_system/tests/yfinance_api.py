import yfinance as yf
import pandas as pd
# from IPython.core.display_functions import display

# tickers = yf.Tickers('ticker aapl goog')
#
# tickers_dic = tickers.tickers
# print(tickers_dic['ticker'].actions)
# print(tickers.tickers['AAPL'].history(period="1mo"))
# print(tickers.tickers['GOOG'].actions)
#
# print('*'*30)


def display_dictionary(dictionary):
    df = pd.DataFrame(dictionary)
    print(df)

def load(symbol):
    ticker = yf.Ticker(symbol)

    # get all stock info
    print(ticker.info)

    # get historical market data
    display_dictionary(ticker.history(period="1mo"))

    # show meta information about the history (requires history() to be called first)
    print("History Metadata" + "+"*30)
    print(ticker.history_metadata)

    # show actions (dividends, splits, capital gains)
    print("Actions (dividends, splits, capital gains)" + "+"*30)
    display_dictionary(ticker.actions)
    print(ticker.dividends)
    print(ticker.splits)
    print(ticker.capital_gains)  # only for mutual funds & etfs

    # show share count
    print("Share Count" + "+"*30)
    print(ticker.get_shares_full(start="2022-01-01", end=None))

    # show financials:
    print("Financials" + "+"*30)
    # - income statement
    print("Income statement")
    print(ticker.income_stmt)
    print(ticker.quarterly_income_stmt)
    # - balance sheet
    print("Balance sheet")
    print(ticker.balance_sheet)
    print(ticker.quarterly_balance_sheet)
    # - cash flow statement
    print("Csh flow statement")
    print(ticker.cashflow)
    print(ticker.quarterly_cashflow)
    # see `Ticker.get_income_stmt()` for more options

    # show holders
    print("Holders")
    print(ticker.major_holders)
    print(ticker.institutional_holders)
    print(ticker.mutualfund_holders)
    print(ticker.insider_transactions)
    print(ticker.insider_purchases)
    print(ticker.insider_roster_holders)

    # show recommendations
    print("Recommendations" + '+'*30)
    print(ticker.recommendations)
    print(ticker.recommendations_summary)
    print(ticker.upgrades_downgrades)

    # Show future and historic earnings dates, returns at most next 4 quarters and last 8 quarters by default.
    # Note: If more are needed use ticker.get_earnings_dates(limit=XX) with increased limit argument.
    print("Future and historic earnings dates" + '+'*30)
    print(ticker.earnings_dates)

    # show ISIN code - *experimental*
    # ISIN = International Securities Identification Number
    print("ISIN code" + '+'*30)
    print(ticker.isin)

    # show options expirations
    print("Options Expirations" + '+'*30)
    print(ticker.options)

    # show news
    print("\n\nNews " + '+'*30)
    print(ticker.news)

    # get option chain for specific expiration
    # opt = ticker.option_chain('YYYY-MM-DD')
    # data available via: opt.calls, opt.puts

load("AAPL")