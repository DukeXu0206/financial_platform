from django.test import TestCase
from financial_system.models import *

class UserModelTests(TestCase):
    def setUp(self):
        # Setup run before every test method.
        self.user = User.objects.create(
            user_name="TestUser",
            password="TestPassword",
            user_gender="Male",
            phone_number="1234567890",
            user_email="test@example.com",
            account_balance=100.00
        )

    def test_user_creation(self):
        # Test the user creation.
        self.assertEqual(self.user.user_name, "TestUser")
        self.assertEqual(self.user.account_balance, 100.00)

class StockModelTests(TestCase):
    def setUp(self):
        # Create a stock instance for testing.
        self.stock = Stock.objects.create(
            currency="USD",
            symbol="AAPL",
            exchangeName="NASDAQ",
            instrumentType="EQUITY",
            firstTradeDate=946684800,  # Example timestamp for 2000-01-01
            regularMarketTime=1610236800,  # Example timestamp for 2021-01-10
            regularMarketPrice=130.00
        )

    def test_stock_info(self):
        # Test stock information.
        self.assertEqual(self.stock.symbol, "AAPL")
        self.assertEqual(self.stock.get_company_name(), "Apple Inc.")

class WatchlistTests(TestCase):
    def test_watchlist_functionality(self):
        # Assuming you have user and stock setup methods.
        user = User.objects.get(user_email="test@example.com")
        stock = Stock.objects.get(symbol="AAPL")
        # Add stock to user's watchlist.
        watchlist_entry = Watchlist.objects.create(user_id=user, stock_symbol=stock)

        # Test if the stock is in the user's watchlist.
        self.assertTrue(Watchlist.is_in_watchlist(user, stock))


class HistoryTradeModelTests(TestCase):
    def setUp(self):
        # Assuming User and Stock setup methods are defined in setUp.
        self.user = User.objects.create(
            user_name="TraderJoe",
            password="securepassword",
            user_email="traderjoe@example.com"
        )
        self.stock = Stock.objects.create(
            symbol="TSLA",
            currency="USD",
            exchangeName="NASDAQ",
            instrumentType="EQUITY",
            regularMarketPrice=700.00
        )
        self.trade = HistoryTrade.objects.create(
            user_id=self.user,
            stock_symbol=self.stock,
            trade_price=705.00,
            trade_quantity=10,
            trade_type='BUY',
            trade_dateTime='2021-01-01 12:00:00'
        )

    def test_trade_creation(self):
        self.assertEqual(self.trade.trade_price, 705.00)
        self.assertEqual(self.trade.trade_quantity, 10)
        self.assertEqual(self.trade.user_id, self.user)
        self.assertEqual(self.trade.stock_symbol, self.stock)


class NewsModelTests(TestCase):
    def setUp(self):
        self.news_article = News.objects.create(
            uuid="123456789abcdef",
            title="Big News in Tech",
            publisher="TechCrunch",
            link="https://techcrunch.com/big-news-in-tech",
            providerPublishTime=datetime.now(),
            type="Article",
            photo_url="https://techcrunch.com/example-image.jpg",
            relatedTickers="AAPL,TSLA"
        )

    def test_news_article_creation(self):
        self.assertEqual(self.news_article.title, "Big News in Tech")
        self.assertIn("AAPL", self.news_article.relatedTickers)


class StockCommentModelTests(TestCase):
    def setUp(self):
        # Assuming User and Stock setup methods are defined in setUp.
        self.user = User.objects.create(
            user_name="Commenter",
            password="commentpassword",
            user_email="commenter@example.com"
        )
        self.stock = Stock.objects.create(
            symbol="GOOGL",
            currency="USD",
            exchangeName="NASDAQ"
        )
        self.comment = StockComment.objects.create(
            title="Interesting Development",
            content="This is a fascinating development in the stock.",
            user_id=self.user,
            stock_symbol=self.stock
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.title, "Interesting Development")
        self.assertEqual(self.comment.user_id, self.user)
        self.assertEqual(self.comment.stock_symbol, self.stock)


class UserNotificationModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.get(user_email="test@example.com")

        self.notification = UserNotification.objects.create(
            user=self.user,
            title="Notification Title",
            message="This is a test notification.",
            read=False
        )

    def test_notification_read_status(self):
        self.assertFalse(self.notification.read)
        # Simulate reading the notification
        self.notification.read = True
        self.notification.save()

        # Fetch from db and assert the change
        updated_notification = UserNotification.objects.get(id=self.notification.id)
        self.assertTrue(updated_notification.read)
