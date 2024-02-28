import uuid

from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from financialSystem import models
from financialSystem.models import UserTable, StockInfo


def goto_login(request):
    return render(request, 'login.html')

def mylogin(request):
    # 10030370820
    # 222222
    if request.POST:
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        print(phone_number)
        print(password)
        message = ''
        try:
            adm = User.objects.get(username=phone_number)
            login(request, adm)
            user_num = UserTable.objects.count()
            stock_num = StockInfo.objects.count()
            request.session['user_name'] = phone_number
            request.session['username'] = adm.username
            request.session['online'] = True
            request.session['user_num'] = user_num
            request.session['stock_num'] = stock_num
            request.session['photo_url'] = ''
            request.session['phone_num'] = adm.username

            return redirect('financialSystem:adm_index')
        except ObjectDoesNotExist:
            try:
                user = UserTable.objects.get(phone_number=phone_number)
                if user.password == password:
                    login(request, user)
                    request.session['user_name'] = user.user_name
                    request.session['photo_url'] = user.photo_url
                    print(user.photo_url)
                    # request.session['photo_url'] = '/static/img/avatar.png'
                    request.session['user_id'] = user.user_id
                    request.session['user_email'] = user.user_email
                    request.session['account_balance'] = user.account_balance
                    request.session['id_no'] = user.id_no
                    request.session['phone_number'] = user.phone_number
                    return redirect('financialSystem:index')
                else:
                    message = "您的密码错误"
            except ObjectDoesNotExist:
                message = "用户不存在"
    return render(request, 'login.html', locals())

def log_out(request):
    logout(request)
    request.session.flush()
    return redirect('financialSystem:goto_login')

def deal_user_change(request):
    message = ""
    try:
        if request.POST:
            user_id = request.POST['user_id']
            user_name = request.POST['user_name']
            phone_number = request.POST['phone_number']
            user_sex = request.POST['user_sex']
            id_no = request.POST['id_no']
            user_email = request.POST['user_email']
            password = request.POST['password']
            conf_password = request.POST['conf_password']
            if conf_password != password:
                message = "确认密码不符"
            else:
                try:
                    user = UserTable.objects.get(user_id=user_id)
                    user.phone_number = phone_number
                    user.user_sex = user_sex
                    user.user_name = user_name
                    user.user_email = user_email
                    user.password = password
                    user.id_no = id_no
                    user.save()
                except Exception:
                    message = "修改信息失败，请仔细检查，或稍后重试"
    except Exception:
        message = "您的信息有误，请仔细检查"
    context = {
        'message': message,
    }
    return render(request, "financialSystem/user_profile.html", context)

def base(request):
    return render(request, 'base.html')


def register(request):
    return render(request, 'register.html')

def do_register(request):
    user_name = request.POST['user_name']
    phone_number = request.POST['phone_number']
    user_sex = request.POST['user_sex']
    id_no = request.POST['id_no']
    user_email = request.POST['user_email']
    password = request.POST['password']
    message = ""
    try:
        user = UserTable.objects.create(
            user_name=user_name,
            user_email=user_email,
            user_sex=user_sex,
            user_id=str(uuid.uuid4())[:8],
            id_no=id_no,
            password=password,
            phone_number=phone_number,
            account_balance=0,
        )
        user.save()
        print("success register user")
        print(user)
    except Exception:
        print(Exception)
        message = "注册失败，请检查或稍后再试！"
        return render(request, 'register.html', locals())
    return redirect('financialSystem:goto_login')


def stock_list(request):

    stockl = models.StockInfo.objects.all()
    stockt = stockl[0:100]

    context = {
        "stock": stockt
    }

    return render(request, 'stock_list.html', context)