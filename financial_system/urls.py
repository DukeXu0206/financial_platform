from django.urls import path
from . import views

app_name = 'financial_system'
urlpatterns = [
    path('', views.news_view, name='index'),
    path('sign_up/', views.sign_up_view, name='sign_up'),
    path('register_action/', views.register_action, name='register_action'),
    path('login/', views.login_view, name='login'),
    path('login_action/', views.login_action, name='login_action'),
    path('logout/', views.log_out, name='logout'),
    path('profile/', views.user_profile_view, name='user_profile'),
    path('edit_profile_action/', views.edit_user_profile_action, name='edit_user_profile_action'),

    path('watchlist/', views.user_watchlist_view, name='user_watchlist_view'),
    path('watchlist/<str:stock_symbol>', views.user_watchlist_view, name='user_watchlist_id_view'),
    path('add_to_watchlist/<str:stock_symbol>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove_from_watchlist/<str:stock_symbol>/', views.remove_from_watchlist, name='remove_from_watchlist'),

    path('stocks/', views.stock_list_view, name='stock_list'),
    path('stock/<str:stock_symbol>', views.stock_detail_view, name='stock_detail'),
    path('stock_current_price/', views.stock_current_price, name='stock_current_price'),

    path('trade/<str:stock_symbol>', views.trade, name='trade'),
    path('buy_stock/', views.buy_stock, name='buy_stock'),
    path('sell_stock/', views.sell_stock, name='sell_stock'),

    path('stock/<str:stock_symbol>/add_comment/', views.add_comment, name='add_comment'),
    path('comments/add_reply/', views.add_reply, name='add_reply'),


    path('notifications/', views.user_notification_view, name='user_notification'),

    path('balance/', views.balance, name='balance'),
    path('deposit_funds/', views.deposit_funds, name='deposit_funds'),
    path('withdraw_funds/', views.withdraw_funds, name='withdraw_funds'),

    path('news/', views.news_view, name='news'),
    path('news/<int:news_id>/', views.news_detail_view, name='news_detail'),

    path('search_results/', views.search_view, name='search'),

    path('submit_feedback/', views.submit_feedback, name='submit_feedback'),

    path('base', views.base, name='base'),
]