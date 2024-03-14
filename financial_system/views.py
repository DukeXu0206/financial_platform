import json

from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseRedirect
from yfinance import Ticker

from django.urls import reverse

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Case, When, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now

from financial_system.models import *


def base(request):
    return render(request, 'base.html')


def index(request):
    user_id = request.session.get('user_id')
    if user_id:
        return redirect('financial_system:user_watchlist_view')
    else:
        return redirect('financial_system:login')


def sign_up_view(request, message=None):
    # if message:
    #     return render(request, 'sign_up.html', {'message': message})
    return render(request, 'sign_up.html')


def register_action(request):
    user_name = request.POST.get('user_name')
    phone_number = request.POST.get('phone_number')
    user_gender = request.POST.get('user_gender')
    user_email = request.POST.get('user_email')
    password = request.POST.get('password')

    existing_user = User.objects.filter(phone_number=phone_number).first()

    if existing_user:
        messages.add_message(request, messages.ERROR, "A user with this phone number already exists.")
        return render(request, 'sign_up.html')

    try:
        user = User.objects.create(
            user_name=user_name,
            user_email=user_email,
            user_gender=user_gender,
            # user_id=str(uuid.uuid4())[:8],
            password=password,
            phone_number=phone_number
        )

        user.save()
        print("Success register user")
        print(user)

        message = "Registration successful!"
        messages.add_message(request, messages.SUCCESS, message)

    except Exception as e:
        print("An exception occurred:", e)
        message = "Registration failed, please check and try again later!"  # Including the message in the context
        messages.add_message(request, messages.ERROR, message)
        return render(request, 'sign_up.html')

    # 跳转到登录
    return redirect('financial_system:login')


def login_view(request, message=None):
    # if message:
    #     return render(request, 'login.html', {"message": message})
    return render(request, 'login.html')


def login_action(request):
    # 10030370820
    # 222222
    if request.POST:
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        print(phone_number)
        print(password)
        try:
            user = User.objects.get(phone_number=phone_number, password=password)
            login(request, user)
            # user_num = User.objects.count()
            request.session['user_id'] = user.user_id
            request.session['phone_number'] = phone_number
            # return redirect('financial_system:adm_index')
            return redirect('financial_system:user_watchlist_view')
        except ObjectDoesNotExist:
            try:
                user = User.objects.get(phone_number=phone_number)
                if user.password == password:
                    login(request, user)
                    request.session['user_name'] = user.user_name
                    request.session['user_id'] = user.user_id
                    request.session['user_email'] = user.user_email
                    request.session['phone_number'] = user.phone_number
                    return redirect('financial_system:index')
                else:
                    message = "Password incorrect."
                    messages.add_message(request, messages.ERROR, message)
            except ObjectDoesNotExist:
                message = "User does not exist."
                messages.add_message(request, messages.ERROR, message)

        return render(request, 'login.html')


def log_out(request):
    logout(request)
    request.session.flush()
    return redirect('financial_system:login')


def user_profile_view(request):
    try:
        # user = User.objects.get(phone_number=request.session['phone_number'])
        user = User.objects.get(user_id=request.session.get('user_id'))

        context = {
            'user': user
        }

        return render(request, 'user_profile.html', context)

    except Exception:
        # 根据后端意思，继续渲染到user_watchlist ，但是显示未登录界面
        context = {
            'user': None,
            'tips': "User not recognized, please login.",
        }
        return render(request, 'user_watchlist.html', context)


# @login_required
def edit_user_profile_action(request):
    message = ""
    try:
        print("-" * 30)
        print("edit_user_profile_action")

        user = User.objects.get(user_id=request.session.get('user_id'))
        print("user: " + str(user))

        if request.POST:
            user_name = request.POST.get('user_name')
            phone_number = request.POST.get('phone_number')
            user_gender = request.POST.get('user_gender')
            user_email = request.POST.get('user_email')
            new_password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if confirm_password == new_password:
                try:
                    user.user_name = user_name
                    user.phone_number = phone_number
                    user.user_gender = user_gender
                    user.user_email = user_email
                    if new_password:
                        user.password = new_password  # Use set_password to properly hash the password

                    if 'photo' in request.FILES:
                        user.photo = request.FILES['photo']

                    user.save()
                    message = "Profile updated successfully."
                    messages.add_message(request, messages.SUCCESS, message)

                except Exception as e:
                    print(e)
                    message = "Failed to update information, please check carefully or try again later."
                    messages.add_message(request, messages.ERROR, message)

                else:
                    message = "Password mismatch!"
                    messages.add_message(request, messages.ERROR, message)


        # context = {
        #     'message': message,
        # }

        return redirect('financial_system:user_profile')

    except ObjectDoesNotExist:
        message = "User not recognized, please login."
        messages.add_message(request, messages.ERROR, message)

        return render(request, 'login.html')


def deposit_funds(request):
    amount = request.POST.get('amount')

    try:
        amount = float(amount)
        user = User.objects.get(user_id=request.session.get('user_id'))
        user.account_balance += amount
        user.save()
        message = "Successful Deposit"
        messages.add_message(request, messages.SUCCESS, message)

        context = {
            'user': user,
        }

        return render(request, 'balance.html', context)
    except ValueError:
        message = "Please introduce a valid amount (decimal value)."
        messages.add_message(request, messages.ERROR, message)

        return render(request, 'balance.html')


def withdraw_funds(request):
    amount = request.POST.get('amount')

    try:
        amount = float(amount)
        user = User.objects.get(user_id=request.session.get('user_id'))
        if user.account_balance >= amount:
            user.account_balance -= amount
            user.save()
            message = "Successful Withdraw"
            messages.add_message(request, messages.SUCCESS, message)
        else:
            message = "Insufficient balance, unsuccessful withdraw."
            messages.add_message(request, messages.ERROR, message)

        context = {
            'user': user,
        }

        return render(request, 'balance.html', context)

    except ValueError:
        message = "Please introduce a valid amount (decimal value)."
        messages.add_message(request, messages.ERROR, message)

        return render(request, 'balance.html')


def balance(request):
    try:
        user = User.objects.get(user_id=request.session.get('user_id'))
        context = {
            'user': user,
        }
        return render(request, 'balance.html', context)
    except ObjectDoesNotExist:
        # 根据后端意思，继续渲染到user_watchlist ，但是显示未登录界面
        context = {
            'user': None,
            'tips': "User not recognized, please login.",
        }
        return render(request, 'user_watchlist.html', context)


def add_to_watchlist(request, stock_symbol):
    previous_url = request.META.get('HTTP_REFERER')
    try:
        user_id = request.session.get('user_id')
        user = User.objects.get(user_id=user_id)
        stock = get_object_or_404(Stock, symbol=stock_symbol)
        Watchlist.objects.create(user_id=user, stock_symbol=stock)
        messages.add_message(request, messages.SUCCESS, f"{stock_symbol} successfully added to your Watchlist.")

    except IntegrityError:
        messages.add_message(request, messages.INFO, f"{stock_symbol} is already in your Watchlist.")

    except ValidationError as e:
        messages.add_message(request, messages.ERROR, "Failed to add to Watchlist due to invalid data.")
    except Exception as e:
        messages.add_message(request, messages.ERROR, "An unexpected error occurred. Please try again later.")

    return HttpResponseRedirect(previous_url)


def remove_from_watchlist(request, stock_symbol):
    previous_url = request.META.get('HTTP_REFERER', '/')
    try:
        user_id = request.session.get('user_id')
        if not user_id:
            raise Exception("User not logged in.")

        user = get_object_or_404(User, user_id=user_id)
        stock = get_object_or_404(Stock, symbol=stock_symbol)

        # Attempt to find the watchlist item and delete it
        watchlist_item = Watchlist.objects.get(user_id=user, stock_symbol=stock)
        watchlist_item.delete()

        message = f"{stock_symbol} successfully removed from Watchlist"
        messages.add_message(request, messages.SUCCESS, message)
    except Watchlist.DoesNotExist:
        message = f"{stock_symbol} is not in your Watchlist"
        messages.add_message(request, messages.INFO, message)
    except Exception as e:
        print(e)  # Log the error for debugging
        message = "Failed to remove from Watchlist, please try again later."
        messages.add_message(request, messages.ERROR, message)

    return HttpResponseRedirect(previous_url)


def user_watchlist_view(request, stock_symbol=None):
    try:
        user_id = request.session.get('user_id')
        user = User.objects.get(user_id=user_id)
        stocks_in_watchlist = Stock.objects.filter(
            symbol__in=Watchlist.objects.filter(user_id=user.user_id).values_list('stock_symbol', flat=True)
        )

        context = {}

        # all_trades = HistoryTrade.objects.filter(user_id=user).order_by('-trade_dateTime')
        # 获取某个stockid，如果没有就选其一
        if stock_symbol:
            current_watch_stock = Stock.objects.get(symbol=stock_symbol)
        else:
            current_watch_stock = stocks_in_watchlist[0] if stocks_in_watchlist else None

        if current_watch_stock:
            ticker = Ticker(current_watch_stock.symbol)

            historical_data_period = request.GET.get("period") if request.GET.get("period") is not None else "1mo"
            # Historical data for a given period
            historical_data = ticker.history(period=historical_data_period)
            historical_data = historical_data.reset_index()

            # print(historical_data)
            historical_data['Date'] = historical_data['Date'].dt.strftime('%Y/%m/%d %H:%M:%S')
            # KLine data 整理
            kline_data = historical_data[['Date', 'Open', 'Close', 'Low', 'High']].values.tolist()
            print(kline_data)

            context.update({
                'current_watch_stock': current_watch_stock,
                'periods_list': current_watch_stock.validRanges.split(','),
                'historical_data': historical_data,
                'kline_data': json.dumps(kline_data),
            })

        open_positions, closed_positions, all_positions = HistoryTrade.get_positions_with_pl(user)

        total_pl_closed = sum(position['pl'] for position in closed_positions if position['pl'] is not None)

        print("all_positions:" + "*" * 30)
        print(all_positions)
        print("open_positions:" + "*" * 30)
        print(open_positions)
        print("closed_positions:" + "*" * 30)
        print(closed_positions)

        context.update({
            'user': user,
            'stocks_in_watchlist': stocks_in_watchlist,

            'all_positions': all_positions,
            'open_positions': open_positions,
            'closed_positions': closed_positions,
            'total_pl_closed': total_pl_closed,
        })

        return render(request, 'user_watchlist.html', context)

    except ObjectDoesNotExist:
        # 根据后端意思，继续渲染到user_watchlist ，但是显示未登录界面
        context = {
            'user': None,
            'tips': "User not recognized, please login.",
        }
        return render(request, 'user_watchlist.html', context)


def user_watchlist_monitor(request, stock_symbol=None):
    user_id = request.session.get('user_id')
    user = User.objects.get(user_id=user_id)
    stocks_in_watchlist = Stock.objects.filter(
        symbol__in=Watchlist.objects.filter(user_id=user.user_id).values_list('stock_symbol', flat=True)
    )
    data = list(stocks_in_watchlist.values())

    index = 0
    for item in stocks_in_watchlist:
        data[index]['get_company_name'] = item.get_company_name()
        data[index]['get_current_price'] = item.get_current_price()
        data[index]['get_open_price'] = item.get_current_price()
        index += 1
    return JsonResponse(data, safe=False)


def news_view(request):
    news_items = News.objects.all()

    for news_item in news_items:
        # Assuming relatedTickers is a comma-separated string of ticker symbols
        ticker_symbols = news_item.relatedTickers.split(',')
        # Initialize an empty list for relatedTickerURLs
        news_item.relatedTickerURLs = []

        for ticker in ticker_symbols:
            # Check if the ticker exists in the Stock model
            if Stock.objects.filter(symbol=ticker).exists():
                # Generate the URL only if the stock exists in the database
                url = reverse('financial_system:stock_detail', kwargs={'stock_symbol': ticker})
                news_item.relatedTickerURLs.append((ticker, url))

    context = {'news': news_items}

    return render(request, 'news.html', context)


def news_detail_view(request, news_id):
    news_item = get_object_or_404(News, news_id=news_id)
    return render(request, 'news_detail.html', {'news_item': news_item})


def stock_list_view(request):
    # Query all stocks
    stocks = Stock.objects.all()

    # Dictionary to map exchange abbreviations to full names
    exchange_names_mapping = {
        'NMS': 'NASDAQ Market Site',
        'NYQ': 'New York Stock Exchange',
        # Add more mappings as needed
    }

    # Group stocks by 'exchangeName', using full names
    stock_groups = {}
    for stock in stocks:
        # Generate the URL for the stock detail view
        detail_url = reverse('financial_system:stock_detail', kwargs={'stock_symbol': stock.symbol})

        # Get the full name of the exchange, falling back to the abbreviation if not found
        full_exchange_name = exchange_names_mapping.get(stock.exchangeName, stock.exchangeName)

        if full_exchange_name in stock_groups:
            stock_groups[full_exchange_name].append((stock, detail_url))
        else:
            stock_groups[full_exchange_name] = [(stock, detail_url)]

    context = {
        'stock_groups': stock_groups
    }

    return render(request, 'stock_list.html', context)


def stock_detail_view(request, stock_symbol):
    stock = get_object_or_404(Stock, symbol=stock_symbol)
    comments = StockComment.objects.filter(stock_symbol=stock.symbol).order_by('-comment_time')

    ticker = Ticker(stock.symbol)

    # Historical data for a given period

    historical_data_period = request.GET.get("period") if request.GET.get("period") is not None else "1mo"
    print("historical_data_period", historical_data_period)
    historical_data = ticker.history(period=historical_data_period)
    company_info = ticker.info
    historical_data = historical_data.reset_index()
    historical_data['Date'] = historical_data['Date'].dt.strftime('%Y/%m/%d %H:%M:%S')
    # KLine data 整理
    kline_data = historical_data[['Date', 'Open', 'Close', 'Low', 'High']].values.tolist()
    print(company_info)
    # print(ticker.recommendations)

    # Fetch additional data
    actions = ticker.actions
    dividends = ticker.dividends
    splits = ticker.splits
    earnings_dates = ticker.earnings_dates

    share_count = ticker.get_shares_full(start="2022-01-01", end=None)

    # Financial information
    # - income statement:
    income_statement = ticker.income_stmt
    quarterly_income_statement = ticker.quarterly_income_stmt

    # - balance
    balance_sheet = ticker.balance_sheet
    quarterly_balance_sheet = ticker.quarterly_balance_sheet

    # - cashflow
    cashflow = ticker.cashflow
    quarterly_cashflow = ticker.quarterly_cashflow

    # Holders
    major_holders = ticker.major_holders
    institutional_holders = ticker.institutional_holders
    mutualfund_holders = ticker.mutualfund_holders
    insider_transactions = ticker.insider_transactions

    # Recomendations
    recommendations = ticker.recommendations
    recommendations_summary = ticker.recommendations_summary
    upgrades_downgrades = ticker.upgrades_downgrades

    # News
    news = News.retrieve_news_by_uuids(ticker.news)
    print(news)

    add_comment_url = reverse('financial_system:add_comment', kwargs={'stock_symbol': stock.symbol})

    context = {
        'stock': stock,
        'comments': comments,
        'add_comment_url': add_comment_url,
        'periods_list': stock.validRanges.split(','),
        'historical_data': historical_data,
        'company_info': company_info,
        'actions': actions,
        'dividends': dividends,
        'splits': splits,
        'share_count': share_count,
        'income_statement': income_statement.to_html(classes='table table-bordered table-responsive-sm'),
        'quarterly_income_statement': quarterly_income_statement.to_html(
            classes='table table-bordered table-responsive-sm'),
        'balance_sheet': balance_sheet.to_html(classes='table table-bordered table-responsive-sm'),
        'quarterly_balance_sheet': quarterly_balance_sheet.to_html(classes='table table-bordered table-responsive-sm'),
        'cashflow': cashflow.to_html(classes='table table-bordered table-responsive-sm'),
        'quarterly_cashflow': quarterly_cashflow.to_html(classes='table table-bordered table-responsive-sm'),
        'major_holders': major_holders.to_html(classes='table table-bordered table-responsive-sm'),
        'institutional_holders': institutional_holders,
        'mutualfund_holders': mutualfund_holders,
        'insider_transactions': insider_transactions,
        'recommendations': recommendations.to_html(classes='table table-bordered table-responsive-sm'),
        'recommendations_summary': recommendations_summary.to_html(classes='table table-bordered table-responsive-sm'),
        'upgrades_downgrades': upgrades_downgrades,
        'earnings_dates': earnings_dates,
        'news': news,
        "kline_data": kline_data
    }

    user_id = request.session.get('user_id')

    if user_id:
        user = User.objects.get(user_id=request.session.get('user_id'))
        is_in_watchlist = Watchlist.is_in_watchlist(user, stock)

        if is_in_watchlist:
            context.update({
                'is_in_watchlist': is_in_watchlist,
            })

    return render(request, 'stock_detail.html', context)


def stock_current_price(request):
    # historical_data_period = "1mo"
    stock_symbol = request.POST.get('stock_symbol')
    stock = get_object_or_404(Stock, symbol=stock_symbol)
    data = {
        "get_current_price": stock.get_current_price(),
        "get_change_extent": stock.get_change_extent(),
    }
    return JsonResponse(data)


def trade(request, stock_symbol):
    stock = get_object_or_404(Stock, symbol=stock_symbol)
    user = User.objects.get(user_id=request.session.get('user_id'))
    average_buy_price, buy_trades = HistoryTrade.get_average_buy_price(user, stock)
    average_sell_price, sell_trades = HistoryTrade.get_average_sell_price(user, stock)

    context = {
        'stock': stock,
        'user': user,
        'buy_trades': buy_trades,
        'average_buy_price': average_buy_price,
        'sell_trades': sell_trades,
        'average_sell_price': average_sell_price,
    }

    return render(request, 'trade.html', context)


def buy_stock(request):
    if request.method == "POST":
        stock_symbol = request.POST.get('stock_symbol')
        try:
            quantity = int(request.POST.get('buy_quantity'))
            current_price = float(request.POST.get('current_price'))

            stock = get_object_or_404(Stock, pk=stock_symbol)
            user = User.objects.get(user_id=request.session.get('user_id'))

            total_cost = current_price * quantity

            if user.account_balance >= total_cost:
                user.account_balance -= total_cost
                user.save()
                # Record the transaction
                HistoryTrade.objects.create(
                    user_id=user,
                    stock_symbol=stock,
                    trade_price=current_price,
                    trade_quantity=quantity,
                    trade_dateTime=now(),
                    trade_type='BUY',
                )
                return redirect('financial_system:user_watchlist_view')
            else:
                message = "Insufficient balance, please deposit."
                messages.add_message(request, messages.ERROR, message)
                return redirect(
                    reverse('financial_system:trade', kwargs={'stock_symbol': stock_symbol}))


        except ValueError:
            message = "Invalid input."
            messages.add_message(request, messages.ERROR, message)
            return redirect(
                reverse('financial_system:trade', kwargs={'stock_symbol': stock_symbol}))


def sell_stock(request):
    if request.method == "POST":
        stock_symbol = request.POST.get('stock_symbol')
        try:
            quantity = int(request.POST.get('sell_quantity'))
            current_price = float(request.POST.get('current_price'))
            stock = get_object_or_404(Stock, pk=stock_symbol)
            user = User.objects.get(user_id=request.session.get('user_id'))

            trades = HistoryTrade.objects.filter(user_id=user.user_id, stock_symbol=stock.symbol).aggregate(
                total_bought=Sum(
                    Case(When(trade_type='BUY', then='trade_quantity'), output_field=models.IntegerField(), default=0)),
                total_sold=Sum(
                    Case(When(trade_type='SELL', then='trade_quantity'), output_field=models.IntegerField(), default=0))
            )

            total_owned = trades['total_bought'] - trades['total_sold']

            if total_owned >= quantity:
                total_revenue = current_price * quantity

                user.account_balance += total_revenue
                user.save()
                HistoryTrade.objects.create(
                    user_id=user,
                    stock_symbol=stock,
                    trade_price=current_price,
                    trade_quantity=quantity,
                    trade_type='SELL',
                    trade_dateTime=now()
                )

                return redirect('financial_system:user_watchlist_view')
            else:
                message = "Insufficient stock to sell."
                messages.add_message(request, messages.ERROR, message)
                return redirect(
                    reverse('financial_system:trade', kwargs={'stock_symbol': stock_symbol}))

        except ValueError:
            message = "Invalid input."
            messages.add_message(request, messages.ERROR, message)
            return redirect(
                reverse('financial_system:trade', kwargs={'stock_symbol': stock_symbol}))


def add_comment(request, stock_symbol):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        user = User.objects.get(user_id=request.session.get('user_id'))
        stock = get_object_or_404(Stock, pk=stock_symbol)

        StockComment.objects.create(title=title, content=content, user_id=user, stock_symbol=stock)

    return redirect(reverse('financial_system:stock_detail', kwargs={'stock_symbol': stock_symbol}))


def add_reply(request):
    if request.method == "POST":
        content = request.POST.get('content')
        comment_id = request.POST.get('comment_id')
        user = User.objects.get(user_id=request.session.get('user_id'))
        comment = get_object_or_404(StockComment, pk=comment_id)

        CommentReply.objects.create(content=content, user_id=user, comment_id=comment)

        return redirect(reverse('financial_system:stock_detail', kwargs={'stock_symbol': comment.stock_symbol}))

    # return redirect('stock_comments', stock_symbol=comment_id.stock_symbol.pk)


def user_notification_view(request):
    notifications = UserNotification.objects.filter(user_id=request.session['user_id'])

    context = {
        "notifications": notifications
    }

    return render(request, 'user_notifications.html', context)


def submit_feedback(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        title = request.POST.get('title')
        content = request.POST.get('content')

        user = User.objects.get(user_id=request.session.get('user_id')) \
            if request.session.get('user_id') else None

        Feedback.objects.create(user=user, email=email, title=title, content=content)
        messages.add_message(request, messages.SUCCESS, "Thank you for your feedback!")
        return redirect('financial_system:index')  # Adjust the redirect as needed

    return render(request, 'submit_feedback.html')


def search_view(request):
    query = request.GET.get('query', '').strip()
    if query != "":
        query_tokens = query.split()

        print(query)
        print(query_tokens)

        filtered_stocks = []
        stock_symbols = []

        for stock in Stock.objects.all():
            info = stock.get_company_info()  # This needs to be optimized for performance.
            shortName = info.get('shortName', '').lower()

            # Check if any token matches.
            symbol_match = any(token.upper() in stock.symbol for token in query_tokens)
            shortName_match = any(token.lower() in shortName for token in query_tokens)
            sector_match = any(query_token.lower() in info.get('sector', '').lower() for query_token in query_tokens)

            if symbol_match or shortName_match or sector_match:
                stock_url = reverse('financial_system:stock_detail', kwargs={'stock_symbol': stock.symbol})
                filtered_stocks.append((stock, stock_url))
                stock_symbols.append(stock.symbol.upper())

        print(filtered_stocks)

        # filtered_news = []
        # filtered_news.append(
        #     news for news in News.objects.filter(Q(title__icontains=query) | Q(publisher__icontains=query)))

        filtered_news = list(News.objects.filter(Q(title__icontains=query) | Q(publisher__icontains=query)))

        for news_item in News.objects.all():
            related_tickers_list = [ticker.strip().upper() for ticker in
                                    news_item.relatedTickers.split(',')] if news_item.relatedTickers else []
            if set(related_tickers_list) & set(
                    stock_symbols):  # Intersection of related tickers and filtered stock symbols
                if news_item not in filtered_news:  # Avoid duplicating news items
                    filtered_news.append(news_item)

        context = {
            'query': query,
            'filtered_news': filtered_news,
            'filtered_stocks': filtered_stocks,
        }
    else:
        context = {
            'query': query,
        }
    return render(request, 'search_results.html', context)
