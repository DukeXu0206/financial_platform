from django.urls import path
from . import views, admin_view

app_name = 'financialSystem'
urlpatterns = [
    # 注册登录，主页,
    path('', views.goto_login, name='goto_login'),
    path('mylogin', views.mylogin, name='mylogin'),
    path('base', views.base, name='base'),
    path('register', views.register, name='register'),
    path('index', views.index, name='index'),

    # 管理员视图与URL
    path('a/base', admin_view.adm_base, name='adm_base'),
    path('a/news', admin_view.adm_news, name='adm_news'),



    # 管理员查看新闻详情
    path('adm_news_detail/<int:news_id>', admin_view.adm_news_detail, name='adm_news_detail'),
    # 管理员编辑新闻内容
    path('adm_edit_news', admin_view.adm_edit_news, name='adm_edit_news'),
    # 管理员新建新闻
    path('adm_add_news', admin_view.adm_add_news, name='adm_add_news'),
]