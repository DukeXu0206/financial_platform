from yfinance import Ticker

from django.urls import reverse

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Case, When, IntegerField, Q, F, FloatField
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now

from financial_system.models import *
# from financial_system.tests.yfinance_api import load


# from financial_system.yfinance_api import YFinanceApi


def base(request):
    return render(request, 'base.html')


def index(request):
    user_id = request.session.get('user_id')
    if user_id:
        return redirect('financial_system:user_watchlist_view')
    else:
        return redirect('financial_system:login')


def sign_up_view(request):
    return render(request, 'sign_up.html')


def register_action(request):
    user_name = request.POST.get('user_name')
    phone_number = request.POST.get('phone_number')
    user_gender = request.POST.get('user_gender')
    user_email = request.POST.get('user_email')
    password = request.POST.get('password')
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

    except Exception as e:
        print("An exception occurred:", e)
        message = "Registration failed, please check and try again later!"  # Including the message in the context
        return render(request, 'sign_up.html', {"message": message})

    # 跳转到登录
    return redirect('financial_system:login')


def login_view(request):
    return render(request, 'login.html')


def login_action(request):
    # 10030370820
    # 222222
    if request.POST:
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        print(phone_number)
        print(password)
        message = ''
        try:
            user = User.objects.get(phone_number=phone_number)
            login(request, user)
            user_num = User.objects.count()
            # stock_num = Stock.objects.count()
            request.session['user_id'] = user.user_id
            request.session['phone_number'] = phone_number
            # request.session['user_name'] = user.user_name
            # request.session['online'] = True
            # request.session['user_num'] = user_num
            # request.session['stock_num'] = stock_num
            # request.session['photo_url'] = ''

            # return redirect('financial_system:adm_index')
            return redirect('financial_system:user_watchlist_view')
        except ObjectDoesNotExist:
            try:
                user = User.objects.get(phone_number=phone_number)
                if user.password == password:
                    login(request, user)
                    request.session['user_name'] = user.user_name
                    # request.session['photo_url'] = user.photo_url
                    # print(user.photo_url)
                    # request.session['photo_url'] = '/static/img/avatar.png'
                    request.session['user_id'] = user.user_id
                    request.session['user_email'] = user.user_email
                    # request.session['account_balance'] = user.account_balance
                    request.session['phone_number'] = user.phone_number
                    return redirect('financial_system:index')
                else:
                    message = "Password incorrect."
            except ObjectDoesNotExist:
                message = "User does not exist."

        return render(request, 'login.html', {"message": message})


def log_out(request):
    logout(request)
    request.session.flush()
    return redirect('financial_system:login')


# @login_required
def user_profile_view(request):
    try:
        user = User.objects.get(phone_number=request.session['phone_number'])

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
        print("request.session['user_id']: " + str(request.session['user_id']))

        user = User.objects.get(user_id=request.session['user_id'])
        print("user: " + str(user))

        if request.POST:
            user_name = request.POST.get('user_name')
            phone_number = request.POST.get('phone_number')
            user_gender = request.POST.get('user_gender')
            user_email = request.POST.get('user_email')
            new_password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if confirm_password != new_password:
                message = "Password mismatched!"
            else:
                try:
                    user.user_name = user_name
                    user.phone_number = phone_number
                    user.user_gender = user_gender
                    user.user_email = user_email
                    if new_password:
                        user.set_password(new_password)  # Use set_password to properly hash the password

                    if 'photo' in request.FILES:
                        user.photo = request.FILES['photo']

                    user.save()
                    message = "Profile updated successfully."

                except Exception:
                    message = "Failed to update information, please check carefully or try again later."

        context = {
            'message': message,
        }

        return render(request, "user_profile.html", context)

    except ObjectDoesNotExist:
        message = "User not recognized, please login."
        context = {
            'message': message,
        }

        return render(request, 'login.html', context)


def deposit_funds(request):
    user = User.objects.get(user_id=request.session.get('user_id'))
    amount = request.POST.get('amount')
    user.balance += amount
    user.save()
    user = User.objects.get(user_id=request.session.get('user_id'))
    context = {
        'user': user,
    }
    return render(request, 'balance.html', context)


def withdraw_funds(request):
    amount = request.POST.get('amount')
    user = User.objects.get(user_id=request.session.get('user_id'))
    if user.balance >= amount:
        user.balance -= amount
        user.save()
        messages.success(request, "Successful Withdraw")
    else:
        messages.error(request, "Insufficient balance, unsuccessful withdraw.")
    user = User.objects.get(user_id=request.session.get('user_id'))
    context = {
        'user': user,
    }
    return render(request, 'balance.html', context)


def balance(request):
    try:

        user = User.objects.get(user_id=request.session.get('user_id'))
        context = {
            'user': user,
        }
        return render(request, 'balance.html', context)
    except ObjectDoesNotExist:
        context = {"message": "User not recognized, please login."}
        # 根据后端意思，继续渲染到user_watchlist ，但是显示未登录界面
        context = {
            'user': None,
            'tips': "User not recognized, please login.",
        }
        return render(request, 'user_watchlist.html', context)


def calculate_pnl(trades):
    # Aggregate the total spent on buys and the total earned from sells
    # trades = HistoryTrade.objects.filter(user_id=user_id).values('stock_symbol')\
    #     .annotate(
    #         total_spent=Sum(Case(When(trade_type='BUY', then=F('trade_quantity') * F('trade_price')), output_field=FloatField(), default=0)),
    #         total_earned=Sum(Case(When(trade_type='SELL', then=F('trade_quantity') * F('trade_price')), output_field=FloatField(), default=0)),
    #     )

    # Calculate P&L for each stock
    pnl_per_stock = [{**trade, 'pnl': trade['total_earned'] - trade['total_spent']} for trade in trades]

    # Calculate overall Gross P&L
    gross_pnl = sum([trade['pnl'] for trade in pnl_per_stock])

    return pnl_per_stock, gross_pnl


def user_watchlist_view(request, stock_symbol=None):
    try:
        user = User.objects.get(user_id=request.session.get('user_id'))
        stocks_in_watchlist = Stock.objects.filter(
            stock_symbol__in=Watchlist.objects.filter(user_id=user.user_id).values_list('stock_symbol', flat=True)
        )
        # all_trades = HistoryTrade.objects.filter(user_id=user).order_by('-trade_dateTime')
        # 获取某个stockid，如果没有就选其一
        if stock_symbol:
            current_watch_stock = Stock.objects.get(stock_symbol=stock_symbol)
        else:
            current_watch_stock = stocks_in_watchlist[0] if stocks_in_watchlist else None

        all_trades = HistoryTrade.objects.filter(user_id=user) \
            .values('stock_symbol') \
            .annotate(
            stock_name=F('stock_symbol__stock_name'),
            total_bought=Sum(
                Case(When(trade_type='BUY', then='trade_quantity'), output_field=IntegerField(), default=0)),
            total_sold=Sum(Case(When(trade_type='SELL', then='trade_quantity'), output_field=IntegerField(), default=0))
        )

        open_positions = [trade for trade in all_trades if trade['total_bought'] > trade['total_sold']]

        closed_positions = [trade for trade in all_trades if
                            trade['total_bought'] == trade['total_sold'] and trade['total_bought'] > 0]

        pnl_per_stock, gross_pnl = calculate_pnl(all_trades)

        context = {
            'user': user,
            'stocks_in_watchlist': stocks_in_watchlist,
            'current_watch_stock': current_watch_stock,
            'all_trades': all_trades,
            'open_positions': open_positions,
            'closed_positions': closed_positions,
            'pnl_per_stock': pnl_per_stock,
            'gross_pnl': gross_pnl,
            "page_title": "user watchlist",
        }

        return render(request, 'user_watchlist.html', context)

    except ObjectDoesNotExist:
        context = {"message": "User not recognized, please login."}
        # 根据后端意思，继续渲染到user_watchlist ，但是显示未登录界面
        context = {
            'user': None,
            'tips': "User not recognized, please login.",
        }
        return render(request, 'user_watchlist.html', context)


def news_view(request):
    news = News.objects.all()

    context = {'news': news, }
    return render(request, 'news.html', context)


def news_detail_view(request, news_id):
    news_item = get_object_or_404(News, news_id=news_id)
    return render(request, 'news_detail.html', {'news_item': news_item})


def stock_list_view(request):
    # Query all stocks
    stocks = Stock.objects.all()

    # Group stocks by 'exchangeName'
    stock_groups = {}
    for stock in stocks:
        # Generate the URL for the stock detail view
        detail_url = reverse('financial_system:stock_detail', kwargs={'stock_symbol': stock.symbol})

        if stock.exchangeName in stock_groups:
            stock_groups[stock.exchangeName].append((stock, detail_url))
        else:
            stock_groups[stock.exchangeName] = [(stock, detail_url)]

    context = {
        'stock_groups': stock_groups
    }

    return render(request, 'stock_list.html', context)


def stock_detail_view(request, stock_symbol, historical_data_period="1mo"):
    stock = get_object_or_404(Stock, symbol=stock_symbol)
    comments = StockComment.objects.filter(stock_symbol=stock.symbol).order_by('-comment_time')

    ticker = Ticker(stock.symbol)

    # Historical data for a given period
    historical_data = ticker.history(period=historical_data_period)
    company_info = ticker.info

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

    context = {
        'stock': stock,
        'historical_data': historical_data,
        'comments': comments,
        'company_info': company_info,
        'actions': actions,
        'dividends': dividends,
        'splits': splits,
        'share_count': share_count,
        'income_statement': income_statement,
        'quarterly_income_statement': quarterly_income_statement,
        'balance_sheet': balance_sheet,
        'quarterly_balance_sheet': quarterly_balance_sheet,
        'cashflow': cashflow,
        'quarterly_cashflow': quarterly_cashflow,
        'major_holders': major_holders,
        'institutional_holders': institutional_holders,
        'mutualfund_holders': mutualfund_holders,
        'insider_transactions': insider_transactions,
        'recommendations': recommendations,
        'recommendations_summary': recommendations_summary,
        'upgrades_downgrades': upgrades_downgrades,
        'earnings_dates': earnings_dates,
        'news': news
    }

    return render(request, 'stock_detail.html', context)


def trade(request, stock_symbol):
    stock = get_object_or_404(Stock, stock_symbol=stock_symbol)
    return render(request, 'trade.html', {'stock': stock})


def buy_stock(request):
    if request.method == "POST":
        stock_symbol = request.POST.get('stock_symbol')
        quantity = int(request.POST.get('quantity'))

        stock = get_object_or_404(Stock, pk=stock_symbol)
        user = User.objects.get(user_id=request.session.get('user_id'))

        total_cost = stock.current_price * quantity

        if user.balance >= total_cost:
            user.balance -= total_cost
            user.save()

            # Record the transaction
            HistoryTrade.objects.create(
                user_id=user,
                stock_symbol=stock,
                trade_price=stock.current_price,
                trade_quantity=quantity,
                trade_type='BUY',
            )
        else:
            messages.error(request, "Insufficient balance, please deposit.")


def sell_stock(request):
    if request.method == "POST":
        stock_symbol = request.POST.get('stock_symbol')
        quantity = int(request.POST.get('quantity'))
        stock = get_object_or_404(Stock, pk=stock_symbol)
        user = User.objects.get(user_id=request.session.get('user_id'))

        trades = HistoryTrade.objects.filter(user_id=user.user_id, stock_symbol=stock).aggregate(
            total_bought=Sum(
                Case(When(trade_type='BUY', then='trade_quantity'), output_field=models.IntegerField(), default=0)),
            total_sold=Sum(
                Case(When(trade_type='SELL', then='trade_quantity'), output_field=models.IntegerField(), default=0))
        )

        total_owned = trades['total_bought'] - trades['total_sold']

        if total_owned >= quantity:
            total_revenue = stock.current_price * quantity

            user.balance += total_revenue
            user.save()
            HistoryTrade.objects.create(
                user_id=request.user,
                stock_symbol=stock,
                trade_price=stock.current_price,
                trade_quantity=quantity,
                trade_type='SELL',
                trade_dateTime=now()
            )
        else:
            messages.error(request, "Insufficient stock to sell.")


def add_comment(request, stock_symbol):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        user = request.user
        stock = get_object_or_404(Stock, pk=stock_symbol)

        StockComment.objects.create(title=title, content=content, user_id=user, stock_symbol=stock)
        return redirect('stock_comments', stock_symbol=stock_symbol)
    return redirect('stock_comments', stock_symbol=stock_symbol)


def add_reply(request, comment_id):
    if request.method == "POST":
        content = request.POST.get('content')
        user = request.user
        comment = get_object_or_404(StockComment, pk=comment_id)

        CommentReply.objects.create(content=content, user_id=user, comment_id=comment)
        return redirect('stock_comments', stock_symbol=comment.stock_symbol.pk)

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
        messages.success(request, "Thank you for your feedback!")
        return redirect('financial_system:index')  # Adjust the redirect as needed

    return render(request, 'submit_feedback.html')
