from django.urls import path
from . import views, admin_view

app_name = 'financial_system'
urlpatterns = [
    path('', views.index, name='index'),
    path('sign_up/', views.sign_up_view, name='sign_up'),
    path('register_action/', views.register_action, name='register_action'),
    path('login/', views.login_view, name='login'),
    path('login_action/', views.login_action, name='login_action'),
    path('logout/', views.log_out, name='logout'),
    path('profile/', views.user_profile_view, name='user_profile'),
    path('edit_profile_action/', views.edit_user_profile_action, name='edit_profile_action'),

    path('watchlist/', views.user_watchlist_view, name='user_watchlist_view'),
    path('watchlist/<int:stock_id>', views.user_watchlist_view, name='user_watchlist_id_view'),

    path('stocks/', views.stock_list_view, name='stock_list'),
    path('stock/<int:stock_id>', views.stock_detail_view, name='stock_detail'),

    path('trade/<int:stock_id>', views.trade, name='trade'),
    path('buy_stock/', views.buy_stock, name='buy_stock'),
    path('sell_stock/', views.sell_stock, name='sell_stock'),
    path('stock/<int:stock_id>/add_comment/', views.add_comment, name='add_comment'),
    path('comments/<int:comment_id>/add_reply/', views.add_reply, name='add_reply'),


    path('notifications/', views.user_notification_view, name='user_notification'),

    path('balance/', views.balance, name='balance'),
    path('deposit_funds/', views.deposit_funds, name='deposit_funds'),
    path('withdraw_funds/', views.withdraw_funds, name='withdraw_funds'),

    path('news/', views.news_view, name='news'),
    path('news/<int:news_id>/', views.news_detail_view, name='news_detail'),

    path('submit_feedback/', views.submit_feedback, name='submit_feedback'),


    path('base', views.base, name='base'),


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