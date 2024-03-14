import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'financial_platform.settings')
django.setup()

from django.utils import timezone
import random
from datetime import timedelta

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
         'user_email': 'alice@example.com', 'account_balance': 10000},
        {'user_name': 'Bob', 'password': 'password123', 'user_gender': 'Male', 'phone_number': '2345678901',
         'user_email': 'bob@example.com', 'account_balance': 20000},
        {'user_name': 'Charlie', 'password': 'password123', 'user_gender': 'Male', 'phone_number': '3456789012',
         'user_email': 'charlie@example.com', 'account_balance': 30000},
        {'user_name': 'Diana', 'password': 'password123', 'user_gender': 'Female', 'phone_number': '4567890123',
         'user_email': 'diana@example.com', 'account_balance': 40000},
        {'user_name': 'Eve', 'password': 'password123', 'user_gender': 'Female', 'phone_number': '5678901234',
         'user_email': 'eve@example.com', 'account_balance': 50000}
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

    # print(Manager.objects.all())


def populate_watchlist(users, stocks):
    # Add 10 Watchlist entries for the first 2 users, 2 for the rest
    for i, user in enumerate(users):
        watchlist_stocks = stocks[:10] if i < 2 else stocks[:2]
        for stock in watchlist_stocks:
            Watchlist.objects.create(user_id=user, stock_symbol=stock)

    print(Watchlist.objects.all())


def create_trades_for_user(user, symbols):
    # First, create 8 buy trades with different stocks
    for symbol in symbols[:8]:
        stock = Stock.objects.get(symbol=symbol)
        HistoryTrade.objects.create(
            user_id=user,
            stock_symbol=stock,
            trade_price=100,  # Example price
            trade_quantity=10,  # Example quantity
            trade_dateTime=timezone.now() - timedelta(days=random.randint(1, 30)),
            trade_type='BUY'
        )

    # Then, create 5 sell trades, reusing some of the previously bought stocks
    for symbol in symbols[3:8]:  # Reuse some stocks for selling
        stock = Stock.objects.get(symbol=symbol)
        HistoryTrade.objects.create(
            user_id=user,
            stock_symbol=stock,
            trade_price=100,  # Example price, assuming flat for simplicity
            trade_quantity=5,  # Example quantity, assuming some sold
            trade_dateTime=timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            trade_type='SELL'
        )


def populate_history_trade(users, symbols):
    for user in users:
        create_trades_for_user(user, symbols)
    print(HistoryTrade.objects.all())


def populate_comments(user, stocks):
    stocks = stocks[:10]

    comments_data = [
        {'title': 'Great Stock', 'content': 'This stock has been performing really well. Highly recommend!'},
        {'title': 'Undervalued Gem',
         'content': 'This stock is currently undervalued and presents a great buying opportunity.'}
    ]

    for stock in stocks:
        for comment_data in comments_data:
            # Create and save the comment for the current stock
            StockComment.objects.create(
                title=comment_data['title'],
                content=comment_data['content'],
                comment_time=timezone.now() - timedelta(days=random.randint(1, 30)),
                user_id=user,
                stock_symbol=stock
            )

    print(StockComment.objects.all())


def populate_reply(user):
    comments = StockComment.objects.all()

    # Sample reply content
    reply_content = "Thank you for your insight!"

    for comment in comments:
        # Create a reply for each comment
        CommentReply.objects.create(
            comment_id=comment,
            user_id=user,
            reply_time=timezone.now() - timedelta(hours=random.randint(1, 24)),
            # Randomize reply time within the last 24 hours
            content=reply_content
        )

    print(CommentReply.objects.all())


def populate_notifications(users):
    notifications_data = [
        {'title': 'System Update', 'message': 'We will be performing a system update this weekend.'},
        {'title': 'New Feature', 'message': 'Check out our new feature in the latest app update!'}
    ]

    for user in users:
        for notification_data in notifications_data:
            UserNotification.objects.create(user=user, **notification_data)

    print(UserNotification.objects.all())


def populate_feedback(users):
    feedback_list = [
        {'title': 'Great App!', 'content': 'Really enjoyed using this app. Great work!'},
        {'title': 'Feature Request', 'content': 'Could you add a dark mode?'},
        {'title': 'Bug Report',
         'content': 'Found a bug in the latest version, please check.'},
        {'title': 'Thank You!',
         'content': 'Thank you for the constant updates and improvements.'}
    ]

    for i, feedback_data in enumerate(feedback_list):
        user = users[i]
        Feedback.objects.create(user=user, **feedback_data)

    print(Feedback.objects.all())
