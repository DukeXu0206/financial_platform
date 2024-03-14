from django.test import TestCase
from django.urls import reverse
from financial_system.models import *

user = User.objects.create_user(user_name='testuser', password='12345', phone_number='111', account_balance=1000)

class SignUpTestCase(TestCase):

    def test_register_action_success(self):
        # Simulate valid form submission
        response = self.client.post(reverse('financial_system:register_action'), {
            'user_name': 'testuser',
            'phone_number': '1234567890',
            'user_gender': 'Male',
            'user_email': 'test@example.com',
            'password': 'testpassword',
        })
        # Check that the user was created
        self.assertTrue(User.objects.filter(user_name='testuser').exists())
        # Verify that the response redirects to the login page
        self.assertRedirects(response, reverse('financial_system:login'))

    def test_register_action_failure(self):
        # Simulate invalid form submission (e.g., missing fields)
        response = self.client.post(reverse('financial_system:register_action'), {})
        # Verify that the user was not created
        self.assertFalse(User.objects.exists())
        # Check that the form is rendered again with an error message
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        self.assertContains(response, "Registration failed")


class LoginActionTestCase(TestCase):
    def test_login_success(self):
        response = self.client.post(reverse('financial_system:login_action'), {
            'phone_number': 'testuser',
            'password': '12345',
        })
        self.assertRedirects(response, reverse('financial_system:user_watchlist_view'))

    def test_login_failure(self):
        response = self.client.post(reverse('financial_system:login_action'), {
            'phone_number': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, "Password incorrect or user does not exist.")


class AddToWatchlistTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.stock = Stock.objects.create(
            currency="USD",
            symbol="AAPL",
            exchangeName="NASDAQ",
            instrumentType="EQUITY",
            firstTradeDate=946684800,  # Example timestamp for 2000-01-01
            regularMarketTime=1610236800,  # Example timestamp for 2021-01-10
            regularMarketPrice=130.00
        )

    def test_add_to_watchlist(self):
        self.client.login('111', password='12345')
        response = self.client.post(reverse('financial_system:add_to_watchlist', args=[self.stock.symbol]))
        self.assertTrue(Watchlist.objects.filter(user_id=user, stock_symbol=self.stock).exists())
        self.assertRedirects(response, reverse('financial_system:user_watchlist_view'))

    def test_add_to_watchlist_not_logged_in(self):
        response = self.client.post(reverse('financial_system:add_to_watchlist', args=[self.stock.symbol]))
        self.assertFalse(Watchlist.objects.exists())
        self.assertRedirects(response, reverse('financial_system:user_watchlist_view'))


class StockTradeTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.stock = Stock.objects.create(symbol='AAPL', regularMarketPrice=150)

    def test_buy_stock_success(self):
        self.client.login('111', password='12345')
        response = self.client.post(reverse('financial_system:buy_stock'), {
            'stock_symbol': self.stock.symbol,
            'buy_quantity': 2,
            'current_price': 150,
        })
        # Check if the stock is added to the user's trades
        self.assertTrue(HistoryTrade.objects.filter(user_id=user, trade_type='BUY').exists())
        # Update the user object to reflect changes
        user.refresh_from_db()
        self.assertEqual(user.account_balance, 700)  # 1000 - 2*150

    def test_sell_stock_success(self):
        # Assume the user already has 2 units of AAPL stock from previous buy trades
        HistoryTrade.objects.create(user_id=user, stock_symbol=self.stock, trade_type='BUY', trade_price=150, trade_quantity=2)
        self.client.login('111', password='12345')
        response = self.client.post(reverse('financial_system:sell_stock'), {
            'stock_symbol': self.stock.symbol,
            'sell_quantity': 1,
            'current_price': 200,
        })
        # Check if the sell trade was successful
        self.assertTrue(HistoryTrade.objects.filter(user_id=user, trade_type='SELL').exists())
        user.refresh_from_db()
        self.assertEqual(user.account_balance, 900)  # 700 + 1*200

    def test_buy_stock_insufficient_funds(self):
        self.client.login('111', password='12345')
        response = self.client.post(reverse('financial_system:buy_stock'), {
            'stock_symbol': self.stock.symbol,
            'buy_quantity': 10,  # Attempt to buy more than the user can afford
            'current_price': 150,
        })
        self.assertFalse(HistoryTrade.objects.filter(user_id=user, trade_type='BUY', trade_quantity=10).exists())
        self.assertContains(response, "Insufficient balance")

    def test_sell_stock_not_owned(self):
        self.client.login('111', password='12345')
        response = self.client.post(reverse('financial_system:sell_stock'), {
            'stock_symbol': self.stock.symbol,
            'sell_quantity': 5,  # Attempt to sell more than owned
            'current_price': 200,
        })
        self.assertFalse(HistoryTrade.objects.filter(user_id=user, trade_type='SELL', trade_quantity=5).exists())
        self.assertContains(response, "Insufficient stock to sell")


# class SubmitFeedbackTestCase(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.user = User.objects.create_user(username='testuser', email='test@example.com', password='12345')
#
#     def test_submit_feedback_authenticated(self):
#         self.client.login('111', password='12345')
#         response = self.client.post(reverse('financial_system:submit_feedback'), {
#             'email': 'test@example.com',
#             'title': 'Feedback Title',
#             'content': 'Feedback content.',
#         })
#         self.assertTrue(Feedback.objects.filter(title='Feedback Title').exists())
#         self.assertRedirects(response, reverse('financial_system:index'))
#
#     def test_submit_feedback_unauthenticated(self):
#         response = self.client.post(reverse('financial_system:submit_feedback'), {
#             'email': 'test@example.com',
#             'title': 'Feedback Title',
#             'content': 'Feedback content.',
#         })
#         # Assuming the feedback form can be submitted by unauthenticated users
#         self.assertTrue(Feedback.objects.filter(title='Feedback Title').exists())
#         self.assertRedirects(response, reverse('financial_system:index'))

