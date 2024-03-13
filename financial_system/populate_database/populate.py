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


def populate_user():
    users_data = [
        {'user_name': 'Alice', 'password': 'password123', 'user_gender': 'Female', 'phone_number': '1234567890',
         'user_email': 'alice@example.com'},
        {'user_name': 'Bob', 'password': 'password123', 'user_gender': 'Male', 'phone_number': '2345678901',
         'user_email': 'bob@example.com'},
        {'user_name': 'Charlie', 'password': 'password123', 'user_gender': 'Male', 'phone_number': '3456789012',
         'user_email': 'charlie@example.com'},
        {'user_name': 'Diana', 'password': 'password123', 'user_gender': 'Female', 'phone_number': '4567890123',
         'user_email': 'diana@example.com'},
        {'user_name': 'Eve', 'password': 'password123', 'user_gender': 'Female', 'phone_number': '5678901234',
         'user_email': 'eve@example.com'}
    ]

    for user_data in users_data:
        user = User(**user_data)
        user.save()

    print(User.objects.all())


def populate_manager():
    managers_data = [
        {
            'manager_name': 'Manager1',
            'password': 'securepassword1',  # Consider using Django's make_password for hashing
            'phone_number': '1111111111',
            'photo_url': 'url/to/manager1/photo',
        },
        {
            'manager_name': 'Manager2',
            'password': 'securepassword2',  # Consider using Django's make_password for hashing
            'phone_number': '2222222222',
            'photo_url': 'url/to/manager2/photo',
        },
    ]

    # Iterate over each dictionary in the list and create Manager instances
    for manager_data in managers_data:
        manager = Manager(**manager_data)
        manager.save()

    print(Manager.objects.all())


stocks = Stock.objects.all()
users = User.objects.all()

def populate_watchlist():
    # Add 10 Watchlist entries for the first 2 users, 2 for the rest
    for i, user in enumerate(users):
        watchlist_stocks = stocks[:10] if i < 2 else stocks[:2]
        for stock in watchlist_stocks:
            Watchlist.objects.create(user_id=user, stock_symbol=stock)

    print(Watchlist.objects.all())


# def populate_