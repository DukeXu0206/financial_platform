import uuid

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Case, When, IntegerField, Q, F, FloatField
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now

from financial_system import models
from financial_system.models import User, StockInfo, Watchlist, News, UserNotification, Feedback, HistoryTrade, \
    StockComment, CommentReply


def base(request):
    return render(request, 'base.html')


def index(request):
    return render(request, 'login.html')


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

    #跳转到登录
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
            # stock_num = StockInfo.objects.count()
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
    return redirect('financial_system:login_view')


# @login_required
def user_profile_view(request):
    try:
        user = User.objects.get(phone_number=request.session['phone_number'])

        context = {
            'user': user
        }

        return render(request, 'user_profile.html', context)

    except ObjectDoesNotExist:
        context = {"message": "User not recognized, please login."}
        return render(request, 'login.html', context)


# @login_required
def edit_user_profile_action(request):
    message = ""
    try:
        print("-" * 30)
        print("edit_user_profile_action")
        print("request.session['user_id']: " + request.session['user_id'])

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


def deposit_funds(request, amount):
    user = User.objects.get(user_id=request.session.get('user_id'))
    user.balance += amount
    user.save()


def withdraw_funds(request, amount):
    user = User.objects.get(user_id=request.session.get('user_id'))
    if user.balance >= amount:
        user.balance -= amount
        user.save()
        messages.success(request, "Successful Withdraw")
    else:
        messages.error(request, "Insufficient balance, unsuccessful withdraw.")


def calculate_pnl(trades):
    # Aggregate the total spent on buys and the total earned from sells
    # trades = HistoryTrade.objects.filter(user_id=user_id).values('stock_id')\
    #     .annotate(
    #         total_spent=Sum(Case(When(trade_type='BUY', then=F('trade_quantity') * F('trade_price')), output_field=FloatField(), default=0)),
    #         total_earned=Sum(Case(When(trade_type='SELL', then=F('trade_quantity') * F('trade_price')), output_field=FloatField(), default=0)),
    #     )

    # Calculate P&L for each stock
    pnl_per_stock = [{**trade, 'pnl': trade['total_earned'] - trade['total_spent']} for trade in trades]

    # Calculate overall Gross P&L
    gross_pnl = sum([trade['pnl'] for trade in pnl_per_stock])

    return pnl_per_stock, gross_pnl


def user_watchlist_view(request):
    try:
        user = User.objects.get(user_id=request.session.get('user_id'))
        stocks_in_watchlist = StockInfo.objects.filter(
            stock_id__in=Watchlist.objects.filter(user_id=user.user_id).values_list('stock_id', flat=True)
        )

        # all_trades = HistoryTrade.objects.filter(user_id=user).order_by('-trade_dateTime')

        all_trades = HistoryTrade.objects.filter(user_id=user) \
            .values('stock_id') \
            .annotate(
            stock_name=F('stock_id__stock_name'),
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
            'all_trades': all_trades,
            'open_positions': open_positions,
            'closed_positions': closed_positions,
            'pnl_per_stock': pnl_per_stock,
            'gross_pnl': gross_pnl,
            "page_title":"user watchlist"
        }

        return render(request, 'user_watchlist.html', context)

    except ObjectDoesNotExist:
        context = {"message": "User not recognized, please login."}
        return render(request, 'login.html', context)


def news_view(request):
    news = News.objects.all().order_by('-news_dataTime')

    context = {'news': news}
    return render(request, 'news.html', context)


def news_detail_view(request, news_id):
    news_item = get_object_or_404(News, news_id=news_id)
    return render(request, 'news_detail.html', {'news_item': news_item})


def stock_list_view(request):
    stock_list = models.StockInfo.objects.all()
    stock_list = stock_list[0:100]

    context = {
        "stocks": stock_list
    }

    return render(request, 'stock_list.html', context)


def stock_detail_view(request, stock_id):
    stock = get_object_or_404(StockInfo, stock_id=stock_id)
    comments = StockComment.objects.filter(stock_id=stock_id).order_by('-comment_time')
    return render(request, 'stock_detail.html', {'stock': stock, 'comments': comments})

def trade(request):
    return render(request, 'trade.html', {})

def buy_stock(request):
    if request.method == "POST":
        stock_id = request.POST.get('stock_id')
        quantity = int(request.POST.get('quantity'))

        stock = get_object_or_404(StockInfo, pk=stock_id)
        user = User.objects.get(user_id=request.session.get('user_id'))

        total_cost = stock.current_price * quantity

        if user.balance >= total_cost:
            user.balance -= total_cost
            user.save()

            # Record the transaction
            HistoryTrade.objects.create(
                user_id=user,
                stock_id=stock,
                trade_price=stock.current_price,
                trade_quantity=quantity,
                trade_type='BUY',
            )
        else:
            messages.error(request, "Insufficient balance, please deposit.")


def sell_stock(request):
    if request.method == "POST":
        stock_id = request.POST.get('stock_id')
        quantity = int(request.POST.get('quantity'))
        stock = get_object_or_404(StockInfo, pk=stock_id)
        user = User.objects.get(user_id=request.session.get('user_id'))

        trades = HistoryTrade.objects.filter(user_id=request.user, stock_id=stock).aggregate(
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
                stock_id=stock,
                trade_price=stock.current_price,
                trade_quantity=quantity,
                trade_type='SELL',
                trade_dateTime=now()
            )
        else:
            messages.error(request, "Insufficient stock to sell.")


def add_comment(request, stock_id):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        user = request.user
        stock = get_object_or_404(StockInfo, pk=stock_id)

        StockComment.objects.create(title=title, content=content, user_id=user, stock_id=stock)
        return redirect('stock_comments', stock_id=stock_id)
    return redirect('stock_comments', stock_id=stock_id)


def add_reply(request, comment_id):
    if request.method == "POST":
        content = request.POST.get('content')
        user = request.user
        comment = get_object_or_404(StockComment, pk=comment_id)

        CommentReply.objects.create(content=content, user_id=user, comment_id=comment)
        return redirect('stock_comments', stock_id=comment.stock_id.pk)

    # return redirect('stock_comments', stock_id=comment_id.stock_id.pk)


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
