import yfinance as yf
from financial_system.models import *


def populate_stock(symbols):
    tickers = yf.Tickers(" ".join(symbols).lower())
    tickers_dic = tickers.tickers
    results = {}  # To store the success/failure status for each ticker

    for symbol in symbols:
        try:
            # Fetch historical data for the symbol
            tickers_dic[symbol].history(period="1mo")

            # Ensure the history_metadata attribute is available and properly structured
            if hasattr(tickers_dic[symbol], 'history_metadata'):
                Stock.create_stock_with_trading_periods_form_dict(tickers_dic[symbol].history_metadata)
                results[symbol] = 'Success'
            else:
                results[symbol] = 'Failed: history_metadata not available'
        except Exception as e:
            # Capture any errors that occur during the stock creation process
            results[symbol] = f'Failed: {str(e)}'

    return results


def populate_news(symbols):
    tickers = yf.Tickers(" ".join(symbols).lower())
    tickers_dic = tickers.tickers
    results = {}  # To store creation status of news articles for each symbol

    for symbol in symbols:
        if symbol in tickers_dic:
            news_items = tickers_dic[symbol].news
            for news_item in news_items:
                # Assuming news_item is a dictionary formatted as required by your News model
                article, created = News.create_from_dict(news_item)
                if created:
                    # If a new article was successfully created
                    results[news_item['uuid']] = 'Created successfully'
                else:
                    # If the article already existed and was not created
                    results[news_item['uuid']] = 'Already exists, not created'
        else:
            results[symbol] = 'Symbol not found in tickers dictionary'

    return results
