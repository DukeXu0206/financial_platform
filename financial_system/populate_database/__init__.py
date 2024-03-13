import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'financial_platform.settings')
django.setup()


from financial_system.populate_database.populate import *


def print_results(table_name, results):
    print(f"Populate {table_name} " + "*" * 30)
    for symbol, result in results.items():
        print(f'{symbol}: {result}')


# DATA
dow_30_symbols = [
    'BA', 'AXP', 'MSFT', 'GSHD', 'CSCO', 'MRK', 'AMGN', 'CRM', 'PG',
    'TRV', 'MMM', 'AMZN', 'CVX', 'KO', 'AAPL', 'DIS', 'CAT', 'DOW',
    'HON', 'UNH', 'WMT', 'INTC', 'IBM', 'VZ', 'JNJ', 'JPM', 'NKE', 'MCD'
]

# Populate
stock_results = populate_stock(dow_30_symbols)
print_results("Stock", stock_results)

news_results = populate_news(dow_30_symbols)
print_results("News", news_results)

populate_user()
populate_manager()

stocks = Stock.objects.all()
users = User.objects.all()[:5]

populate_watchlist(users, stocks)
populate_history_trade(users, dow_30_symbols)

populate_comments(users[0], stocks)
populate_reply(users[2])

populate_notifications(users[:2])
populate_feedback(users)
