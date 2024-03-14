# financial_platform

## Introduction
Welcome to the Financial Platform! Our platform is tailored for users interested in stocks, providing a rich set of features including personalized news feeds, detailed analyses, trading features, and a community space for sharing insights.

## User Guide
### Getting Started
- Creating an Account
To create an account, navigate to our 'Sign Up' page at http://fin.pythonanywhere.com/sign_up/ and complete the registration form.
- Logging In
Access the 'Login' page to enter your credentials and sign in to your account.

### Navigating the Website
Upon logging in, you'll be taken to the 'Trading & Watchlist'. This is your personal space where you can monitor your 'watchlist', and see a summary of your 'balance' and 'trades'.
Apart from that, you can catch up on 'News' and 'Stock Market'.

### Managing Your Watchlist
-Adding and Removing Stocks
To add a stock to your watchlist, go to the 'Stock Market' page to find the stocks you're interested in, then click the 'star' button to add or remove to/from watchlist.
-Buying and Selling Stocks
Visit the 'Trade' section to engage in buying or selling. Select the product and the desired quantity, then confirm your transaction details on 'Trading History' section of the 'Trading & Watchlist' page.

## Features
### For Users:
- Account Management: Utilize 'Sign Up', and 'Profile' to create, access and edit your account.
- Secure Authentication: Log in and out securely with our 'Login' system.
- Trading: Engage in buying or selling on the 'Trade' page
- Trading & Watchlist：View for trade summaries, monitor your positions and P&L, and follow up with interested stocks.
- Interactive Data Visualization: Access financial 'Stock Market' and 'Stock' charts and analyses tailored to your preferences.
- Balance: Check your account balance and execute fund deposits or withdraws.
- Notifications


### For Managers:
- User Management: Create, read, update, and delete 'Users'.
- News Management: Create, read, update, and delete 'News'.
- Stock Management: Create, read, update, and delete 'Stocks'.
- Stock Comment Management: Create, read, update, and delete 'Stock Comments'.
- Trade History Management: Create, read, update, and delete 'Trade Histories'.
- User Nofication Management: Create, read, update, and delete 'User Notifications'.


## Implementation
Our platform integrates various technologies such as Django, Bootstrap, and AJAX to deliver a responsive and feature-rich user experience, as well as APIs like yfinance (to fetch real-time stock and news data from Yahoo Finance), echart (to display candlestickers of historical stock prices based on a period range determined by the user), and simpleui (to render a clean and attractive manager side UI).

